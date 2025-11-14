import csv
import requests
import re

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url, remove_fragment

MAIN_SITE = "https://witcher.fandom.com/wiki/The_Witcher_3_main_quests"

SECONDARY_SITE = "https://witcher.fandom.com/wiki/The_Witcher_3_secondary_quests"

CONTRACTS_SITE = "https://witcher.fandom.com/wiki/The_Witcher_3_contracts"

TREASURE_HUNTS_SITE = "https://witcher.fandom.com/wiki/The_Witcher_3_treasure_hunts"

HEARTS_OF_STONE_SITE = "https://witcher.fandom.com/wiki/Hearts_of_Stone_quests"

BLOOD_AND_WINE_SITE = "https://witcher.fandom.com/wiki/Blood_and_Wine_quests"


MAIN_SECTIONS = ["Prologue", "Act_I", "Act_II", "Act_III"]

SECONDARY_SECTIONS = ["Multiple_Regions", "White_Orchard", "Velen", "Novigrad", "Skellige", "Kaer_Morhen"]

CONTRACTS_SECTIONS = ["White_Orchard", "Velen", "Novigrad", "Skellige"]

TREASURE_HUNTS_SECTIONS = ["White_Orchard", "Velen", "Novigrad", "Skellige", "Kaer_Morhen"]

HEART_OF_STONE_SECTIONS = ["Main_quests", "Secondary_quests", "Treasure_hunts"]

BLOOD_AND_WINE_SECTIONS = ["Main_quests", "Secondary_quests", "Contracts", "Treasure_hunts"]

LIST_SITES = [MAIN_SITE, SECONDARY_SITE, CONTRACTS_SITE, TREASURE_HUNTS_SITE, HEARTS_OF_STONE_SITE, BLOOD_AND_WINE_SITE]

dict_witcher = {MAIN_SITE: MAIN_SECTIONS,
                SECONDARY_SITE: SECONDARY_SECTIONS,
                CONTRACTS_SITE: CONTRACTS_SECTIONS,
                TREASURE_HUNTS_SITE: TREASURE_HUNTS_SECTIONS,
                HEARTS_OF_STONE_SITE: HEART_OF_STONE_SECTIONS,
                BLOOD_AND_WINE_SITE: BLOOD_AND_WINE_SECTIONS}

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

def get_quest_content(soup):
    section = soup.find("span", {"class": "mw-headline"}, string="Walkthrough")

    content = []
    if section:
        h2 = section.find_parent("h2")
        if h2:
            for sibling in h2.find_next_siblings():
                if sibling.name == "h2":
                    break
                content.append(str(sibling.get_text()))
        else:
            h3 = section.find_parent("h3")
            for sibling in h3.find_next_siblings():
                if sibling.name == "h3":
                    break
                content.append(str(sibling.get_text()))
    
    objectives = soup.find("span", {"class": "mw-headline"}, string="Objectives")
    obj = []
    if objectives:
        h2 = objectives.find_parent("h2")
        if h2:
            for sibling in h2.find_next_siblings():
                if sibling.name == "h2":
                    break
                obj.append(str(sibling.get_text()))
        else:
            h3 = objectives.find_parent("h3")
            for sibling in h3.find_next_siblings():
                if sibling.name == "h3":
                    break
                obj.append(str(sibling.get_text()))

    return "\n".join(content).strip(), "\n".join(obj).strip()


def main():
    with open("witcher_quests.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Quest URL", "Category", "Walkthrough", "Objectives"])
        for site in LIST_SITES:
            print(f"Scraping sur le site {site}...")
            soup = get_soup(site)
            sections = dict_witcher[site]
            for category in sections:
                quest_links = get_game_quests_links(category, soup)
                print(f"Scraping sur la partie {category}...")
                cpt = 0
                total = len(quest_links)
                for quest_link in quest_links:
                    quest_url = construct_url(site, quest_link)
                    quest_soup = get_soup(quest_url)
                    walkthrough, objectives = get_quest_content(quest_soup)
                    writer.writerow([quest_url, category, walkthrough, objectives])
                    cpt += 1
                    print(f"  - Progress: {cpt}/{total}")


# def main():
#     soup = get_soup("https://witcher.fandom.com/wiki/Something_Ends,_Something_Begins_(quest)")
#     walkthrough, objectives = get_quest_content(soup)
#     print("WALKTHROUGH\n")
#     print(walkthrough)
#     print("\nOBJECTIVES\n")
#     print(objectives)



if __name__ == "__main__":
    main()