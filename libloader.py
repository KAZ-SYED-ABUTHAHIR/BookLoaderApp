# !/usr/bin/python
# -*- coding: <utf-8> -*-

"""libloader.py: A CLI Interface to download LibGen files"""

__author__ = "NOBODY"
__copyright__ = "NOBODY"

import downloader as dlr  # local module
import soupipy

import os, sys, time, winsound
import pyperclip as clip
import requests
from bs4 import BeautifulSoup as bsp
from typing import List, Dict, Tuple

# ------------------------------------------------System & PC Bell Sound--------------------------------------------------------#
def ringBell(bell='BEEP') -> None:
    """ Function to ring the system bell '\a' is the escape sequence for the bell"""
    if bell == 'BEEP':
        winsound.Beep(2500, 100)
        return
    elif bell == 'SYS_SOUND':
        sys.stdout.write('\a')
        sys.stdout.flush()
        return


# -----------------------------------------------------------------------------------------------------------------------------------------------#
def startCoverRenderer() -> None:
    """ Function to start the cover rendering app at the beginning"""
    cwdSaved = os.getcwd()
    os.chdir(r"bin")
    os.system(r"ShowCoverImage.exe")
    os.chdir(cwdSaved)
    return


# ------------------------------------------------------Display Cover Image-------- -------------------------------------------------------------#
def renderCoverImage(url: str = None) -> None:
    """
		Func to display the cover image.The task of displaying the image from the url is delegated to 
		the processing micro app through the file
	"""

    if not url:
        return None
    try:
        with open(r"bin\data\coverURL.txt", "w") as txtfl:
            txtfl.write(url)
    except Exception as e:
        print(e)
        return None


    # ---------------------------------------------------------------------------------------------------------------------------------------#
def exitCoverRenderer() -> None:
    try:
        with open(r"bin\data\commands.txt", "w") as txtfl:
            txtfl.write('EXIT')
    except Exception as e:
        print(e)
    time.sleep(1)
    try:
        with open(r"bin\data\commands.txt", "w") as txtfl:
            txtfl.write('START')
    except Exception as e:
        print(e)


# ---------------------------------------------Function to get user base path attached to a dir name-------------
def getUserBasePath(appendPath = ''):
    return os.path.expanduser('~') + "\\" + appendPath + "\\"
    
# -----------------------------------------------------------------------------------------------------------------------------------------------#
def searchSoup(search: str, page='1', view='detailed', column='def', sortby='year', sortmode='DESC') -> bsp:
    """
		Function to construct the url string and to get the soup out of it, returns a bsp object.
	"""
    searchStr = search.strip().replace(' ', '+')
    urlString = 'http://93.174.95.27/search.php?&req={}&phrase=1&view={}&column={}&sort={}&sortmode={}&page={}'.format(
        searchStr, view, column, sortby, sortmode, page)
    soup = None
    MAX_NUM_TRYS = 15
    i = 0
    while (soup is None):
        try:
            soup = soupipy.getSoup(urlString)
            i += 1
            # print('\rTrying {}'.format(i),end='')
            if i > MAX_NUM_TRYS:
                break
        except Exception as e:
            print(e)
    return soup


# -----------------------------------------------------------------------------------------------------------------------------------------------#
def catchErr(fun, *args, **kwargs):
    """Function to catch RTErrs raised from list comprehensions"""
    try:
        return fun(*args, **kwargs)
    except:
        return None


