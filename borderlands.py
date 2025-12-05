import csv
import requests
import re

from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, construct_url, remove_fragment

MAIN_SITE = "https://borderlands.fandom.com"

SITE_1 = "https://borderlands.fandom.com/wiki/Borderlands_missions_flow"
SITE_2 = "https://borderlands.fandom.com/wiki/Borderlands_2_mission_flow"
SITE_3 = "https://borderlands.fandom.com/wiki/Borderlands_3_mission_flow"


def get_quest_content(soup):
    background = soup.find("span", {"class": "mw-headline"}, string="Background")
    content = []
    if background:
        h2 = background.find_parent("h2")
        if h2:
            for sibling in h2.find_next_siblings():
                if sibling.name == "h2":
                    break
                content.append(str(sibling.get_text()))
    
    walkthrough = soup.find("span", {"class": "mw-headline"}, string="Walkthrough")
    obj = []
    if walkthrough:
        h2 = walkthrough.find_parent("h2")
        if h2:
            for sibling in h2.find_next_siblings():
                if sibling.name == "h2":
                    break
                obj.append(str(sibling.get_text()))

    return "\n".join(content).strip(), "\n".join(obj).strip()


def main():
    with open("borderlands_missions.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Mission URL", "Type", "Background", "Walkthrough", "Game"])
        for site in [SITE_1, SITE_2, SITE_3]:

            game = site.split("/")[-1].split("_")[0:2]
            if "missions" in game:
                game.remove("missions")
            game = "_".join(game)
            
            soup = get_soup(site)
            main_links = soup.scrape("ol>li>b>a", "href")
            side_links = soup.scrape("ol>li i>a", "href")
                
            cpt = 0
            len_main = len(main_links)
            len_side = len(side_links)
            for link in main_links:
                mission_url = construct_url(MAIN_SITE, link)
                mission_soup = get_soup(mission_url)

                overview, objectives = get_quest_content(mission_soup)

                writer.writerow([mission_url, "Main", overview, objectives, game])
                cpt += 1
                print(f"Scraped {cpt}/{len_main} main missions", end="\r")
            cpt = 0
            for link in side_links:
                mission_url = construct_url(MAIN_SITE, link)
                mission_soup = get_soup(mission_url)
                overview, objectives = get_quest_content(mission_soup)
                writer.writerow([mission_url, "Side", overview, objectives, game])
                cpt += 1
                print(f"Scraped {cpt}/{len_side} side missions", end="\r")
    
    




















if __name__ == "__main__":
    main()