

curl -H 'Authorization: Bearer <token>' 'https://api.adsabs.harvard.edu/v1/search/query?q=star'

curl -H 'Authorization: Bearer HZeLrdZnKSQxw1xHbiPYM9QgYNl2WL3ZcnVV2GtC' 'https://api.adsabs.harvard.edu/v1/search/query?q=star'

HZeLrdZnKSQxw1xHbiPYM9QgYNl2WL3ZcnVV2GtC


qGMnfKiwT_ydy8eoGu7esw

curl -H "Authorization: Bearer HZeLrdZnKSQxw1xHbiPYM9QgYNl2WL3ZcnVV2GtC" https://api.adsabs.harvard.edu/v1/biblib/libraries/qGMnfKiwT_ydy8eoGu7esw | python -m json.tool


r = requests.get("https://api.adsabs.harvard.edu/v1/biblib/libraries/qGMnfKiwT_ydy8eoGu7esw", \
                 headers={"Authorization": "Bearer HZeLrdZnKSQxw1xHbiPYM9QgYNl2WL3ZcnVV2GtC"})
print(r.json())
