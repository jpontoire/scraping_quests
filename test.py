from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, get_quests_box

SITE = "https://en.uesp.net/wiki/Skyrim:The_Whispering_Door"

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

def get_content(soup):
    sections = soup.select("h2 span.mw-headline")
    print(sections)
    return

def main():
    soup = get_soup(SITE)
    section = get_section("Quest Stages", soup)
    print(section)
    return

if __name__ == "__main__":
    main()