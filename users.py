# Импортируем модуль поиска атлетов
from find_athlete import *

# Чтобы SQLAlchemy работала необходимо установить ее в проекте через терминал:  pip install sqlalchemy
# импортируем библиотеку SQLAlchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # Пол пользователя
    gender = sa.Column(sa.Text)
    # Дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # Рост пользователя
    height = sa.Column(sa.FLOAT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    email = input("Адрес твоей электронной почты: ")
    gender = input("Укажите Ваш пол (Male/Female): ")
    birthdate = input("Введите Вашу дату рождения в формате YYYY-MM-DD: ")
    height = input("Введите свой рост в формате meters.centimeters (метры.сантиметры), например 1.88: ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    # user_id = str(uuid.uuid4())
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def find(name, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # находим все записи в таблице User, у которых поле User.first_name совпадает с параметром name
    query = session.query(User).filter(User.first_name == name)
    # подсчитываем количество таких записей в таблице с помощью метода .count()
    users_cnt = query.count()
    # составляем список идентификаторов всех найденных пользователей
    user_ids = [user.id for user in query.all()]
    # возвращаем кортеж количество_найденных_пользователей, список_идентификаторов
    return (users_cnt, user_ids)


def print_users_list(cnt, user_ids):
    """
    Выводит на экран количество найденных пользователей и их идентификаторы
    Если передан пустой список идентификаторов, выводит сообщение о том, что пользователей не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if user_ids:
        # если список не пуст, распечатываем количество найденных пользователей
        print("Найдено пользователей: ", cnt)
        print("Список идентификаторов найденных пользователей")
        # проходимся по каждому идентификатору
        for user_id in user_ids:
            # выводим на экран идентификатор — время_последней_активности
            print("ID: {}".format(user_id))
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователей с таким именем нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти пользователя по имени\n2 - ввести данные нового пользователя\n"
                 "3 – найти двух атлетов: ближайшего по дате рождения к данному пользователю "
                 "и ближайшего по росту к данному пользователю\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        name = input("Введи имя пользователя для поиска: ")
        # вызываем функцию поиска по имени
        users_cnt, user_ids = find(name, session)
        # вызываем функцию печати на экран результатов поиска
        print_users_list(users_cnt, user_ids)
    elif mode == "2":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    elif mode == "3":
        user_id = input("Введите идентификатор пользователя: ")
        find_athlete_by_date(user_id, session)
        find_athlete_by_height(user_id, session)
    else:
        print("Некорректный режим:(")


if __name__ == "__main__":
    main()