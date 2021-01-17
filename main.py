from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class ArticleModel(db.Model):
  id = db.Column(db.String, primary_key=True)
  slug = db.Column(db.String, nullable=True)
  title = db.Column(db.String, nullable=True)
  dek = db.Column(db.String, nullable=True)
  published_date = db.Column(db.String, nullable=True)
  canonical_url = db.Column(db.String, nullable=True)
  word_count = db.Column(db.Integer, nullable=True)
  tags = db.Column(db.String, nullable=True)
  
  def __repr__(self):
    return f"Video(id={id}, slug={slug}"

# db.create_all()

article_put_args = reqparse.RequestParser()
article_put_args.add_argument("id", type=str, help="ID of article", required=True)
article_put_args.add_argument("slug", type=str, help="slug of article")
article_put_args.add_argument("title", type=str, help="title of article")
article_put_args.add_argument("dek", type=str, help="dek of article")
article_put_args.add_argument("published_date", type=str, help="pub date of article")
article_put_args.add_argument("canonical_url", type=str, help="canonical url of article")
article_put_args.add_argument("word_count", type=int, help="word count of article")
article_put_args.add_argument("tags", type=str, help="tags of article")


resource_fields = {
  'id': fields.String,
  'slug': fields.String,
  'title': fields.String,
  'dek': fields.String,
}

class Article(Resource):
  
  @marshal_with(resource_fields)
  def get(self, article_id):
    result = ArticleModel.query.filter_by(id = article_id).first()
    if not result:
      abort(404, message="could not find article")
    return result
  
  @marshal_with(resource_fields)
  def put(self):
    args = article_put_args.parse_args()
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


api.add_resource(Article, "/article", "/article/<string:article_id>")

if __name__ == "__main__":
  app.run(debug=True)