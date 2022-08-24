from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Query

# Create Database
Base = declarative_base()


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)


engine = create_engine('sqlite:///weather.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

city_1 = Cities(name='Odessa')
city_2 = Cities(name='Boston')
city_3 = Cities(name='Oslo')
city_4 = Cities(name='Praga')
session.add(city_1)
session.add(city_2)
session.add(city_3)
session.add(city_4)
session.commit()

