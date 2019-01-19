from bs4 import BeautifulSoup
import requests
import re
import numpy as np


# GET ALL URLS
all_urls = []


def all_url(h2):
	a = h2.find('a')
	url = 'https://www.bookmundi.com'+a['href']
	all_urls.append(url)
	print('{} no of urls scrapped'.format(len(all_urls)))




def scrape(url):
	source_code = requests.get(url)
	html = source_code.text
	soup = BeautifulSoup(html, 'html.parser')
	i = 1
	for article in soup.find_all('div',{'class':'trips-block'}):
		h2 = article.find('h2')
		all_url(h2)


	stop = soup.find('li',{'class':'hidden'})
	next = soup.find('li',{'class':'next'})
	a = next.find('a')
	next = a['href']
	if stop == None:
	    scrape(next)
	else:
		return
	return


def fill_data(url):

	source_code = requests.get(url)
	html = source_code.text
	soup = BeautifulSoup(html,'html.parser')

	info_title_list = []
	info_list = []
	itemprops = []
	otherinfo = []

	# Obtain Price of the package as:
	messy_price = soup.find('span',{'id':'fromPrice'}).text
	price = re.sub(r"[,]*", "", messy_price)
	price = str(int(price)*110)


	# Obtain Rating of the package as:
	cost = soup.find('span',{'class':'rat-count'})
	f = lambda rate: rate.text if rate != None else np.nan
	rating = str(f(cost))
	rating = re.sub(r"[\n\t]*", "", rating)
	tour = 'nan'
	trek = 'nan'


    # Obtain Name of the package as:
	for article in soup.find_all('header',{'class':'heading'}):
		h1 = article.find('h1')
		name = re.sub(r"[,]*", "", h1.text).strip()

	# Obtain Duration as:

	for title in soup.find_all('span',{'class':'duration'}):
	    durationclass = title.find('span', {'class':'info'})
	    duration = re.sub(r"[\n\t]*", "", durationclass.text)
	    

	# Obtain Tour-Type as:

	for title in soup.find_all('span',{'class':'tour-type'}):
	    tour = title.find('span', {'class':'info'})
	    tour = re.sub(r"[\n\t]*", "", tour.text)
	    

    # Obtain Trek-difficulty as:

	for title in soup.find_all('span',{'class':'difficulty-icon'}):
	    trek = title.find('span', {'class':'info'})
	    trek = re.sub(r"[\n\t]*", "", trek.text)
        
    # Obtain Location and primary activity of the package as:
	
	for item in soup.find_all('span',{'itemprop':'title'}):
		itemprops.append(item.text)
	
	location = re.sub(r"[,]*", "", itemprops[3]).strip()
	primary_activity = re.sub(r"[,]*", "", itemprops[4]).strip()
    
	# Obtain Operation and secondary activity of the package as:
	for article in soup.find_all('span',{'class':'product-title'}):
		for info in article.find_all('a'):
			otherinfo.append(info.text)
    
	operator = re.sub(r"[,]*", "", otherinfo[0]).strip()
	secondary_activity = re.sub(r"[,]*", "", otherinfo[1]).strip()
	
	info_list.append(name)
	info_list.append(price)
	info_list.append(duration)
	info_list.append(rating)
	info_list.append(tour)
	info_list.append(trek)
	info_list.append(operator)
	info_list.append(location)
	info_list.append(primary_activity)
	info_list.append(secondary_activity)

	f = open('finaldatasets.csv','a+')

	for i in range(0,len(info_list)):
		f.write(info_list[i]+' ,, ')
	f.write('\n')




def start_feeding(first, last):
    i = first
    sliced_urls = all_urls[first: last]
    for url in sliced_urls:
        fill_data(url)
        print('Url {} data fill complete !!'.format(i))
        i=i+1


def main():
    f = open("finaldatasets.csv", "w")
    f.write('Name of Package'+' ,, '+
		'Price'+' ,, '+
		'Duration'+' ,, '+
		'Rating'+' ,, '+
		'Tour Type'+' ,, '+
		'Trek Difficulty'+' ,, '+
		'Operator'+' ,, '+
		'Location'+' ,, '+
		'Primary Activity'+' ,, '+
		'Secondary Activity'+' ,, '+
		'\n')
    
#main()
#scrape('https://www.bookmundi.com/nepal?page=22')
#start_feeding(0,10)
