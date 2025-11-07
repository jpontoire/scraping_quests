import csv
import requests
import re

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url, remove_fragment

MAIN_SITE = "https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Main_Jobs"

SIDE_SITE = "https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Side_Jobs"

MINOR_SITE = "https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Minor_Jobs"

SITE = [MAIN_SITE, SIDE_SITE, MINOR_SITE]

MAIN_CATEGORIES = ["Prologue", "Act_1", "Interlude", "Act_2", "Act_3", "Epilogue", "Phantom_Liberty"]

SIDE_CATEGORIES = ["Romances", "Story_Characters"]

MINOR_CATEGORIES = ["Cyberpunk_2077", "Phantom_Liberty"]

PAGE_CATEGORIES = {MAIN_SITE: MAIN_CATEGORIES, SIDE_SITE: SIDE_CATEGORIES, MINOR_SITE: MINOR_CATEGORIES}

QUEST_PARTS = ["Walkthrough", "Objectives"]

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
        quests = sibling.scrape("td:nth-child(2) a", "href")
        for quest in quests:
            content.append(quest)
    return content

def get_quest_content(part, soup):
    section = soup.find("span", {"class": "mw-headline"}, string=f"{part}")
    content = []
    if section:
        h2 = section.find_parent("h2")
        for sibling in h2.find_next_siblings():
            if sibling.name == "h2":
                break
            content.append(str(sibling.get_text()))
        return "\n".join(content).strip()
    return None


def main():
    for site in SITE:
        print(f"Scraping sur {site}...")
        with open(f"DATA/cyberpunk_{site.split('_')[-2]}_quests.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Quest Name", "Category", "Walkthrough", "Objectives"])
            soup = get_soup(site)
            for category in PAGE_CATEGORIES[site]:
                print(f"Scraping sur la partie {category}...")
                quests = get_game_quests_links(category, soup)
                set_quests = set(quests)
                cpt = 0
                total = len(set_quests)
                for quest in set_quests:
                    quest_soup = get_soup(construct_url("https://cyberpunk.fandom.com", quest))
                    walkthrough = get_quest_content("Walkthrough", quest_soup)
                    objectives = get_quest_content("Objectives", quest_soup)
                    quest_name = quest.split("/")[-1]
                    writer.writerow([quest_name, category, walkthrough, objectives])
                    cpt += 1
                    print(f"{cpt}/{total} : {quest_name}")


if __name__ == "__main__":
    main()