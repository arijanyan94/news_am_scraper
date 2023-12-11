import requests
import concurrent.futures
from bs4 import BeautifulSoup

def get_article(url):

	resp = requests.get(url)
	soup = BeautifulSoup(resp.content, 'html.parser')

	title = soup.find('div', class_='article-title').get_text()
	article = soup.find('div', class_='article-text')
	img_url = article.img['src']
	# if the article doesn't have an image, the logo image is returned,
	# and no need to run the face detection on it
	if img_url=="https://news.am/css/images/desktop/logo.png":
		img_source = (img_url, "logo")
	else:
		img_source = f"https://news.am/{img_url}"
		img_source = (img_source, "face")

	text_paragraphs = [p.get_text() for p in article.find_all('p')]
	text = " ".join(text_paragraphs)

	return [img_source, url, title, text]

def get_top_news_urls(url):

	resp = requests.get(url)
	soup = BeautifulSoup(resp.content, 'html.parser')
	shorts = soup.find('div', class_='news-list short-top')
	links = shorts.find_all('a')
	# Extract the 'href tag from the list of "Top News"
	urls = [f"https://news.am{link['href']}" for link in links]

	return urls

def scrape_news():

	base_url = "https://news.am/eng/"
	urls = get_top_news_urls(base_url)
	results = []
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
		future_to_url = {executor.submit(get_article, url): url for url in urls}
		for future in concurrent.futures.as_completed(future_to_url):
			results.append(future.result())

	print("finished scraping")

	return results
