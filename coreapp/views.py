from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re 

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

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
def index(request):
    return render(request, "index.html", {  })

def get_login_form(soup):
    forms=[]
    for form in soup.find_all('form'):
        forms.append( form.get("action") )
        
    for form in soup.find_all('input'):
        if form.get("type") in ["text","email","password"]:
            forms.append( form.get("type") )
    return forms
        
    # match = re.search(r"\login", url)

def check_internal_link(base_url, url):
    if( base_url.startswith("http") or base_url.startswith("https") ):
        base_url=(base_url.split("//")[1]).split('/')[0]
    return True if url.startswith("/") else url.startswith(base_url)

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
def parse(request):
    data = request.POST['url']
    message=""
    title=""
    links=[]
    soup=""
    if not url_valide(data) :
        message = "Url non valide , merci d'entrer une url de forme http(s)://nom.extension"
        return render(request, "index.html", {"message": message})
    else:
        #  here i have a valide url
        target_url = data
        response_data = requests.get(target_url)
        soup = BeautifulSoup(response_data.text, 'html.parser')
        title = soup.title.string
        # getting the html version
        version = soup.find('html')
        version = version.get('version') 
        # grouping all hx
        hx=headings_grouped(soup)
        # getting all links grouped by extenals and internals
        links = getting_links(soup,target_url)
        #  getting login form 
        login_form = get_login_form(soup)
        print(login_form)
 

    return render(request, "index.html", {"message": f"Analyse {data}, <br> {message}","hx":hx,"version":version, "links":links,"soup":soup.find('title') ,"title":title})
 