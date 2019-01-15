from bs4 import BeautifulSoup
import requests
import re


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
	
	for article in soup.find_all('header',{'class':'heading'}):
		h1 = article.find('h1')
		heading = h1.text
		info_title_list.append('Title')
		info_list.append(heading)

	for article in soup.find_all('div',{'class':'row-holder'}):
		info_title = article.find('strong',{'class':'info-title'})
		info = article.find('span',{'class':'info'})
			
		if info_title != None:
			infotitletext = (info_title.text)
			infotext = (info.text)

			infotitle_t = re.sub(r"[\n\t]*", "", infotitletext)
			infotext_t = re.sub(r"[\n\t]*", "", infotext)
			
			info_title_list.append(infotitle_t)
			info_list.append(infotext_t)
					
			
	mapped = zip(info_title_list, info_list)
	ls = list(mapped)


	f = open('data.txt','a+')
	for i in range(0,len(info_list)):
		f.write(info_list[i]+',')
	f.write('\n')

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
    i = 1
    sliced_urls = all_urls[first: last]
    for url in sliced_urls:
        fill_data(url)
        print('Url {} data fill complete !!'.format(i))				
        i=i+1		

#scrape('https://www.bookmundi.com/nepal?page=2')
#start_feeding(1,10)
