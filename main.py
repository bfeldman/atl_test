from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#JOIN TABLES
embed_table = db.Table('embeds',
  db.Column('embed_id', db.Integer, db.ForeignKey('embed_model.id'), primary_key=True),
  db.Column('article_id', db.Integer, db.ForeignKey('article_model.id'), primary_key=True)
)

author_table = db.Table('authors',
  db.Column('author_id', db.Integer, db.ForeignKey('author_model.id'), primary_key=True),
  db.Column('article_id', db.Integer, db.ForeignKey('article_model.id'), primary_key=True)
)

#embed model (many-to-many)
class EmbedModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  def __repr__(self):
    return '<Embed %r>' %self.id

#author model (many-to-many)
class AuthorModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  slug = db.Column(db.String, nullable=True)
  
  def __repr__(self):
    return '<Author %r>' %self.id
    
# article model
class ArticleModel(db.Model):
  id = db.Column(db.String, primary_key=True)
  slug = db.Column(db.String, nullable=True)
  title = db.Column(db.String, nullable=True)
  dek = db.Column(db.String, nullable=True)
  published_date = db.Column(db.String, nullable=True)
  canonical_url = db.Column(db.String, nullable=True)
  word_count = db.Column(db.Integer, nullable=True)
  tags = db.Column(db.String, nullable=True)
  #relationships
  lead_art = db.Column(db.Integer, db.ForeignKey('lead_art_model.id'), nullable=True)
  embeds = db.relationship('EmbedModel', secondary=embed_table, lazy='subquery', backref=db.backref('articles', lazy=True))
  authors = db.relationship('AuthorModel', secondary=author_table, lazy='subquery', backref=db.backref('articles', lazy=True))
  
  def __repr__(self):
    return '<Article %r>' %self.id
    
#lead art model (one-to-many relationship) 
class LeadArtModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String, nullable=True)
  articles = db.relationship('Article', backref=db.backref('user', lazy='joined'), lazy='dynamic'),
  def __repr__(self):
    return '<LeadArt %r>' %self.id



db.create_all()

article_put_args = reqparse.RequestParser()
article_put_args.add_argument("id", type=str, required=True)
article_put_args.add_argument("slug", type=str, required=True)
article_put_args.add_argument("title", type=str)
article_put_args.add_argument("dek", type=str)
article_put_args.add_argument("published_date", type=str)
article_put_args.add_argument("canonical_url", type=str)
article_put_args.add_argument("word_count", type=int)
article_put_args.add_argument("tags", type=str)
article_put_args.add_argument("embeds", type=list)
article_put_args.add_argument("lead_art", type=dict)
article_put_args.add_argument("authors", type=list)


resource_fields = { "article" : {
  'id': fields.String,
  'slug': fields.String,
  'title': fields.String,
  'dek': fields.String,
  'published_date': fields.String,
  'canonical_url': fields.String,
  'word_count': fields.Integer,
  'tags': fields.String
  }
}

class Article(Resource):
  
  @marshal_with(resource_fields)
  def get(self, article_id):
    result = ArticleModel.query.get(article_id)
    if not result:
      abort(404, message="could not find article")
    return result
  
  @marshal_with(resource_fields)
  def put(self):
    args = article_put_args.parse_args()
    existing_entry = ArticleModel.query.filter_by(id = args['id'], slug = args['slug']).first()
    if not existing_entry:
      article = ArticleModel(
        id=args['id'],
        slug=args['slug'],
        title=args['title'],
        dek=args['dek'],
        published_date=args['published_date'],
        canonical_url=args['canonical_url'],
        word_count=args['word_count'],
        tags=args['tags']
      )
      db.session.add(article)
      db.session.commit()
      return article, 201
    
    else:
      print("ENTRY ALREADY EXISTS", existing_entry)
      if args['title']:
        existing_entry.title = args['title']
      db.session.commit()
      return existing_entry, 201
    

api.add_resource(Article, "/article", "/article/<string:article_id>")

if __name__ == "__main__":
  app.run(debug=True)