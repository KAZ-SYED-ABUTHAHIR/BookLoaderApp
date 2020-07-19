"""
Module containgin functions to extract soup from web pages.
"""
import requests
from bs4 import BeautifulSoup as bsp

# -----------------------------------------------------------------------------------------------------------------------------------------------#
def getSoup(url: str, ftrs: str = "html5lib") -> bsp:
    """
	Function to extract soup from the url passed in, returns a bsp object.
	"""
    rspns = requests.get(url)
    return bsp(rspns.content, ftrs)


# ----------------------------------------------------------------------------------------------------------------------------------------------#
def getSoups(urls: list, ftrs: str = "html5lib") -> list:
    """
		Function to extract soups from the list of urls passed in, returns a list of bsp objects.
	"""
    rspnss = [getSoup(url, ftrs) for url in urls]
    return rspnss