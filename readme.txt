# cursor_project_1

Проект - онлайн-магазин

Запуск проекта - manage.py runserver
В целях тестирования по умолчанию создано:
 - два пользователя:
    - администратор (логин - admin, пароль - password);
    - обычный пользователь (логин - user, пароль - password);
 - два магазина;
 - два товара;
 - две категории товаров.
А также соответствующие таблицы в базе данных (плюс таблица для записи покупок пользователей)

Функции администратора - в шапке сайта
Поиск товаров - на странице товаров (/products)
Добавление товара в корзину покупок - на странице конкретного товара (например, /products/2)
Совершение покупки - на странице корзины (/cart)
История покупок доступна только для зарегистрированных пользователей (/purchase_history, покупки для неавторизированных пользователей вносится в базу с пустым полем user_id)
