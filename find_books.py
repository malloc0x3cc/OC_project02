from bs4 import BeautifulSoup
import requests, csv, os, threading


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
	open(f"{EXPORT_PATH}{folder_name}/{''.join(x for x in title if x.isalnum())}.jpg", 'wb').write(r.content)

def findAllBooks(category_url, current_page="index.html"):
	catalog_page = f"{BASE_URL}{category_url}"

	soup = BeautifulSoup(requests.get(catalog_page).content, "html.parser")
	book_links = soup.findAll('div', attrs={'class' : 'image_container'})
	category = soup.find('li', {'class': "active"}).text

	try:
		next_page = soup.find('li', {"class": "next"}).find('a')['href']
	except AttributeError:
		print("No more pages ahve been found.")
	else:
		print(next_page)
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
		threads = []
		for book in book_links:
			task_args = (f"{BASE_URL}catalogue/{book.find_all('a', href=True)[0]['href'][9:]}", writer, category)
			t = threading.Thread(target=scrapeBookInfos, args=task_args, daemon=True)
			threads.append(t)
			t.start()

		# wait for the threads to complete
		for t in threads:
		    t.join()
