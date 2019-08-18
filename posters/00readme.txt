# Convert PDFS to thumbnail images and large jpg

# make thumbnails
for i in *.pdf; do convert $i -resize 600x ${i%.pdf}_small.jpg;done

# make high res jpegs
for i in *.pdf; do convert $i -resize x2000 ${i%.pdf}.jpg;done

# make the HTML for the web page
# run
python make_html_for_webpage.py > tmp
