# make_html_for_webpage
# M. Kenworthy kenworthy@strw.leidenuinv.nl 2019 aug 18
#
# reads in one line from list_of_pdfs and generates HTML suitable for tufte.css styles so that you can cut and paste into index.html
#
# rearrange lines in text file to match desired order in HTML

lin = open('list_of_pdfs.txt')

for curr in lin:
    words = curr.split()
    fname = words[0]
    descript = ' '.join(words[1:])
    print('<figure><label for="mn-{}" class="margin-toggle">&#8853;</label><input type="checkbox" id="mn-{}" class="margin-toggle"/><span class="marginnote">{}</span><a href="{}"><img src="{}" /></a></figure>'.format(fname.replace('.pdf',''),fname.replace('.pdf',''),descript,fname,fname.replace('.pdf','_small.jpg')))
