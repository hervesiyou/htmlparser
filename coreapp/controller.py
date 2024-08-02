from django.shortcuts import render
import requests

from coreapp.exceptions.url_exception import URLException
from .use_cases import *
from bs4 import BeautifulSoup

def index(request):

    if request.method!="POST":
        return render(request, "index.html", {  })
    
    data = request.POST['url']
    message=""
    title=""
    links=[]
    soup=""
    try:
        
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
            # getting reachable url
            reachable = links_reachable(links["ext_links"]) 
            #  getting login form 
            login_form = get_login_form(soup) 
            
    except URLException as e:
        print(f" Exception :{e}")
        raise e
    
    return render(request, "index.html", {"message": f"Analyse {data}, {message}","reachable":reachable,"login_form":login_form,"hx":hx,"version":version, "links":links,"soup":soup.find('title') ,"title":title})
