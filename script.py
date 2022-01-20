#!/usr/bin/python
import os, requests, csv, re, time
from bs4 import BeautifulSoup


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

def findAllBooks(category_url, current_page="index.html"):
	# TODO: get books on all pages
	file_name = category_url[25:].replace(f"/{current_page}", '')
	catalog_page = f"{BASE_URL}{category_url}"

	soup = BeautifulSoup(requests.get(catalog_page).content, "html.parser")
	book_links = soup.findAll('div', attrs={'class' : 'image_container'})

	try:
		next_page = soup.find('li', {"class": "next"}).find('a')['href']
	except AttributeError:
		pass
	else:
		findAllBooks(category_url.replace(current_page, next_page), next_page)


	try:
		os.mkdir(f"{EXPORT_PATH}{file_name}/")
	except FileExistsError:
		print(f"\nAppending to '{EXPORT_PATH}/{file_name}/'")

	with open(f"{EXPORT_PATH}{file_name}/{file_name}.csv", 'a', newline='') as file:
		writer = csv.writer(file)
		# Top row
		if (os.stat(f"{EXPORT_PATH}{file_name}/{file_name}.csv").st_size == 0):
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
			scrapeBookInfos(f"{BASE_URL}catalogue/{book.find_all('a', href=True)[0]['href'][9:]}", writer, file_name) # Could be better / in a variable ?
			print('.', end='', flush=True)

def findAllCategories():
	soup = BeautifulSoup(requests.get(BASE_URL).content, "html.parser")
	links = []

	for s in soup.find_all(href=re.compile("category")):
		links.append(s['href'])
	links.pop(0)

	try:
		os.mkdir(EXPORT_PATH)
	except FileExistsError:
		print(f"The '{EXPORT_PATH}' directory already exists")
	else:
		print(f"Successfully created the directory '{EXPORT_PATH}'")
	return links

if __name__ == "__main__":
	start_time = time.time()
	categories = findAllCategories()
	findAllBooks(categories[1])
	# findAllBooks(categories[3])
	# for category in categories:
		# findAllBooks(category)
	print("\nDONE!")
	print("--- %s seconds ---" % (time.time() - start_time))
