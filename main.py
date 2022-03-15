#!/usr/bin/python
from find_books import findAllBooks
import os, requests, csv, re, time, threading
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
EXPORT_PATH = "./exports/"

def findAllCategories():
	r = requests.get(BASE_URL)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.content, "html.parser")
	links = []

	for s in soup.find_all(href=re.compile("category")):
		links.append(s['href'])
	links.pop(0)

	try:
		os.mkdir(EXPORT_PATH)
		print(f"Successfully created the directory '{EXPORT_PATH}'")
	except FileExistsError:
		print(f"The '{EXPORT_PATH}' directory already exists")
	return links

if __name__ == "__main__":
	start_time = time.time()
	categories = findAllCategories()

	threads = []
	for category in categories:
		t = threading.Thread(target=findAllBooks, args=(category, ))
		threads.append(t)
		t.start()

	# wait for the threads to complete
	for t in threads:
		t.join()

	print("\nDONE!")
	print("--- %s seconds ---" % (time.time() - start_time))
