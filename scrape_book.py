from bs4 import BeautifulSoup
import requests, csv


BASE_URL = "https://books.toscrape.com/"
EXPORT_PATH = "./exports/"

def scrapeBookInfos(book_url, csv_file, folder_name):
	soup = BeautifulSoup(requests.get(book_url).content, "html.parser")
	td = soup.find_all('td')
	p = soup.find_all('p')

	upc = td[0].text
	price_including_tax = td[3].text
	price_excluding_tax = td[2].text
	number_available = td[5].text
	image_url = f"{BASE_URL}{soup.find('img')['src'][6:]}"
	title = soup.find('h1').text
	product_description = p[3].text
	review_rating = p[2]['class'][1]
	category = soup.find_all('a')[3].text

	# Pushing book infos in a row
	csv_file.writerow([
		book_url,
		upc,
		title,
		price_including_tax,
		price_excluding_tax,
		number_available,
		product_description,
		category,
		review_rating,
		image_url
	])

	# download image
	r = requests.get(image_url, allow_redirects=True)
	open(f"{EXPORT_PATH}{folder_name}/{title}.jpg", 'wb').write(r.content)
