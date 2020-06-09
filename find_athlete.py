# Импортируем библиотеку для работы с датами
from datetime import datetime, timedelta

from users import *


class Athelete(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # Дата рождения атлета
    birthdate = sa.Column(sa.Text)
    # Пол атлета
    gender = sa.Column(sa.Text)
    # Рост атлета
    height = sa.Column(sa.FLOAT)
    # Имя атлета
    name = sa.Column(sa.Text)
    # Вес атлета
    weight = sa.Column(sa.Integer)
    # Золотые медали
    gold_medals = sa.Column(sa.Integer)
    # Серебряные медали
    silver_medals = sa.Column(sa.Integer)
    # Бронзовые медали
    bronze_medals = sa.Column(sa.Integer)
    # Всего медалей
    total_medals = sa.Column(sa.Integer)
    # Вид спорта
    sport = sa.Column(sa.Text)
    # Страна
    country = sa.Column(sa.Text)


def find_athlete_by_date(user_id, session):
    """
    Поиск атлета ближайшего по дате рождения к выбранному пользователю
    """
    # находим все записи в таблице User, у которых поле User.id совпадает с параметром user_id введенным пользователем
    query_user = session.query(User).filter(User.id == user_id)
    # Подсчитываем колличество найденных записей
    users_cnt = query_user.count()

    # Если запись найдена ищем атлета, если нет выводим инфоримацию о том, что такого ползователя нет в базе
    if users_cnt == 1:
        # Получаем дату рождения введенного пользователя
        user_birth_date = [user.birthdate for user in query_user]

        # Находим все записи в таблице athelete
        query_athlete = session.query(Athelete)
        # Выбираем даты рождения всех атлетов
        athlete_birth_date = [athlete.birthdate for athlete in query_athlete.all()]

        # Перевод даты рождения пользователя в формать datetime
        u_year = 0
        u_month = 0
        u_day = 0

        for user_date in user_birth_date:
            # Разделяем дату рождения пользователя на список split_user_date вида ['YYYY', 'MM', 'DD']
            split_user_date = user_date.split("-")
            u_year = int(split_user_date[0])
            u_month = int(split_user_date[1])
            u_day = int(split_user_date[2])

        user_date_of_birth = datetime(u_year, u_month, u_day)
        print("\nДата рождения пользователя с ID = {}:".format(user_id),
              user_date_of_birth.strftime("%Y-%m-%d"))

        # Аналогично разделяем даты рождения атлетов и переводим в нужный формат
        athlete_date_of_birth = []

        for athlete_date in athlete_birth_date:
            split_athlete_date = athlete_date.split("-")
            a_year = int(split_athlete_date[0])
            a_month = int(split_athlete_date[1])
            a_day = int(split_athlete_date[2])

            athlete_date_of_birth.append(datetime(a_year, a_month, a_day))

        # Считаем разницу между датой рождения пользователя и атлетов
        difference = []
        for date in athlete_date_of_birth:
            dif = date - user_date_of_birth
            difference.append(int(dif.days))

        # Находим индекс минимальной разницы
        index_min_dif = difference.index(min(difference, key=abs)) + 1

        # Выводим информацию о найденном атлете
        for athlete in query_athlete:
            if athlete.id == index_min_dif:
                print("Атлет с ближайше датой рождения.\n"
                      "ID: {}\n"
                      "Имя: {}\n"
                      "Дата рождения: {}".format(athlete.id, athlete.name, athlete.birthdate))
                print("Разница между датами в днях: {}".format(abs(min(difference, key=abs))))

    else:
        print("Ближайший по дате рождения атлет не может быть найден, "
              "так как пользователя с введенным идентификатором нет в базе.")


def find_athlete_by_height(user_id, session):
    """
    Поиск атлета ближайшего по росту к выбранному пользователю
    """
    # находим все записи в таблице User, у которых поле User.id совпадает с параметром user_id введенным пользователем
    query_user = session.query(User).filter(User.id == user_id)
    # Подсчитываем колличество найденных записей
    users_cnt = query_user.count()

    # Если запись найдена ищем атлета, если нет выводим инфоримацию о том, что такого ползователя нет в базе
    if users_cnt == 1:
        # Получаем рост введенного пользователя
        user_height = [user.height for user in query_user]
        print("\nРост выбранного пользователя:", user_height[0])

        # Находим все записи в таблице athelete
        query_athlete = session.query(Athelete)
        # Выбираем параметры роста всех атлетов
        athlete_height = [athlete.height for athlete in query_athlete.all()]

        # Список для вычисленной разници в росте атлета и пользователя
        difference = []
        # Спсиок id атлетов для которых вычисленна разница в росте с пользователем
        dif_id_athletes = []
        # Счетчик для добавления id атлетов, у которых есть данные о росте, в список dif_id_athletes
        cnt = 0

        for height in athlete_height:
            # Если есть данные о росте атлета
            if height:
                # Заполняем список разниц в росте
                difference.append(abs(height - user_height[0]))
                # Заполняем список id
                dif_id_athletes.append(cnt)
            cnt += 1

        # Индекс id нужного атлета в списке dif_id_athletes
        idx_id = difference.index(min(difference, key=abs)) + 1

        for athlete in query_athlete:
            if athlete.id == dif_id_athletes[idx_id]:
                print("Атлет с ближайшим ростом.\n"
                      "ID: {}\n"
                      "Имя: {}\n"
                      "Рост: {}".format(athlete.id, athlete.name, athlete.height))
                print("Разница в росте - {} м".format(min(difference, key=abs)))

    else:
        print("Ближайший по росту атлет не может быть найден, "
              "так как пользователя с введенным идентификатором нет в базе.")
