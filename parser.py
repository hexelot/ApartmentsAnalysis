import requests
from bs4 import BeautifulSoup
import csv


# file = "./test.csv"
# with open(file, mode="w", encoding='utf-8') as w_file:
# 	file_writer = csv.writer(w_file, delimiter = ";", lineterminator="\r")
# 	file_writer.writerow(["Seller", "Location", "Price", "Currency", "Rooms", "Area", "Floor"])


def encoder(text):
	pass


def parseLink(link):

	url = f'https://bina.az{link}'

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'html.parser')

	params = soup.find('table', class_='parameters')
	for n, p in params:
		category = p.text
		break

	locations = soup.find('ul', class_='locations')
	for l in locations:
		print(l.text)


def parser(page):

	url = f'https://bina.az/baki/alqi-satqi/menziller?page={page}'

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'html.parser')


	items_Lists = soup.find_all('div', class_='items_list')

	for items_list in items_Lists:
		items = items_list.find_all('div', class_='items-i')

		for item in items:

			product_label = item.find('div', class_="products-label")
			if product_label == None:
				product_label = "Owner"
			elif product_label.text == "Kompleks":
				continue
			else:
				product_label = product_label.text

			location = item.find('div', class_="location").text
			location = location.replace("ə","a").replace("ı","i").replace("ğ","g").replace("ö","o")
			location = location.replace("ç","ch").replace("ş","sh").replace("ü","u")
			location = location.replace("Ə","A").replace("I","I").replace("Ğ","G").replace("Ö","O")
			location = location.replace("Ç","Ch").replace("Ş","Sh").replace("Ü","U").replace("İ","I")

			price = [item.find('span', class_="price-cur").text,
				int(item.find('span', class_="price-val").text.replace(" ", ""))]

			params = []
			ul = item.find('ul', class_="name")
			for li in ul:
				params.append(li.text.split(" ")[0])
			rooms = int(params[0])
			area = float(params[1])
			floor = int(params[2].split("/")[0])

			link = item.find('a', class_="item_link")["href"]

			parseLink(link)
			exit()

			print(product_label, location, price, rooms, area, floor, link)

			
			# data = [product_label, location, price[1], price[0], rooms, area, floor]
			# with open(file, mode="a", encoding='utf-8') as w_file:
			# 	file_writer = csv.writer(w_file, delimiter = ";", lineterminator="\r")
			# 	file_writer.writerow(data)



pages = 1

for page in range(pages):
	parser(page+1)