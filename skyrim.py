from ural import is_url
from urllib.parse import urljoin

from minet.web import request, create_pool_manager, Response
from minet.scrape import WonderfulSoup, Tag

from utils import get_soup, get_html, get_quests_box


SITE = "https://en.uesp.net/wiki/Skyrim:Skyrim"

def get_quests():
    """Get list of quests from Skyrim UESP page."""
    soup = get_soup(SITE)
    print(get_quests_box(soup))
    return


def main():
    get_quests()
    return

if __name__ == "__main__":
    main()