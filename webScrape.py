import requests 
from bs4 import BeautifulSoup 
import nltk   
from urllib.request import urlopen

def get():
    url = "http://0.0.0.0:80/coord"    
    print("read html")
    html = urlopen(url).read()    
    soup = BeautifulSoup(html, 'html.parser')
    strhtm = soup.prettify()
    # raw = BeautifulSoup.get_text(html)  
    print(strhtm) 