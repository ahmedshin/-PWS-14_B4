import uuid
import os
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = sa.Column(sa.Integer, primary_key=True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.Float)

def connect_db():
	 # создаем соединение к базе данных
	engine = sa.create_engine(DB_PATH)
	# создаем описанные таблицы
	Base.metadata.create_all(engine)
	# создаем фабрику сессию
	session = sessionmaker(engine)
	# возвращаем сессию
	return session()

def request_data():
	#  выводим приветствие.
	print ("Привет! Я запишу твои данные!")
	# запрашиваем у пользователя данные
	first_name = input("Введи своё имя: ")
	last_name = input("А теперь фамилию: ")
	gender = input("Пол: ")
	email = input("Мне еще понадобится адрес твоей электронной почты: ")
	birthdate = input("Дата рождения: ")
	height = input("Твой рост: ")
	# генерируем идентификатор пользователя и сохраняем его строковое представление
	user_id = str(uuid.uuid4())
	
	user = User(
		first_name=first_name,		
		last_name=last_name,
		gender = gender,
		email=email,
		birthdate = birthdate,
		height = height
		)
	return user

def find():
	# находим все записи в таблице User, у которых поле User.first_name совпадает с параметром name
	query = session.query(User).filter(User.first_name == name)
	# подсчитываем количество таких записей в таблице с помощью метода .count()
	users_cnt = query.count()
	# составляем список идентификаторов всех найденных пользователей
	user_ids = [user.id for user in query.all()]
	# находим все записи в таблице LastSeenLog, у которых идентификатор совпадает с одним из найденных
	last_seen_query = session.query(LastSeenLog).filter(LastSeenLog.id.in_(user_ids))
	# строим словарь вида идентификатор_пользователя: время_его_последней_активности
	log = {log.id: log.timestamp for log in last_seen_query.all()}
	# возвращаем кортеж количество_найденных_пользователей, список_идентификаторов, словарь_времени_активности
	return (users_cnt, user_ids, log)

def print_users_list(cnt, user_ids, last_seen_log):

    if user_ids:
    	# если список не пуст, распечатываем количество найденных пользователей
    	print("Найдено пользователей: ", cnt)
    	# легенду будущей таблицы
    	print("Идентификатор пользователя - дата его последней активности")
    	# проходимся по каждому идентификатору
    	for user_id in user_ids:
    		# получаем время последней активности из словаря last_seen_log
    		last_seen = last_seen_log[user_id]
    		# выводим на экран идентификатор — время_последней_активности
    		print("{} - {}".format(user_id, last_seen))
    else:
    	# если список оказался пустым, выводим сообщение об этом
    	print("Пользователей с таким именем нет.")
def main():
	
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти пользователя по имени\n2 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1":
    	# выбран режим поиска, запускаем его
    	name = input("Введи имя пользователя для поиска: ")
    	# вызываем функцию поиска по имени
    	users_cnt, user_ids, log = find(name, session)
    	# вызываем функцию печати на экран результатов поиска
    	print_users_list(users_cnt, user_ids, log)
    elif mode == "2":
    	# запрашиваем данные пользоватлея
    	user = request_data()
    	# добавляем нового пользователя в сессию
    	session.add(user)
    	# обновляем время последнего визита для этого пользователя
    	# log_entry = update_timestamp(user.id, session)
    	# добавляем объект log_entry в сессию
    	# session.add(log_entry)
    	# сохраняем все изменения, накопленные в сессии
    	session.commit()
    	print("Спасибо, данные сохранены!")
    else:
    	print("Некорректный режим:(")
if __name__ == "__main__":
	main()