import csv
import requests
import re

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url, remove_fragment

SITE = "https://reddead.fandom.com/wiki/Missions_in_Redemption_2"

SECTIONS = ["Chapter_1:_Colter", "Chapter_2:_Horseshoe_Overlook", "Chapter_3:_Clemens_Point", "Chapter_4:_Saint_Denis", "Chapter_5:_Guarma", "Chapter_6:_Beaver_Hollow", "Epilogue,_Part_1:_Pronghorn_Ranch", "Epilogue,_Part_2:_Beecher's_Hope", "Stranger_Side_Missions", ]

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
        quests = sibling.scrape("li>a", "href")
        for quest in quests:
            content.append(quest)
    return content







def get_quest_content(soup):
    overview = soup.find("span", {"class": "mw-headline"}, string="Mission Overview")
    if not overview:
        overview = soup.find("span", {"class": "mw-headline"}, string="Description")
    content = []
    if overview:
        h2 = overview.find_parent("h2")
        if h2:
            for sibling in h2.find_next_siblings():
                if sibling.name == "h2":
                    break
                content.append(str(sibling.get_text()))
        else:
            h3 = overview.find_parent("h3")
            for sibling in h3.find_next_siblings():
                if sibling.name == "h3":
                    break
                content.append(str(sibling.get_text()))
    
    story = soup.find("span", {"class": "mw-headline"}, string="Story")
    if not story:
        story = soup.find("span", {"class": "mw-headline"}, string="Walkthrough")
    obj = []
    if story:
        h2 = story.find_parent("h2")
        if h2:
            for sibling in h2.find_next_siblings():
                if sibling.name == "h2":
                    break
                obj.append(str(sibling.get_text()))
        else:
            h3 = story.find_parent("h3")
            for sibling in h3.find_next_siblings():
                if sibling.name == "h3":
                    break
                obj.append(str(sibling.get_text()))

    return "\n".join(content).strip(), "\n".join(obj).strip()


def main():
    soup = get_soup(SITE)
    with open("RDR2_missions.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Mission URL", "Category", "Overview", "Story/Walkthrough"])
        for section in SECTIONS:
            print(f"Scraping la section {section}...")
            quests_links = get_game_quests_links(section, soup)
            if not quests_links:
                continue
            for quest_link in quests_links:
                quest_url = urljoin(SITE, quest_link)
                print(f"  Scraping la mission {quest_url}...")
                quest_soup = get_soup(quest_url)
                overview, story = get_quest_content(quest_soup)
                writer.writerow([quest_url, section, overview, story])



if __name__ == "__main__":
    main()