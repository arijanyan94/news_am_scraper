from flask import Flask, render_template_string, jsonify
from transformers import pipeline, BartForConditionalGeneration, BartTokenizer
from scrape import scrape_news
from face_detection import detect_faces

app = Flask(__name__)
DATA = None

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)
summarizer = pipeline("summarization",
						model=model,
						tokenizer=tokenizer,
						device=-1)

@app.route('/')
def index():
	"""
	Renders the frontend to Webpage

	Returns:
		The Webpage
	"""
	return render_template_string(open('templates/index.html').read())

@app.route('/get_articles')
def get_articles():
	"""
	Calls the main scraping module and distributes
	the data within the HTML tags.

	Returns:
		HTML string
	"""
	global DATA
	# Owerwrites the DATA object to use later in summarization and face detection.
	DATA = scrape_news()
	articles_html = ""
	for indx, item in enumerate(DATA):
		articles_html += f'''
			<div class="article">
				<h2><a href="{item[1]}" target="_blank">{item[2]}</a></h2>
				<img src="{item[0][0]}" alt="Article Image">
				<p class="article-text" id="article_{indx}">{item[3]}</p>
				<a href="{item[1]}" target="_blank">Read more...</a>
			</div>
		'''
	return articles_html

@app.route('/get_summary/<int:index>')
def get_summary(index):
	"""
	Calls the summarization function.

	Args:
		index: the index of the article

	Returns:
		json object with index and summarized text
	"""
	global DATA
	if DATA and index < len(DATA):
		article_text = DATA[index][3]
		summary = summarize(article_text)
		return jsonify({'index': index, 'summary': summary})
	else:
		return jsonify({'error': 'Article index out of range'})

@app.route('/process_image/<int:index>', methods=['GET'])
def process_images(index):
	"""
	Calls the summarization face detection module.

	Args:
		index: the index of the image

	Returns:
		json object with base64 string
	"""	
	global DATA
	if DATA and index < len(DATA):
		image = DATA[index][0]
		processed_img = detect_faces(image[0], image[1])
		return jsonify({'processedImg': processed_img})
	else:
		return jsonify({'error': 'Index out of range'})

def summarize(text):
	"""
	Uses Bart-Cnn model to summarize the text.
	Adjustes the text lenght to be no more than 50 words.

	Args:
		index: the text to summarize

	Returns:
		string of summarized text
	"""
	summary = summarizer(text, max_length=50, min_length=30, do_sample=False)
	text = summary[0]['summary_text']
	# To control the text words count
	text_split = text.split(" ")
	if len(text_split) > 50:
		text = " ".join(text_split[:50])
		# To avoid that the sentence ends with the below characters
		if text[-1] in [',', ':', '"', "'"]:
			text = text[:-1] + '...'
		elif text[-1].isalpha():
			text = text + '...'

	return text

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
