# Simple Reminder
Простая "open source" напоминалка для различных задач. Мною используется в основом в качестве повторения пройденного материала.
### Demo
![Demo](media/reminder.gif)

### Установка
~~~
#!/bin/bash
path_=$HOME/Apps    # use your path

mkdir $path_
git clone https://github.com/AtlanticP/reminder $path_/reminder
python -m venv $path_/reminder/.note    # создание виртуального окружения
source $path_/reminder/.note/bin/activate    # активация виртуального окружения
pip install --upgrade pip    # установка зависимостей
pip install -r $path_/reminder/requirements.txt
~~~
В домашней директории создается папка ***Apps***, в ней директория ***reminder***, в которую клонируются необходимые данные. Далее создается и активируется виртаульное окружение и устанавливаются зависимости.
Если установка осуществляется вручную, то для запуска напоминалки необходимы два пакета, указанные в ***requirements.txt***: 
~~~
pip install -r $path_/reminder/requirements.txt
~~~
### Запуск
~~~
python main.py
~~~
В процессе запуска Simple Reminder создает в корневой папке ***nosql*** файл ***tasks.csv***, в котором сохраняются задачи.
