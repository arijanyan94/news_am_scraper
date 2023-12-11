import requests
import concurrent.futures
from bs4 import BeautifulSoup

def get_article(url):

	resp = requests.get(url, timeout=10)
	soup = BeautifulSoup(resp.content, 'html.parser')
	if url.startswith("https://news.am"):
		title = soup.find('div', class_='article-title').get_text()
		article = soup.find('div', class_='article-text')
		prefix = "https://news.am/"

	elif url.startswith("https://tech.news"):
		article = soup.find('div', id='opennewstext')
		title = article.find('h1').get_text()
		prefix = "https://tech.news.am"

	else:
		title = soup.find('div', id='opennews').find('h1').get_text()
		article = soup.find('div', id='opennewstext')
		prefix = "https://med.news.am" if url.startswith("https://med.news") else "https://sport.news.am"

	img_url = article.img['src']
	if img_url=="https://news.am/css/images/desktop/logo.png":
		img_source = (img_url, "logo")
	else:
		img_source = f"{prefix}{img_url}"
		img_source = (img_source, "face")

	text_paragraphs = [p.get_text() for p in article.find_all('p')]
	text = " ".join(text_paragraphs)
	print(img_source)
	return [img_source, url, title, text]

def get_top_news_urls(url):

	resp = requests.get(url, timeout=10)
	soup = BeautifulSoup(resp.content, 'html.parser')
	shorts = soup.find('div', class_='news-list short-top')
	links = shorts.find_all('a')
	# Extract the 'href tag from the list of "Top News"
	urls = [f"https://news.am{link['href']}" if not link['href'].startswith('http')
												else link['href'] for link in links]
 
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

print(scrape_news())