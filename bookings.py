#Импортируйте библиотеку pandas как pd. 
#Прочитайте датасет bookings.csv, находящийся по ссылке, с разделителем ;  и сохраните в переменную bookings. 
#Затем запишите первые 7 строк в переменную bookings_head.

import pandas as pd
bookings = pd.read_csv('https://stepik.org/media/attachments/lesson/360344/bookings.csv', sep=';')
bookings_head=bookings[:7]

#Замените пробел в названиях колонок на знак нижнего подчёркивания. 
def change(name):
    new_name = name.replace(' ', '_')
    new_name=str.lower(str(new_name))
    return(new_name)
bookings=bookings.rename(columns=change)

#Пользователи из каких стран совершили наибольшее число успешных бронирований? 
#Бронирование считается успешным, если в дальнейшем оно не было отменено (переменная is_canceled). 
#В качестве ответа выберите страны, входящие в топ-5.
bookings.query('is_canceled ==0') \
    .country \
    .value_counts()[:5]

#На сколько ночей (stays_total_nights)  в среднем бронируют отели типа City Hotel? Resort Hotel? 
#Запишите полученные значения в пропуски с точностью до 2 знаков после точки.
bookings \
    .groupby(['hotel'], as_index=False) \
    .aggregate({'stays_total_nights': 'mean'}) \
    .round(2)

#Иногда тип номера, полученного клиентом (assigned_room_type), отличается от изначально забронированного (reserved_room_type). 
#Такое может произойти, например, по причине овербукинга.
#Сколько подобных наблюдений встретилось в датасете?
bookings \
    .query('assigned_room_type != reserved_room_type') \
    .count()

#На какой месяц чаще всего оформляли бронь в 2016 году? 
#Изменился ли самый популярный месяц в 2017 году?
bookings \
    .groupby('arrival_date_year') \
    .arrival_date_month \
    .value_counts()

#На какой месяц (arrival_date_month) бронирования отеля типа City Hotel отменялись чаще всего в 2015? 2016? 2017? 
bookings.query("hotel == 'City Hotel'").groupby(["arrival_date_year", "arrival_date_month"])\
    .agg({"is_canceled": "sum"})\
    .sort_values(["arrival_date_year", "is_canceled"], ascending = [True, False])\
    .groupby("arrival_date_year")\
    .head(1)

#Посмотрите на числовые характеристики трёх колонок: adults, children и babies. 
#Какая из них имеет наибольшее среднее значение?
bookings.agg({'adults': 'mean', 'children': 'mean', 'babies': 'mean'}).idxmax()

#Создайте колонку total_kids, объединив столбцы children и babies. 
#Для отелей какого типа среднее значение переменной оказалось наибольшим?
#City hotel – отель находится в городе
#Resort hotel – отель курортный
#В качестве ответа укажите наибольшее среднее total_kids, округлив до 2 знаков после точки.
bookings["total_kids"]= bookings["children"]+bookings["babies"]
bookings \
    .groupby('hotel') \
    .aggregate({'total_kids': 'mean'}).round(2).max()

#Определить в какой группе Churn rate наибольший: с детьми или без?
#Churn_rate-отношение количества ушедших пользователей к общему количеству пользователей, 
#выраженное в процентах.

bookings['has_kids'] = bookings.total_kids>0
bookings.groupby('has_kids').agg({'is_canceled': 'mean'}) \
    .round(4)*100