# -----------------------------------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------Main Function-------------------------------------------------------------------------------#
def main():
    # Auxiliary Function To Extract Juice From A Book Search Page
    def getPageJuice(search='None', pageNum='1') -> List[Dict]:
        """
    	Extract Page Details for the page <pageNum> corresponding to the search string <search> and
    	returns the extracted details for each book as a list of dictionaries
    	"""
        soup = searchSoup(search, pageNum)

        try:
            imgs = soup.findAll('img')
            srcs = [img['src'] for img in imgs]
            refstobookget = ['http://93.174.95.29/main/' + img.parent['href'].split('=', 1)[1] for img in imgs]
            bkldpgsoups = soupipy.getSoups(refstobookget)
            loaderURIs = [bkldpgsoup.findAll('a', text='GET')[:][0]['href'] for bkldpgsoup in bkldpgsoups]
        except Exception as e:
            print(e)

        NUM_RECORDS = len(loaderURIs)
        print('{} Books Found.'.format(NUM_RECORDS))

        NON_EXISTING = -1
        imgsrcuris = ['http://93.174.95.27' + src if src.find('https') is NON_EXISTING else src.split('/covers/', 1)[1] for
                      src in srcs]

        bibtexjsonsresultset = soup.findAll('a', text='Link')
        bibtexjsons = ['http://93.174.95.27' + bibtexjson['href'] for bibtexjson in bibtexjsonsresultset]

        bibtexjsonsoups = soupipy.getSoups(bibtexjsons)
        bibtexjsonsoupsnuts = [bibtexjsonsoup.textarea.text.split('\n', 1)[1:][-1][:-1] for bibtexjsonsoup in
                               bibtexjsonsoups]

        sizes = soup.findAll('td', text='Size:')
        FILE_SIZE = 0
        EXTENSION = 2
        sizesexts = [(size.findNextSiblings()[FILE_SIZE].text, size.findNextSiblings()[EXTENSION].text) for size in
                     sizes]  # Extracting sizes and extensions

        pgnums = [pg.findNextSiblings()[0].text for pg in soup.findAll('td', text='Pages:')]

        FILE_SIZE = 0
        EXTENSION = 1

        """
    	"""
        bibtexjsonsoupsnuts = [('   ' + bibtexjsonsoupsnut.strip() +
                                ',\n   size =      {},\n   extension = {},\n   pages =     {}'.
                                format('{' + sizesexts[i][FILE_SIZE] + '}', '{' + sizesexts[i][EXTENSION] + '}',
                                       '{' + pgnums[i]) + '}').split(',') \
                               for i, bibtexjsonsoupsnut in enumerate(bibtexjsonsoupsnuts)]
        """
    	"""
        bibtexjsonsoupsnuts = [''.join(bibtexjsonsoupsnut).replace('=', '', 1) for bibtexjsonsoupsnut in bibtexjsonsoupsnuts]

        pageJuice = []

        TITLE = 0
        AUTHOR = 1
        PUBLISHER = 2
        ISBN = 3
        YEAR = 4
        SERIES = 5
        EDITION = 6
        VOLUME = 7
        URL = 8
        SIZE = 9
        EXTENSION = 10
        PAGES = 11

        for i, bibtexjsonsoupsnut in enumerate(bibtexjsonsoupsnuts):
            record = [element[element.index('{') + 1:].strip('}') for element in bibtexjsonsoupsnut.split('\n')]
            dictRecord = {}
            dictRecord['Title'] = record[TITLE]
            dictRecord['Author'] = record[AUTHOR]
            dictRecord['Pubisher'] = record[PUBLISHER]
            dictRecord['ISBN'] = record[ISBN]
            dictRecord['Year'] = record[YEAR]
            dictRecord['Series'] = record[SERIES]
            dictRecord['Edition'] = record[EDITION]
            dictRecord['Volume'] = record[VOLUME]
            dictRecord['URL'] = record[URL]
            dictRecord['Size'] = record[SIZE]
            dictRecord['Extension'] = record[EXTENSION]
            dictRecord['Pages'] = record[PAGES]
            dictRecord['Image URL'] = imgsrcuris[i]
            dictRecord['Book URL'] = loaderURIs[i]
            pageJuice.append(dictRecord)

        spdlinksoups = [soupipy.getSoup(spdlnkget['URL'].replace('http://gen.lib.rus.ec/book/index', 'https://libgen.lc/ads')) for
                        spdlnkget in pageJuice]
        bookdscrns = [str(spdlinksoup).split('<td colspan="2">')[-1].split('</td>')[0].replace('<br/>', ' ') + '\n' for
                      spdlinksoup in spdlinksoups]
        bookdscrns = [bookdscrn if bookdscrn.find('<html/>') == -1 else 'Not Found' for
                      bookdscrn in bookdscrns]

        spdlnkgeturls = [catchErr(lambda: spdlinksoup.findAll('a', text='GET')[:][0]['href']) for spdlinksoup in
                         spdlinksoups]

        for pgJce, spdlnkgeturl, bookdscrn in zip(pageJuice, spdlnkgeturls, bookdscrns):
            pgJce['Book URL(Faster)'], pgJce['Book Description'] = spdlnkgeturl, bookdscrn
             

        return pageJuice, NUM_RECORDS


    startCoverRenderer()

    searchfor = input('What Do You Like To Search For?(Search By Title,Author,Pubisher,ISBN and Tags): ')
    pgnum = input('Enter the Page Number To Search: ')

    print('Juicing......Kindly Wait')

    pgJce, _ = getPageJuice(searchfor, pgnum)

    for book in pgJce:
        imgurl = book['Image URL']

        if book['Book URL(Faster)'] is not None:
            bookurl = book['Book URL(Faster)']
        else:
            bookurl = book['Book URL']

        name = book['Title']
        author = book['Author']
        numOfPgs = book['Pages']
        year = book['Year']
        size = book['Size']
        extension = book['Extension']
        description = book['Book Description']

        renderCoverImage(imgurl)

        print('\nDo you want to download this book?')

        print('Title 		   : {}'.format(name))
        print('Author 		   : {}'.format(author))
        print('Number of Pages    : {}'.format(numOfPgs))
        print('Year               : {}'.format(year))
        print('Size  		   : {}'.format(size))
        print('Extention	   : {}'.format(extension))
        print('Description        : {}'.format(description))
        print()

        clip.copy(author) # Author name is copied to the system clipboard 

        choice = input('Y/N : ')
        if choice in ['Y', 'y']:
            sizeinbytes = int(size.split('(')[1].rstrip(')'))
            print('\nDownloading: {} \n'.format(name + '.' + extension))
            dlr.downloadFile(bookurl, sizeinbytes, getUserBasePath(appendPath='Desktop'), name, extension, barStyle='BAR')
            ringBell()
        else:
            continue

    exitCoverRenderer()


# -----------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    main()

