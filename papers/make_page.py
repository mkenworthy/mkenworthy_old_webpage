import os
import math
import requests
import argparse
import csv

import sys

'''make_page.py = parses a list of bibcodes from a file and then produces an HTML page
with the links to the papers, and if a bibcode.txt and bibcode.jpg|png file exists, add a side panel figure'''

# TODO shorten the names of the journals

html_out = 'index.html'

filenames = ['head.txt','tmp.html','tail.txt']

##https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
import logging
class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# create logger with 'spam_application'
logger = logging.getLogger("MAKE_PAGE")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

#logger.debug("debug message")
#logger.info("info message")
#logger.warning("warning message")
#logger.error("error message")
#logger.critical("critical message")

# write the htmlized paper list to this temporary file
outfile = open('tmp.html','w')


# https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence
def pickle_loader(filename):
    import pickle
    with open(filename, "rb") as f:
        obj = pickle.load(f)

    return obj

# https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence
def save_object(obj, filename):
    import pickle
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def authorlist(authors, nauthors=3):
    '''authorlist - pretty print list of authors for HTML'''
    st = ""
    if len(authors) < nauthors:
        return ", ".join(authors)

    return ", ".join(authors[:nauthors])+" et al."


def get_bibinfo(bibcode):

    # make filename
    fin = bib+'.pkl'

    # see if file exists
    if os.path.isfile(fin):
        # read in from the pickle
 #       print(f'pickle {fin} found, reading in...')
        res=pickle_loader(fin)
    else:
        # if no, download and save pickle
        import ads
        print(f'pickle file {fin} not found. Downloading from ADS...')
        bibcodes = [bibcode]
        articles = [list(ads.SearchQuery(bibcode=bibcode,fl=['author','id','year', 'bibcode', 'title', 'citation_count','id','page','volume','pub']))[0] for bibcode in bibcodes]
        res = articles[0]
        print(f'Downloaded. Saving to {fin}...')
        save_object(res, fin)

    return res

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r',
        '--read-from-file',
        dest='input_file',
        help='Read libraries from this file.',
        default='kenworthy_ads_lib.csv'
    )
    parser.add_argument(
        '-L',
        '--library',
        dest='ads_lib',
        help='Code for ADS library (usually alphanumeric string).',
        default='qGMnfKiwT_ydy8eoGu7esw'
    )
    args = parser.parse_args()
    input_file = args.input_file
    ads_lib = args.ads_lib

    with open(input_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')

        header=[]
        header = next(spamreader)
        data = next(spamreader)

    bibcodes = data[1].split("\t")

    for bib in bibcodes:
        ob = get_bibinfo(bib)

        url = f'https://home.strw.leidenuniv.nl/~kenworthy/papers/{ob.bibcode}.pdf'
#     journal = journal + f', {ob.page[0]} '
# TypeError: 'NoneType' object is not subscriptable
        journal = ""
        if hasattr(ob, 'pub'):
            journal = journal + f'{ob.pub}'
        if hasattr(ob, 'volume'):
            journal = journal + f', {ob.volume}'
        if hasattr(ob, 'page'):
            try:
                journal = journal + f', {ob.page[0]} '
            except:
                logger.warning(f'no page number for {bib}. Skipping page number insertion.')

        jourref = journal

        # if there's a file called bibcode.txt then read it in
        # check that bibcode.jpg exists
        # build up the html snippet
        if  os.path.isfile(bib+'.txt'):

            pin = 'not found'
            if os.path.isfile(bib+'.png'):
                pin = bib+'.png'
            if os.path.isfile(bib+'.jpg'):
                pin = bib+'.jpg'

            logger.info(f'Found {bib}.txt and found {pin} image\n\n')


            # read in text file to get maintxt and alttext
            fi = open(bib+'.txt',newline='\n')
            (xin) = fi.read().split('\n')
            alttxt, maintxt = xin[0], xin[1]

            fauth = ob.author[0].split(',')[0]

            urlbackref = f'<a href="https://home.strw.leidenuniv.nl/~kenworthy/papers/{bib}.pdf">{fauth} et al. ({ob.year})</a>'

            sidepanel = f'<p><label for="{bib}" class="margin-toggle">&#8853;</label><input type="checkbox" id="{bib}" class="margin-toggle"/><span class="marginnote"><img src="{pin}" alt="{alttxt}"/>{maintxt} {urlbackref}.</span></p>'

            outfile.write((sidepanel+"\n"))

        message = f'<p><a href="{url}">{ob.title[0]}</a><br /> {authorlist(ob.author)} ({ob.year})<br /> {journal} <a href="https://ui.adsabs.harvard.edu/abs/{ob.bibcode}">[ADS]</a></p>'
        outfile.write(message+"\n\n")


# put them all together


# write out the html page using filenames defined at the top!
with open(html_out, 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())

