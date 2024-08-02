import pytest 
import requests
from bs4 import BeautifulSoup

 
@pytest.mark.django_db   
def fetch_html(url): 
    response = requests.get(url)
    response.raise_for_status() 
    return response.text

def test_login_form_exists():
    url="https://github.com/login"
    html_content = fetch_html(url)
    soup = BeautifulSoup(html_content, 'html.parser') 
    login_form = soup.find('form', {'action': '/login/'}) 
    assert login_form is not None, "Un Login form doit exister."

def test_form(): 
    url="https://github.com/login"
    html_content = fetch_html(url)
    soup = BeautifulSoup(html_content, 'html.parser') 
    element = soup.find_all('form') 
    assert element is not None, "Le formulaire doit exister"
