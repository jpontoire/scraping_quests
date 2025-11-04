from urllib.parse import urljoin

from minet.web import request
from minet.scrape import WonderfulSoup

MAIN_GAMES = ["Online", "Skyrim", "Oblivion", "Morrowind", "Daggerfall", "Arena"]

SITE = "https://en.uesp.net"


def construct_url(path):
    """Construct full URL from path."""
    return urljoin(SITE, path)


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


def get_quests_box(soup):
    """Get quests box from soup object."""
    title : WonderfulSoup = soup.select_one("span#Quest_Information")

    h2 = title.find_parent("h2")

    # Trouve l’élément suivant (souvent un <ul>)
    next_ul = h2.find_next_sibling("ul")
    quest_box = next_ul.scrape("b a", "href")

    return [construct_url(url) for url in quest_box]

def get_section(title, soup):
    """Retourne le contenu HTML entre <h2>title</h2> et le <h2> suivant"""
    section = soup.find("span", {"class": "mw-headline"}, string=title)
    if not section:
        return None

    h2 = section.find_parent("h2")

    content = []
    for sibling in h2.find_next_siblings():
        if sibling.name == "h2":
            break
        content.append(str(sibling.get_text()))
    return "\n".join(content).strip()