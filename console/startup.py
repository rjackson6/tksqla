from tksqla import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///var/db.sqlite', echo=True)
Session = sessionmaker(bind=engine)
