from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import ast

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# MODELS
# - Article
# - Author (many to many with article)
# - Embed (many to many with article)
# - Lead Art (one to many, as in: one lead art can be used on many articles)

#join tables
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
  lead_art = db.Column(db.Integer, db.ForeignKey('lead_art_model.id', onupdate="CASCADE"), nullable=True)
  embeds = db.relationship('EmbedModel', secondary=embed_table, lazy='subquery', backref=db.backref('articles', lazy=True))
  authors = db.relationship('AuthorModel', secondary=author_table, lazy='subquery', backref=db.backref('articles', lazy=True))
  
  def __repr__(self):
    return '<Article %r>' %self.id
    
#lead art model (one-to-many relationship) 
class LeadArtModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String, nullable=True)
  articles = db.relationship('ArticleModel', backref=db.backref('article', lazy='joined'), lazy='dynamic')
  def __repr__(self):
    return '<LeadArt %r>' %self.id

# uncomment when running main.py for the first time to create database
#db.create_all()

# argument parsing
article_put_args = reqparse.RequestParser()
article_put_args.add_argument("article", type=str, required=True)


#serializer
resource_fields = {
  'id': fields.String,
  'slug': fields.String,
  'title': fields.String,
  'dek': fields.String,
  'published_date': fields.String,
  'canonical_url': fields.String,
  'word_count': fields.Integer,
  'tags': fields.String,
  'embeds': fields.List(fields.String),
  'authors': fields.List(fields.String),
  'lead_art': fields.String
}

class Article(Resource):
  
  # get article JSON  
  @marshal_with(resource_fields, envelope='article')
  def get(self, article_id):
    result = ArticleModel.query.get(article_id)
    if not result:
      abort(404, message="could not find article")
    return result
  
  # put article JSON
  @marshal_with(resource_fields)
  def put(self):
    # unpack args from 'article' envelope
    args = article_put_args.parse_args()
    args = ast.literal_eval(args['article'])
    #check if entry with id and canonical_url already exists
    existing_entry = ArticleModel.query.filter_by(id = args['id'], canonical_url = args['canonical_url']).first()
    
    # create new article
    if not existing_entry:
      article = ArticleModel(
        id=args['id'],
        slug=args['slug'],
        title=args['title'],
        dek=args['dek'],
        published_date=args['published_date'],
        canonical_url=args['canonical_url'],
        word_count=args['word_count'],
        tags=args['tags'],
      )
       
      #attach embeds, checking whether or not they're already in db 
      if args['embeds']:
        embeds = args['embeds']
        for embed in embeds:
          if EmbedModel.query.get(embed['id']) is not None:
            article.embeds.append(EmbedModel.query.get(embed['id']))
          else:
            embed = EmbedModel(
              id = embed['id']
            )
            article.embeds.append(embed)
      
      #attach authors, checking whether or not they're already in db
      if args['authors']:
        authors = args['authors']
        for author in authors:
          if AuthorModel.query.get(author['id']) is not None:
            article.authors.append(AuthorModel.query.get(author['id']))
          else:
            author = AuthorModel(
              id = author['id'],
              slug = author['slug']
            )
            article.authors.append(author)
      
      #attach lead art, checking whether or not it's already in db
      if args['lead_art']:
        lead_art = args['lead_art']
        if LeadArtModel.query.get(lead_art['id']) is not None:
          article.lead_art = lead_art['id']
        else:
          lead_art = LeadArtModel(
            id = lead_art['id'],
            type = lead_art['type']
          )
          article.lead_art = lead_art.id
          db.session.add(lead_art)
      
      db.session.add(article)
      db.session.commit()
      return article, 201
    
    # article update
    else:
      print("ENTRY ALREADY EXISTS", existing_entry)
      #update if args contain data
      if args['title']:
        existing_entry.title = args['title']
      if args['dek']:
        existing_entry.dek = args['dek']
      if args['published_date']:
        existing_entry.published_date = args['published_date']
      if args['slug']:
        existing_entry.slug = args['slug']
      if args['word_count']:
        existing_entry.word_count = args['word_count']
      if args['tags']:
        existing_entry.tags = args['tags']
      
      # update embeds by clearing out and then re-appending
      if args['embeds']:
        existing_entry.embeds = []
        embeds = args['embeds']
        for embed in embeds:
          if EmbedModel.query.get(embed['id']) is not None:
            print("HEEEEEEEEEEEEEEEEEEEEY", embed)
            existing_entry.embeds.append(EmbedModel.query.get(embed['id']))
          else:
            embed = EmbedModel(
              id = embed['id']
            )
            existing_entry.embeds.append(embed)

      # update authors by clearing out and reappending
      if args['authors']:
        existing_entry.authors = []
        authors = args['authors']
        for author in authors:
          if AuthorModel.query.get(author['id']) is not None:
            existing_entry.authors.append(AuthorModel.query.get(author['id']))
          else:
            author = AuthorModel(
              id = author['id'],
              slug = author['slug']
            )
            existing_entry.authors.append(author)
      
      # update lead art
      if args['lead_art']:
        lead_art = args['lead_art']
        if LeadArtModel.query.get(lead_art['id']) is not None:
          existing_entry.lead_art = lead_art['id']
        else:
          new_lead_art = LeadArtModel(
            id = lead_art['id'],
            type = lead_art['type']
          )
          db.session.add(new_lead_art)
      
      db.session.commit()
      return existing_entry, 201
    

api.add_resource(Article, "/article", "/article/<string:article_id>")

if __name__ == "__main__":
  app.run(debug=True)