# Matthew Kenworthy's Papers

CAUTION: in `zsh` shell, wildcards have to be quoted to prevent local expansion

Pulling the PDFs from belterwijde:

    cd papers/
    rsync -rva kenworthy@belterwijde.strw.leidenuniv.nl:public_html/papers/\*.pdf .

Pushing papers to belterwijde:

    rsync -rva *.pdf kenworthy@belterwijde.strw.leidenuniv.nl:public_html/papers/.

## Building database

Building the database from an ADS library that are already generated:

    python lib_2_csv.py

This generates a list of the ADS bibcodes from the default library specified in the above script:

    kenworthy_ads_lib.csv

Generate the `index.html` with:

    python make_page.py

## Converting from the old format

Making the page using `python make_page.py`

awk -F '\t' '{ print "cp " $1 " \047" $4".jpg\047" }' < allimgs.txt > jpgs.sh

awk -F '\t' '{ print "echo \"" $2"\\n" $3 "\" >\047" $4.".txt\047" }' < allimgs.txt > run.sh

