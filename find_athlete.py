import uuid
import os
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

def connect_db():
	 # создаем соединение к базе данных
	engine = sa.create_engine(DB_PATH)
	# создаем описанные таблицы
	Base.metadata.create_all(engine)
	# создаем фабрику сессию
	session = sessionmaker(engine)
	# возвращаем сессию
	return session()

class User(Base):
	__tablename__ = 'user'
	id = sa.Column(sa.Integer, primary_key=True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.Float)

class Athlete(Base):
	__tablename__ = 'athelete'

	id = sa.Column(sa.Integer, primary_key=True)
	age = sa.Column(sa.Integer)
	birthdate = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	height = sa.Column(sa.Float)
	weight = sa.Column(sa.Integer)
	name = sa.Column(sa.Text)
	gold_medals = sa.Column(sa.Integer)
	silver_medals = sa.Column(sa.Integer)
	bronze_medals = sa.Column(sa.Integer)
	total_medals = sa.Column(sa.Integer)
	sport = sa.Column(sa.Text)
	country = sa.Column(sa.Text)

def take_user_id():
	user_id = input("Введи id пользователя для поиска: ")
	return int(user_id)

def convert_date(date_str):
	parts = date_str.split("-")
	# parts = date_str.split(".")
	date_parts = map(int, parts)
	date = datetime.date(*date_parts)
	return date

def find_atelets_height(session, user_height):
    
    athletes_list = session.query(Athlete).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user_height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        if height is None:
            continue

        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height

def find_atelets_bd(session, user_birthdate):
	athletes = session.query(Athlete).all()
	# (athletes).sort()
	
	athlete_id_bd = {}
	for athlete in athletes:
		bd = convert_date(athlete.birthdate)
		athlete_id_bd[athlete.id] = bd

	user_bd = convert_date(user_birthdate)
	min_dist = None
	athlete_id = None
	athlete_bd = None
	

	for id_, bd in athlete_id_bd.items():
		dist = abs(user_bd - bd)
		if not min_dist or dist < min_dist:
			min_dist = dist
			athlete_id = id_
			athlete_bd = bd
	return athlete_id, athlete_bd


def main():
	
    session = connect_db()
    user_id = take_user_id()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
    	print("Пользователь не наден!")
    else:
    	user_birthdate = user.birthdate
    	user_height = user.height
    	bd_athlete, bd = find_atelets_bd(session, user_birthdate)
    	print("Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd))

    	height_athlete, height = find_atelets_height(session, user_height)
    	print("Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height))

    	# print(user_birthdate)
    	# print(user_height)
    
    
if __name__ == "__main__":
	main()