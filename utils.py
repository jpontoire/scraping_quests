from urllib.parse import urljoin

from minet.web import request
from minet.scrape import WonderfulSoup

def construct_url(site, path):
    """Construct full URL from path."""
    return urljoin(site, path)


def get_soup(url):
    """Get BeautifulSoup object from URL."""
    response = request(url)
    soup = response.soup()
    return soup

def get_html(url):
    """Get HTML from URL and save to file."""
    soup = get_soup(url)
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(str(soup))
    return

def remove_fragment(link):
    """Supprime le fragment d'une URL (la partie après #)"""
    return link.split("#")[0]
