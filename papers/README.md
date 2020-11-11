# Matthew Kenworthy's Papers

CAUTION: in `zsh` shell, wildcards have to be quoted to prevent local expansion

Pulling the PDFs from belterwijde:

    cd papers/
    rsync -rva kenworthy@belterwijde.strw.leidenuniv.nl:public_html/papers/\*.pdf .

Pushing papers to belterwijde:

    rsync -rva *.pdf kenworthy@belterwijde.strw.leidenuniv.nl:public_html/papers/.
