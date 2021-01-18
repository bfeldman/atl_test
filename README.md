## Database schema

- Models:
	- ArticleModel
		- `id` (string)
		- `slug` (string)
		- `title` (string)
		- `dek` (string)
		- `published_date` (string)
		- `canonical_url` (string)
		- `word_count` (integer)
		- `tags` (string)
		- `lead_art` (integer, foreign key)
	- AuthorModel
		- `id` (integer)
		- `slug` (string)
		- many-to-many relationship with ArticleModel through join table
	- LeadArtModel
		- `id` (integer)
		- `type` (string)
		- one to many relationship with ArticleModel, as in: one lead art can be used on many articles)
	- EmbedModel
		- `id` (integer)
		- many-to-many relationship with ArticleModel through join table
- Join tables
	- Embeds
	- Authors

## Setup instructions
- navigate to the program's folder
	- (if they're still there, you can delete the `env` folder and `database.db` files to start fresh. i've included them strictly for transparency)
- from the command line, type `python3 -m venv env` to create a virtual environment
- activate the virtual environment by typing `source env/bin/activate`
- install the required packages from pip by typing `pip install -r requirements.txt`

Creating the db:
- make sure line 68 in `main.py` is uncommented (this creates the SQLite database) and run `python main.py` to start the server
	- you only need to do this once! if you stop the server and run `main.py` again, comment out line 68 so that it doesn't keep creating the db over and over

Making calls
- while the server is running, you can run `python test.py` to make a couple of test calls to the API
	- `BASE_URL` is `localhost:5000`. change this variable if your server is running on a different port
- to write to the db, send correctly formatted JSON in a `PUT` request to the `/article` endpoint
- to read JSON from the DB, include the article's ID in the URL like so and send a `GET` response like so: `http://localhost:5000/article/b73b8b0e-0240-42a9-874c-00445d51dd8a`