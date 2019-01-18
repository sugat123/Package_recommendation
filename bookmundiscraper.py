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

	# Obtain Price of the package as:
	messy_price = soup.find('span',{'id':'fromPrice'}).text
	price = re.sub(r"[,]*", "", messy_price)


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
		name = h1.text

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
	    






	info_list.append(name)
	info_list.append(price)
	info_list.append(duration)
	info_list.append(rating)
	info_list.append(tour)
	info_list.append(trek)

	f = open('datasets.csv','a+')

	for i in range(0,len(info_list)):
		f.write(info_list[i]+',,')
	f.write('\n'+'\n')

	'''
def start_feeding(first,last):
        i=1
        	sliced_urls = all_urls[first:last]
        	for url in all_urls:
        		fill_data(url)
        		print('Url {} data fill complete !!'.format(i))
        		i = i+1


'''
def start_feeding(first, last):
    i = first
    sliced_urls = all_urls[first: last]
    for url in sliced_urls:
        fill_data(url)
        print('Url {} data fill complete !!'.format(i))
        i=i+1


def main():
    f = open("datasets.csv", "w")
    f.write('Name of Package'+',,'+
		'Price'+',,'+
		'Duration'+',,'+
		'Rating'+',,'+
		'Tour Type'+',,'+
		'Trek Difficulty'+',,'+
		'\n'+'\n')
    
#main()
#scrape('https://www.bookmundi.com/nepal?page=22')
#start_feeding(0,10)
