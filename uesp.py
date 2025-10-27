from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

SITE = "https://en.uesp.net"


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


def get_games():
    """Get list of games from UESP site."""
    soup = get_soup(SITE)
    list_games = soup.scrape("table.vtop b>a", "href")
    for i in range(0, len(list_games)-1):
        list_games[i] = urljoin(SITE, list_games[i])
    print(list_games)
    return



def main():
    get_games()
    return


if __name__ == "__main__":
    main()