
import re
from typing import Dict 
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


import requests
from bs4 import BeautifulSoup

def is_link_reachable(url):
    try:
        response = requests.get(url) 
        if response.status_code == 200:
            return {"status":True, "message":f"Le lien {url} est atteignable."}
        else: 
            return {"status": False,"message":f" Desolé, {url} est inatteignable: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        print(f"Une erreur : {e}")
        return False

def links_reachable(links):
    alls:Dict = {} 
    for link in links:
        if(link != None and ( link.startswith("http") or link.startswith("www") ) ):
            alls.update({link: is_link_reachable(link),"info":requests.head(link)})
    return alls;

def url_valide(url): 
    validate = URLValidator()  
    if url is None or len(url)<5:
        return False
    match = re.search(r"\.", url)
    try:
        validate(url) 
        return True
    except ValidationError as e: 
        return bool(match)


def get_login_form(soup):
    
    forms = [form.get("action") for form in soup.find_all('form')]
    for form in soup.find_all('input'):
        if form.get("type") in ["text","email","password"]:
            forms.extend( form.get("type") )
    return forms 

def check_internal_link(base_url, url):
    if( base_url.startswith("http") or base_url.startswith("https") ):
        base_url=(base_url.split("//")[1]).split('/')[0]
    if url != None:
        return True if  url.startswith("/") else url.startswith(base_url)
    return False

def getting_links(soup,base_url): 
    links = [ link.get('href') for link in soup.find_all('a') ]  
    links.extend(link.get('href') for link in soup.find_all('link'))
    internal=[]
    external=[]
    nbint=0
    nbext=0
    for link in links:
        if check_internal_link(base_url,link):
            nbint+=1
            internal.append(link)
        else:
            nbext+=1
            external.append(link) 
    return {"nbext":nbext,"ext_links":external,"nbint":nbint,"int_links":internal,"links":links}

def headings_grouped(soup):
    heading_counts = {}  
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tag_level = int(tag.name[1])
        if tag_level in heading_counts:
            heading_counts[tag_level] += 1 
        else:
            heading_counts[tag_level] = 1  
   
    return heading_counts