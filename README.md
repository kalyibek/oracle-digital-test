# oracle-digital-test

## Установка и настройка

1. Сперва перейдите в корневую директорию приложения и выполните команду "docker-compose build" для создания образа.
   ```cmd
    docker-compose build
   ```
2. Затем примените миграции, команда приведена ниже:
   ```cmd
    docker-compose run django python manage.py migrate
   ```

3. Затем выполните команду "docker-compose run django python manage.py loaddata data.json" для загрузки фикстур из файла data.json.
   ```cmd
    docker-compose run django python manage.py loaddata data.json
   ```
   
4. Не забудьте создать суперюзера:
   ```cmd
    docker-compose run django python manage.py createsuperuser
   ```
   
5. И наконец запустите контейнеры:
   ```cmd
    docker-compose up
   ```
   
Создайте необходимые записи в админ панели (School, Klass).
