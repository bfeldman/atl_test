import requests

BASE_URL = "http://localhost:5000/"

article = {
    "id": "b73b8b0e-0240-42a9-874c-00445d51dd8a",
    "slug": "tracee-ellis-ross-on-hollywood-girlfriends-netflix",
    "title": "Tracee Ellis Ross Felt Lost in Hollywood. Then She Changed Course.",
    "dek": "The <em>Black-ish </em>star and Emmy nominee figured she’d made it when she scored the lead role in the early-2000s sitcom <em>Girlfriends</em>. But it would be 14 more years before she hit her stride.",
    #"published_date": "2020-08-30T10:00:00Z",
    "canonical_url": "/culture/archive/2020/08/tracee-ellis-ross-on-hollywood-girlfriends-netflix/615754/",
    "word_count": 2068,
    "tags": "",
  } 


#print(article['id'])
print(BASE_URL + "article/" + article['id'])
response = requests.put(BASE_URL + "article/" + article['id'], article)
print(response)

# input()
# 
# response = requests.get(BASE_URL + "article/2")
# print(response.json())