#!/bin/python3

# vocab_page_content = bs(vocab_page.content, "html5lib")

import requests
import re
import random
import os

from gtts import gTTS
#random.randrange() with two arguments
#print("Total score for {0} is {1}".format(name, score))
from bs4 import BeautifulSoup as bs

# headers
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

site = "https://www.antoloji.com"

sair = "ali-lidar"#input("sair adi: ")

siir_page_list = []
#last_page = 0

# Siirlistesi Sayfada

def getPoemList():
    with requests.Session() as s:

        siir_list_page = s.get(site +"/" +sair +"/siirleri/ara-/sirala-/sayfa-{0}".format(random.randrange(1, getPageLimit())))# 4 değişecek for dongüsü


#        siir_list_page_content = bs(siir_list_page.content, "html5lib")

        siir_list_page_content = bs(siir_list_page.content, 'html5lib')
        link_raw = siir_list_page_content.findAll('div', {'class':'list-number'})
    
        for g in link_raw:
            a = g.find('a')
            siir_page_list.append(site + a['href'])

#getPoemList()

def getPageLimit():
    with requests.Session() as s:
        main_page = s.get(site +'/' +sair + '/siirleri/ara-/sirala-/sayfa-1' )
        
        main_page_content = bs(main_page.content, 'html5lib')
        
        for g in main_page_content.findAll('li', {'class': 'PagedList-skipToLast'}):
            a = g.find('a')
            last_page_raw = a['href']
        return int(re.findall(r'\d+', last_page_raw)[0])

#getPoem
#https://www.antoloji.com/sen-en-cok-kar-yagarken-guzeldin-siiri/#

def getPoem():
    with requests.Session() as s:
        poem_page = s.get(siir_page_list[random.randrange(0,(len(siir_page_list) -1))])
        
        poem_page_content = bs(poem_page.content, 'html5lib')
        #poem_page = s.get(site + "{0}")
        #print(poem_page_content, 'html5lib')

        poem_raw = str(poem_page_content.find('div',attrs={'class':'pd-text'}))
        
        poem = str(bs(poem_raw, 'lxml').text)
        #re.sub('[A-Za-z0-9]+', ''i poem)

        return re.sub( '\W+',' ', poem)


getPageLimit()
getPoemList()

lang = 'tr'
poem = getPoem()
speech = gTTS(text=poem, lang=lang, slow=True)
speech.save('raw.mp3')
print(poem)
os.system("cvlc raw.mp3")

