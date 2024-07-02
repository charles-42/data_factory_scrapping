import scrapy
import csv
from allocine_project.allocine.items import MovieScraperItem
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from allocine_project.allocine import settings 
from dotenv import load_dotenv

load_dotenv()


Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, Sequence('movie_id_seq'), primary_key=True)
    title = Column(String)

class MovieSpider(scrapy.Spider):
    name = "film_spider"
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://www.allocine.fr/film/meilleurs/"]

    def __init__(self):
        db = settings.DATABASE
        database_url = f"postgresql://{db['username']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
        
        # Set up the database connection
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def parse(self, response):
        movies = response.xpath('//h2')

        for movie in movies :
            movie_url = movie.xpath('./a/@href').get()
            yield response.follow(movie_url, callback=self.parse_movie)
        

    def parse_movie(self, response):

        item = MovieScraperItem()

        item['title'] = response.xpath('//h1/text()').get()

        movie = Movie(title=item['title'])
        self.session.add(movie)
        self.session.commit()
        yield item
        