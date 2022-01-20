from scrape_book import scrapeBookInfos
from bs4 import BeautifulSoup
import requests, csv, os


BASE_URL = "https://books.toscrape.com/"
EXPORT_PATH = "./exports/"

def findAllBooks(category_url, current_page="index.html"):
	catalog_page = f"{BASE_URL}{category_url}"

	soup = BeautifulSoup(requests.get(catalog_page).content, "html.parser")
	book_links = soup.findAll('div', attrs={'class' : 'image_container'})
	category = soup.find('li', {'class': "active"}).text

	try:
		next_page = soup.find('li', {"class": "next"}).find('a')['href']
	except AttributeError:
		pass
	else:
		findAllBooks(category_url.replace(current_page, next_page), next_page)


	try:
		os.mkdir(f"{EXPORT_PATH}{category}/")
	except FileExistsError:
		print(f"\nAppending to '{EXPORT_PATH}/{category}/'")

	with open(f"{EXPORT_PATH}{category}/{category}.csv", 'a', newline='') as file:
		writer = csv.writer(file)
		# Top row
		if (os.stat(f"{EXPORT_PATH}{category}/{category}.csv").st_size == 0):
			writer.writerow([
				"product_page_url",
				"universal_product_code (upc)",
				"title",
				"price_including_tax",
				"price_excluding_tax",
				"number_available",
				"product_description",
				"category",
				"review_rating",
				"image_url"
			])

		print(f"\nScraping {len(book_links)} books from {catalog_page}, please wait...")
		for book in book_links:
			scrapeBookInfos(f"{BASE_URL}catalogue/{book.find_all('a', href=True)[0]['href'][9:]}", writer, category) # Could be better / in a variable ?
			print('.', end='', flush=True)
