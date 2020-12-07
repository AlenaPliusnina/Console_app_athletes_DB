# Users_athletes_DataBase_B_4.12

Консольное приложение

Описание проекта:

1. Модуль users.py регистрирует новых пользователей. Скрипт запрашивает следующие данные:

   - имя
   - фамилию
   - пол
   - адрес электронной почты
   - дату рождения
   - рост
   
2. Все данные о пользователях сохраняются в таблице user базы данных sochi_athletes.sqlite3.

3. Модуль find_athlete.py осуществляет поиск ближайшего к пользователю атлета. Его логика работы такова:

   - запросить идентификатор пользователя;
   
   - если пользователь с таким идентификатором существует в таблице user, то вывести на экран двух атлетов: 
     ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
     
   - если пользователя с таким идентификатором нет, вывести соответствующее сообщение.


Разворачивае проект локально:

1. Скачайте репозиторий

2. Создайт виртуальное окружение:

       python -m venv env

3. Активируйте виртуальное окружение:

       source env/bin/activate

2. Запаустите команду в терминале (командной строке) проекта:

       python users.py

В консоли появится пользователское меню:

![Иллюстрация к проекту](https://github.com/AlenaPliusnina/Users_athletes_DataBase_B_4.12/blob/master/screenshoots/screen_1.png)

![Иллюстрация к проекту](https://github.com/AlenaPliusnina/Users_athletes_DataBase_B_4.12/blob/master/screenshoots/screen_2.png)

![Иллюстрация к проекту](https://github.com/AlenaPliusnina/Users_athletes_DataBase_B_4.12/blob/master/screenshoots/screen_3.png)

![Иллюстрация к проекту](https://github.com/AlenaPliusnina/Users_athletes_DataBase_B_4.12/blob/master/screenshoots/screen_4.png)

