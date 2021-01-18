import requests
import json

BASE_URL = "http://localhost:5000/"
null = []

article1 = { "article": {
  "id": "b73b8b0e-0240-42a9-874c-00445d51dd8a",
  "slug": "tracee-ellis-ross-on-hollywood-girlfriends-netflix",
  "title": "Tracee Ellis Ross Felt Lost in Hollywood. Then She Changed Course.",
  "dek": "The <em>Black-ish </em>star and Emmy nominee figured she’d made it when she scored the lead role in the early-2000s sitcom <em>Girlfriends</em>. But it would be 14 more years before she hit her stride.",
  "published_date": "2020-08-30T10:00:00Z",
  "canonical_url": "/culture/archive/2020/08/tracee-ellis-ross-on-hollywood-girlfriends-netflix/615754/",
  "word_count": 2068,
  "tags": "",
  "embeds": null,
  "lead_art": {
      "id": "1526857",
      "type": "image_large"
  },
  "authors": [
      {
          "id": "7313",
          "slug": "shirley-li"
      },
      {
          "id": "3453",
          "slug": "lafrance-adrienne"
      }
  ]
}}

article2 = { "article": {
  "id": "TEST-1234",
  "slug": "test-slug-9000",
  "title": "I'm Testing",
  "dek": "welcome to test land",
  "published_date": "2020-08-30T10:00:00Z",
  "canonical_url": "/url/to/thing",
  "word_count": 666,
  "tags": "test tag",
  "embeds": [
      {"id": 99999},
      {"id": 13}
  ],
  "authors":[
      {
        "id": "6",
        "slug": "brian-feldman"
      },
      {
        "id": "3453",
        "slug": "lafrance-adrienne"
      }
  ],
  "lead_art": {
      "id": "1526857",
      "type": "image_large"
    }
}}

article1 = json.dumps(article1, indent = 2)
article2 = json.dumps(article2)

response1 = requests.put(BASE_URL + "article", article1, headers = {"Content-Type": "application/json"})
response2 = requests.put(BASE_URL + "article", article2, headers = {"Content-Type": "application/json"})
print("ARTICLE 1:", response1.text)
print("ARTICLE 2:", response2.text)
