**First, I'll admit that this took me a bit longer than 2-3 hours.** The clock got away from me and it was fun! I've never written an API in Python or JavaScript before, so I spent a lot of time researching options, reading tutorials, getting annoyed and bouncing to another option, etc. Eventually I settled on a simple Flask app based on [this tutorial](https://www.youtube.com/watch?v=GMppyAPbLYk). I figured I'd take a bit longer, teach myself something new, and get closer to feature-completion, instead of sending you a half-baked program that doesn't function after exactly 3 hours. I hope that's alright; I understand if it's not.

### What I got done:

- ✅ user can post JSON (that matches the given schema in the example) to your API endpoint
- ✅ application parses the JSON and saves it to the database
	- ✅ JSON containing a unique ​id​ and a unique ​canonical_url​ is added to the database as a new entry
	- ✅ JSON containing ​id​ and ​canonical_url​ values that match an existing entry is handled as an update to an existing entry with the new content

### Known issues:
- it's all one big file (blech!)
- Article `published_date` table column is a String type when it should be DateTime
- similarly, Article `tags` are a String. Tags could probably be their own model in a many-to-many relationship
- models related to Article - embeds, lead art, authors - do not serialize properly.
	- I can get the embed and author objects, displayed in a list, and I can show the lead art's ID (those are all included in GET requests) but I can't quite figure out how to transform those related things back into JSON with @marshal_with
- `null` issue: sending the sample JSON, where `"embeds": null`, via Postman works totally fine. however, sending it via the included `test.py` file hits an error because "null" is an undefined variable. not sure why that is, some Python quirk
- this probably the least DRY code ever written in the history of computer science