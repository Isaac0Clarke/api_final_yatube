# API_FINAL_YATUBE

# Как запустить проект:

Открыть папку проекта

Написать в терминале 
```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
. venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
    
# Примеры запросов

```
http://127.0.0.1:8000/redoc/
```

Публикация поста

```
POST http://127.0.0.1:8000/api/v1/posts/
{
  "text": "string",
  "image": "string",
  "group": 0
}
```

Получение списка групп

```
GET http://127.0.0.1:8000/api/v1/groups/ 
```

Получение списка постов

```
GET http://127.0.0.1:8000/api/v1/posts/
```

Получение всех комментариев

```
GET http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
```
