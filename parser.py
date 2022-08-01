import requests
from bs4 import BeautifulSoup
import csv
import time


file = "./data.csv"
with open(file, mode="w", encoding='utf-8') as w_file:
	file_writer = csv.writer(w_file, lineterminator="\r")
	file_writer.writerow(["ID", "Seller", "Category", "Locations", "Price", 
		"Currency", "Rooms", "Area", "Floor"])


AZtoEN = [["Ə","A"],["I","I"],["Ğ","G"],["Ö","O"],["Ç","Ch"],["Ş","Sh"],["Ü","U"],["İ","I"],
	["ə","a"],["ı","i"],["ğ","g"],["ö","o"],["ç","ch"],["ş","sh"],["ü","u"]]

def encoder(text):
	for letter in AZtoEN:
		text = text.replace(letter[0],letter[1])
	return text


def parseLink(link):

	url = f'https://bina.az{link}'

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'html.parser')

	params = soup.find('table', class_='parameters')
	for n, p in params:
		category = encoder(p.text)
		break

	locs = soup.find('ul', class_='locations')
	locations = []
	regions = ["r.", "q.", "m."]
	for l in locs:
		if (l.text)[-2:] in regions:
			locations.append(encoder(l.text))

	return category, locations


def parser(page):

	url = f'https://bina.az/baki/alqi-satqi/menziller?page={page}'

	html = requests.get(url).text
	soup = BeautifulSoup(html, 'html.parser')


	items_Lists = soup.find_all('div', class_='items_list')

	data_list = []

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

			# location = item.find('div', class_="location").text

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

			category, locations = parseLink(link)

			try:
				link_id = int(link.split("/")[2])
			except:
				link_id = int(link.split("/")[2][:5])


			# print(link_id, product_label, category, locations, price, rooms, area, floor)

			
			data_list.append([link_id, product_label, category, locations, 
				price[1], price[0], rooms, area, floor])

	with open(file, mode="a", encoding='utf-8') as w_file:
		file_writer = csv.writer(w_file, lineterminator="\r")
		for data in data_list:
			file_writer.writerow(data)



start_time = time.time()


pages = 1000
for page in range(pages):
	print('In page:',page+1)
	parser(page+1)


time_min = round((time.time() - start_time) / 60)
time_sec = round((time.time() - start_time) % 60)
working_time = f"\nTime spent parsing: {time_min} min {time_sec} sec"
print(working_time)