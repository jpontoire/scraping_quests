import csv
import requests

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url, remove_fragment

SITE = "https://masseffect.fandom.com/wiki/Missions"

GAMES = ["Mass Effect", "Mass Effect 2", "Mass Effect 3", "Mass Effect: Infiltrator", "Mass Effect: Andromeda"]

def get_game_quests_links(title, soup):
    """Retourne la liste des balises <a> entre <h2>title</h2> et le <h2> suivant"""
    section = soup.find("span", {"class": "mw-headline"}, string=title)
    if not section:
        return None

    h2 = section.find_parent("h2")

    content = []
    for sibling in h2.find_next_siblings():
        if sibling.name == "h2":
            break
        quests = sibling.scrape("a", "href")
        for quest in quests:
            content.append(quest)
    return content

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

def main():
    soup = get_soup(SITE)
    cpt = 0
    for game in GAMES:
        print(f"Début du scraping pour {game}...")
        list_quests = get_game_quests_links(game, soup)
        set_quests = set()
        for quest in list_quests:
            response = requests.get(construct_url("https://masseffect.fandom.com", quest), allow_redirects=True)
            quest_url =remove_fragment(response.url)
            set_quests.add(quest_url)
        list_quests = list(set_quests)
        total = len(list_quests)
        with open(f"{game.replace(" ", "")}_quests.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Quest", "Acquisition", "Walkthrough"])
            for link in list_quests:
                if link:
                    quest_soup = get_soup(link)
                    acquisition = get_section("Acquisition", quest_soup)
                    walkthrough = get_section("Walkthrough", quest_soup)
                    if not acquisition and not walkthrough:
                        continue
                    writer.writerow([link, acquisition, walkthrough])
                    cpt += 1
                    print(f"{cpt}/{total} : {link}")

if __name__ == "__main__":
    main()

