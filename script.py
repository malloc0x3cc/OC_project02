import os, requests, csv, re
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
CSV_PATH = "./CSV/"

def scrapeBookInfos(book_url, csv_file):
	soup = BeautifulSoup(requests.get(book_url).content, "html.parser")
	td = soup.find_all('td')
	upc = td[0].text
	price_including_tax = td[3].text
	price_excluding_tax = td[2].text
	number_available = td[5].text
	image_url = f"{BASE_URL}{soup.find('img')['src'][6:]}"
	title = soup.find('h1').text
	
	# TODO
	product_description = "product_description"
	category = "category"
	review_rating = "review_rating"

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
	open(f"{CSV_PATH}{title}.jpg", 'wb').write(r.content)

def findAllBooks(category_url):
	# TODO: get books on all pages
	file_name = category_url[25:].replace("/index.html", '')
	catalog_page = f"{BASE_URL}{category_url}"
	
	soup = BeautifulSoup(requests.get(catalog_page).content, "html.parser")
	book_links = soup.findAll('div', attrs={'class' : 'image_container'})
	
	with open(f"{CSV_PATH}{file_name}.csv", 'w', newline='') as file:
		writer = csv.writer(file)
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
			scrapeBookInfos(f"{BASE_URL}catalogue/{book.find_all('a', href=True)[0]['href'][9:]}", writer)
			print('.', end='', flush=True)

def findAllCategories():
	soup = BeautifulSoup(requests.get(BASE_URL).content, "html.parser")
	links = []
	
	for s in soup.find_all(href=re.compile("category")):
		links.append(s['href'])
	links.pop(0)

	if (links):
		try:
			os.mkdir(CSV_PATH)
		except FileExistsError:
			print(f"The '{CSV_PATH}' directory already exists")
		else:
			print(f"Successfully created the directory '{CSV_PATH}'")

	return links

def main():
	categories = findAllCategories()
	findAllBooks(categories[0])
	# for category in categories:
		# findAllBooks(category)
	print("\nDONE!")

if __name__ == "__main__":
	main()
