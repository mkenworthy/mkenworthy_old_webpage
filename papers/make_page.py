
import os
import math
import requests
import argparse
import csv


#url = "https://home.strw.leidenuniv.nl/~kenworthy/papers/2021ExA...tmp..124S.pdf"
#title = "Detecting life"
#author = "Snellen, I. A. G., Snik, F., Kenworthy, M., et al."
#year = "2021"
#jourref = "ExA...tmp"
#adsurl = "https://ui.adsabs.harvard.edu/abs/2021ExA...tmp..124S"


#sample = """
#    <p><a href="{0}">{1}</a><br /> {2} ({3})<br /> {4}, <a href="{5}">[ADS]</a></p>
#        """.format(url, title, author, year, jourref, adsurl)

# Using triple quotes will give you unwanted indentation. To align your indentation,
# you can use textwrap module from pythons stdlib
import textwrap
#sample = textwrap.dedent(sample)

#print(sample)

#message = f'<p><a href="{url}">{title}</a><br /> {author} ({year})<br /> {jourref}, <a href="{adsurl}">[ADS]</a></p>'
#print(message)

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



def get_bibinfo(bibcode):

    # make filename
    fin = bib+'.pkl'

    # see if file exists
    if os.path.isfile(fin):
        # read in from the pickle
        print(f'pickle {fin} found, reading in...')
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

    for bib in bibcodes[10:14]:
        print(bib)
        ob = get_bibinfo(bib)

        url = f'https://home.strw.leidenuniv.nl/~kenworthy/papers/{ob.bibcode}.pdf'

        journal = ""
        if hasattr(ob, 'pub'):
            journal = journal + f'{ob.pub} '
        if hasattr(ob, 'volume'):
            journal = journal + f'{ob.volume} '
        if hasattr(ob, 'page'):
            journal = journal + f'{ob.page}, '

        jourref = journal
        print(ob.year)

        message = f'<p><a href="{url}">{ob.title[0]}</a><br /> {ob.author} ({ob.year})<br /> {journal}<a href="https://ui.adsabs.harvard.edu/abs/{ob.bibcode}">[ADS]</a></p>'
        print(message)
