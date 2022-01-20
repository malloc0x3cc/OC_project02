#!/usr/bin/python
from find_books import findAllBooks
import os, requests, csv, re, time
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
EXPORT_PATH = "./exports/"

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
	# for category in categories:
		# findAllBooks(category)
	print("\nDONE!")
	print("--- %s seconds ---" % (time.time() - start_time))