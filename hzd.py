import csv
import requests
import re

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url, remove_fragment

MAIN_SITE = "https://horizon.fandom.com/wiki/Horizon_Zero_Dawn_quests"

SECTIONS = ["Main_quests", "Side_quests", "Errands"]

def get_game_quests_links(title, soup):
    """Retourne la liste des balises <a> entre <h2>title</h2> et le <h2> suivant"""
    section = soup.find("span", class_="mw-headline", id=title)
    if not section:
        return None

    h2 = section.find_parent("h2")

    content = []
    for sibling in h2.find_next_siblings():
        if sibling.name == "h2":
            break
        quests = sibling.scrape("td:nth-child(1) a", "href")
        for quest in quests:
            content.append(quest)
    return content

def get_quest_content(soup):
    section = soup.find("span", {"class": "mw-headline"}, string="Synopsis")
    if not section:
        section = soup.find("span", {"class": "mw-headline"}, string="Description")

    content = []
    if section:
        h2 = section.find_parent("h2")
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2":
                break
            content.append(str(sibling.get_text()))
    
    objectives = soup.find("span", {"class": "mw-headline"}, string="Objectives")
    obj = []
    if objectives:
        h2 = objectives.find_parent("h2")
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2":
                break
            obj.append(str(sibling.get_text()))


    return "\n".join(content).strip(), "\n".join(obj).strip()


def main():
    soup = get_soup(MAIN_SITE)
    with open("hzd_quests.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Quest URL", "Category", "Synopsis", "Objectives"])
        for category in SECTIONS:
            quest_links = get_game_quests_links(category, soup)
            print(f"Scraping sur la partie {category}...")
            cpt = 0
            total = len(quest_links)
            for quest_link in quest_links:
                quest_url = construct_url(MAIN_SITE, quest_link)
                quest_soup = get_soup(quest_url)
                synopsis, objectives = get_quest_content(quest_soup)
                writer.writerow([quest_url, category, synopsis, objectives])
                cpt += 1
                print(f"{cpt}/{total} : {quest_link}")



if __name__ == "__main__":
    main()