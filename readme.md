### Курсовой проект 6

##### В этой работе мы создаем свой сайт объявлений.


___
Для запуска контейнера и наполнения базы необходимо в терминале выполнить следующие команды:
```
docker-compose up -d
./manage.py migrate
./manage.py loaddata fixtures/ad.json fixtures/category.json fixtures/location.json fixtures/user.json
```