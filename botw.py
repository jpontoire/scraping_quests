import csv
import requests
import re

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url, remove_fragment

SITE = "https://zelda-archive.fandom.com/wiki/Quest"

CATEGORIES = ["Main quests", "Side quests", "Shrine quests"]

def get_game_quests_links(title, soup):
    """Retourne la liste des balises <a> entre <h2>title</h2> et le <h2> suivant"""
    section = soup.find("span", {"class": "mw-headline"}, string=title)
    if not section:
        return None

    h2 = section.find_parent("h2")

    content = []
    for sibling in h2.find_next_siblings():
        if sibling.name == "h2" or "Spoiler" in sibling.text:
            break
        quests = sibling.scrape("tbody>tr>td:first-child a", "href")
        for quest in quests:
            content.append(quest)
    return content

def get_quest_content(soup):
    section = soup.find("span", {"class": "mw-headline"}, string="Overview")
    if not section:
        section = soup.find("span", {"class": "mw-headline"}, string="Objectives")
    content = []
    if section:
        h2 = section.find_parent("h2")
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2" or "Spoiler warning: Spoilers end here" in sibling.text:
                break
            if not "Spoiler warning" in sibling.text:
                content.append(str(sibling.get_text()))
        return "\n".join(content).strip()
    start_spoiler = soup.find("a", string=re.compile(r"Spoiler warning"))
    if start_spoiler:
        for sibling in start_spoiler.find_parent("div").find_next_siblings():
            if "Spoiler" in sibling.text:
                break
            content.append(str(sibling.get_text()))
        return "\n".join(content).strip()
    return None


def main():
    soup = get_soup(SITE)
    for category in CATEGORIES:
        print(f"Scraping sur la partie {category}...")
        quests = get_game_quests_links(category, soup)
        set_quests = set(quests)
        cpt = 0
        total = len(set_quests)
        with open(f"zelda_{category.replace(' ', '_').lower()}.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Quest URL", "Content"])
            for quest in set_quests:
                soup_quest = get_soup(construct_url("https://zelda-archive.fandom.com", quest))
                content = get_quest_content(soup_quest)
                writer.writerow([construct_url("https://zelda-archive.fandom.com", quest), content])
                cpt += 1
                print(f"{cpt}/{total} : {quest}")

                

if __name__ == "__main__":
    main()