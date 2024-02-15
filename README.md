# Yacut - укоротитель ссылок

Технологии:

Python

Flask


Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/hellakiddo/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Заполнить файл .env
``` bash
touch .env
nano .env
```

Создать базу данных и применить миграции
``` bash
flask db upgrade
```

Запуск проекта
``` bash
flask run
```

Автор: 
[https://github.com/hellakiddo](https://github.com/hellakiddo)