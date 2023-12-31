# <div style=""><font size=5>Задания выполнены по курсу на https://unionepro.ru/:</font></div>

## <div style=""><font size=5>Курс: Использования языка программирования Python для автоматизации работы с веб-сервисами</font></div>

### <div style="text-align:center"><font size=5>Практическое задание №1.</font></div>

**<div style="text-align:center"><font size=4>Тема: «GraphQL schema-first»</font></div>**

**Суть работы:** реализовать api на основе GraphQL с использованием библиотеки ariadne.

**Ход работы:**

1. Выберите для работы любую интересную вам тематику, аналогично примеру с занятий про машины.
2. По аналогии с реализацией на занятиях написать свою программу, с query (получение списка объектов, получение одного объекта) и mutation (добавление, редактирование и удаление объекта).
3. Должно быть подключение к базе данных, и все манипуляции с объектами совершаются в ней.
4. Проверить работоспособность с помощью https://studio.apollographql.com/sandbox/explorer.

Результатом работы будет программный код и файл со скриншотами результатов запросов.

### <div style="text-align:center"><font size=5>Практическое задание №2.</font></div>

**<div style="text-align:center"><font size=4>Тема: «GraphQL code-first»</font></div>**

**Суть работы:** реализовать api на основе GraphQL с использованием библиотеки graphene.

**Ход работы:**
1. Выберите для работы любую интересную вам тематику, аналогично примеру с занятий про списки желаний.
2. По аналогии с реализацией на занятиях написать свою программу, с query (получение списка объектов, получение одного объекта) и mutation (добавление, редактирование и удаление объекта).
3. Доработать api программы с учётом разделения пользователей на авторизованных и неавторизованных. Дописать метод @app.route('/login', methods=['POST']) получения access_token.
4. Добавьте два метода для работы с query и mutation с учётом схем: для авторизованных пользователей – auth_required_schema и неавторизованных – schema, написанных на занятиях.
5. Базу данных можно создать просто в файле проекта для упрощения. Для этого запустите код в файле с занятия data.py, выполнив команду python data.py.
6. Проверьте работоспособность.

Результатом работы будет программный код и файл со скриншотами результатов запросов. 

### <div style="text-align:center"><font size=5>Практическое задание №3.</font></div>

**<div style="text-align:center"><font size=4>Тема: Парсер сайта [dog-60.ru](http://dog-60.ru/)</font></div>**

**Задание:** написать парсер для [dog-60.ru](http://dog-60.ru/)

Все категории (украшения и амуниция). По каждому из пунктов при их наличии:
- название, 
- идентификатор, 
- артикул, 
- размерная и ценовая сетка (с учётом скидки), 
- картинки, 
- описание, 
- характеристики, 
- наличие, 
- вложенность категорий.

Периодичность сбора: 1 раз в 14 дней.

### <div style="text-align:center"><font size=5>Практическое задание №4.</font></div>

**<div style="text-align:center"><font size=4>Тема: Парсер сайта [amazin.su](https://amazin.su/)</font></div>**

**Задание:** написать парсер для [amazin.su](https://amazin.su/)

Парсинг каталога товаров в категории зоотовары. По каждому параметру при его наличии:
- название, 
- идентификатор, 
- артикул, 
- весовая и ценовая сетка (с учётом скидки), 
- производитель, 
- картинки, 
- гарантия, 
- единицы, 
- вес, 
- описание, 
- инструкции, 
- характеристики, 
- наличие, 
- вложенность 
- категорий, 
- отзывы.

Периодичность сбора: 1 раз в 5 дней.
