# Simple Reminder
Простая "open source" напоминалка для различных задач. Мною используется в основом в качестве повторения пройденного материала.
### Demo
<img src="media/reminder.gif" width=420 height=300>

### Установка в Ubuntu
Возможно для установки виртуального окружения может понадобится **python3.x-venv** пакет. 
```
$ python --version
3.8.10
```
В моем случае пакет версии **python3.8-venv** .
```
$ sudo apt install python3.8-venv
```
Создаем скрипт 
```
$ vi $HOME/Desktop/reminstall.sh
```
В нем сохраняем следующие строки:
~~~
#!/bin/bash
path_=$HOME/Apps    # use your path

mkdir $path_
git clone https://github.com/AtlanticP/reminder $path_/reminder
python3 -m venv $path_/reminder/.venv    # создание виртуального окружения
source $path_/reminder/.note/bin/activate    # активация виртуального окружения
pip install --upgrade pip    # установка зависимостей
pip install -r $path_/reminder/requirements.txt
~~~
В домашней директории создается папка ***Apps***, в ней директория ***reminder***, в которую клонируются необходимые данные. Далее создается и активируется виртаульное окружение и устанавливаются зависимости.

Запускаем скрипт, превдарительно сделав его исполняемым:
```
$ sudo chmod +x $HOME/Descktop/reminstall.sh
$ source $HOME/Descktop/reminstall.sh
```
NOTE: Если установка осуществляется вручную, то для запуска напоминалки необходимы два пакета, указанные в ***requirements.txt***: 
~~~
path_=$HOME/Apps    # use your path
pip install -r $path_/reminder/requirements.txt
~~~
### Запуск
~~~
path_=$HOME/Apps
source $path_/reminder/.venv/bin/activate
python $path_/reminder/main.py
~~~
В процессе запуска Simple Reminder создает в корневой папке ***nosql*** файл ***tasks.csv***, в котором сохраняются задачи.

### Автозапуск (пример в Ubuntu)
Создаем  файл ***reminder.desktop*** в папке автозагрузк с соответствующим расширением:
```
vi $HOME/.config/autostart/reminder.desktop
```
В нем прописываем следующую конфигурацию:
~~~
[Desktop Entry]
Type=Application
Name=Reminder
Exec=$HOME/Apps/reminder/autostart.sh
~~~
Сохраняеем изменения и создаем новый файл ***autostart.sh*** в корневой папке приложения:
```
$ vi $HOME/Apps/reminder/autostart.sh
```
Скрипт будет содежрать следующий код:
~~~
#!/bin/bash
path_=$HOME/Apps/reminder
$path_/.note/bin/python $path_/main.py &
~~~
Делаем ***autostart.sh*** файл исполняемым:
```
$ sudo chmod +x $HOME/Apps/reminder/autostart.sh
```