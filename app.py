from flask import Flask, render_template_string, jsonify
from scrape import scrape_news
from face_detection import detect_faces
from transformers import pipeline, BartForConditionalGeneration, BartTokenizer

app = Flask(__name__)
sample_data = None

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)
summarizer = pipeline("summarization", 
						model=model, 
						tokenizer=tokenizer,
						device=-1)

@app.route('/')
def index():
	return render_template_string(open('templates/index.html').read())

@app.route('/get_articles')
def get_articles():
	global sample_data
	sample_data = scrape_news()
	articles_html = ""
	for index, item in enumerate(sample_data):
		articles_html += f'''
			<div class="article">
				<h2><a href="{item[1]}" target="_blank">{item[2]}</a></h2>
				<img src="{item[0][0]}" alt="Article Image">
				<p class="article-text" id="article_{index}">{item[3]}</p>
				<a href="{item[1]}" target="_blank">Read more...</a>
			</div>
		'''
	return articles_html

@app.route('/get_summary/<int:index>')
def get_summary(index):
	global sample_data
	if sample_data and index < len(sample_data):
		article_text = sample_data[index][3]
		summary = summarize(article_text)
		return jsonify({'index': index, 'summary': summary})
	else:
		return jsonify({'error': 'Article index out of range'})

# Route to process images asynchronously one by one
@app.route('/process_image/<int:index>', methods=['GET'])
def process_images(index):
	global sample_data
	if sample_data and index < len(sample_data):
		image = sample_data[index][0]
		processed_img = detect_faces(image[0], image[1]=='face')
		return jsonify({'processedImg': processed_img})
	else:
		return jsonify({'error': 'Index out of range'})

def summarize(text):

	global summarizer
	# Adjust the max_length and min_length parameters for desired summary length
	summary = summarizer(text, max_length=50, min_length=30, do_sample=False)
	text = summary[0]['summary_text']
	# To control the text words count
	text_split = text.split(" ")
	if len(text_split) > 50:
		text = " ".join(text_split[:50])
		if text[-1] in [',', ':', '"', "'"]:
			text = text[:-1] + '...'
		elif text[-1].isalpha():
			text = text + '...'

	return text

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
