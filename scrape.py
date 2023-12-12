import concurrent.futures
import time
import requests
from bs4 import BeautifulSoup

def get_article(url):
	"""
	Extracs the necessary data from page HTML.

	Args:
		url: page url for scraping.

	Returns:
		Returns a list containing image URL, page URL,
							article title and text.
	"""
	resp = requests.get(url, timeout=10)
	soup = BeautifulSoup(resp.content, 'html.parser')
	# "Top News" section can contain urls of multiple sources, which slightly
	# differ in HTML structure, thats why this statements are needed
	if url.startswith("https://news.am"):
		title = soup.find('div', class_='article-title').get_text()
		article = soup.find('div', class_='article-text')
		image_prefix = "https://news.am/"

	elif url.startswith("https://tech.news"):
		article = soup.find('div', id='opennewstext')
		title = article.find('h1').get_text()
		image_prefix = "https://tech.news.am"

	else:
		title = soup.find('div', id='opennews').find('h1').get_text()
		article = soup.find('div', id='opennewstext')
		if url.startswith("https://med.news"):
			image_prefix = "https://med.news.am"
		elif url.startswith("https://sport.news"):
			image_prefix = "https://sport.news.am"
		else:
			image_prefix = "https://style.news.am"

	img_url = article.img['src']
	if img_url=="https://news.am/css/images/desktop/logo.png":
		img_source = (img_url, False) # The boolean value is used for face detecion
	else:
		img_source = f"{image_prefix}{img_url}"
		img_source = (img_source, True)

	# Collects all the paragraphs in a list
	text_paragraphs = [p.get_text() for p in article.find_all('p')]
	# Joins the in one string with a space delimeter
	text = " ".join(text_paragraphs)

	return [img_source, url, title, text]

def get_top_news_urls(url):
	"""
	Requests the Home page and extracs the 
	"Top New" section URLs

	Args:
		url: Home page URL.

	Returns:
		List of "Top News" section URLs.
	"""
	resp = requests.get(url, timeout=10)
	soup = BeautifulSoup(resp.content, 'html.parser')
	shorts = soup.find('div', class_='news-list short-top')
	links = shorts.find_all('a')
	# Extract the 'href tag from the list of "Top News"
	urls = [f"https://news.am{link['href']}" if not link['href'].startswith('http')
												else link['href'] for link in links]

	return urls

def scrape_news():
	"""
	Collects the "Top News" section information in paralell

	Returns:
		2d List of scraped data
	"""
	base_url = "https://news.am/eng/"
	st_time = time.time()
	urls = get_top_news_urls(base_url)
	results = []
	with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
		future_to_url = {executor.submit(get_article, url): url for url in urls}
		for future in concurrent.futures.as_completed(future_to_url):
			results.append(future.result())

	print(f"Finished Scraping in {time.time() - st_time} seconds")

	return results
