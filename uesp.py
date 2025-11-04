import csv

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url


MAIN_GAMES = ["Online", "Skyrim", "Oblivion", "Morrowind", "Daggerfall", "Arena"]

SITE = "https://en.uesp.net"

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

def get_quest_link_by_game(game):
    return f"https://en.uesp.net/wiki/Category:{game}-Quests"

def get_quests_from_soup(soup):
    return soup.scrape("div#mw-pages li a", "href")

def get_next_page_link(soup):
    next_page = soup.scrape_one("a:contains('next page')", "href")
    if next_page:
        return construct_url(SITE, next_page)
    return None

def get_quests_pages(game):
    quests = []
    pages = []
    pages.append(get_quest_link_by_game(game))
    for page_url in pages:
        soup = get_soup(page_url)
        for quest in get_quests_from_soup(soup):
            quests.append(construct_url(SITE, quest))
        next_page = get_next_page_link(soup)
        if next_page:
            pages.append(next_page)
    return quests

def get_content(soup):
    quick = get_section("Quick Walkthrough", soup)
    detailed = get_section("Detailed Walkthrough", soup)
    return quick, detailed

def main():
    quests = get_quests_pages("Arena")
    cpt = 0
    total = len(quests)

    with open("arena_quests.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["Quest", "Quick Walkthrough", "Detailed Walkthrough"])

        for quest in quests:
            if "miscellaneous" in quest.lower():
                continue
            soup = get_soup(quest)
            quick, detailed = get_content(soup)
            
            quick = (quick or "").replace("\n", " ").strip()
            detailed = (detailed or "").replace("\n", " ").strip()
            
            writer.writerow([quest, quick, detailed])

            cpt += 1
            print(f"{cpt}/{total} : {quest}")

    print("Collecte terminée.")


if __name__ == "__main__":
    main()