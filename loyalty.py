#Определить долю пользователей, лояльных к бренду
#Импортирую необходимые библиотеки
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#Эта строчка необходима, чтобы графики показывались сразу в jupiter notebook
%matplotlib inline

#Загружаю данные
df=pd.read_csv('https://stepik.org/media/attachments/lesson/383523/lesson_3_data__1_.csv', encoding='windows-1251')

#Переименовываю колонки
user_df=user_df.rename(columns={'tc':'user_id', 'art_sp': 'brand_info'})

#Достаю название бренда
user_df['brand_name']=user_df.brand_info.apply(lambda x: x.split(' ')[-1])

#Смотрю, какое кол-во покупок у каждого пользователя
users_purchases = user_df.groupby('user_id', as_index=False) \
    .agg({'brand_info': 'count'}) \
    .rename(columns={'brand_info': 'purchases'})

#Смотрю медианное значение покупок (медиана 2)
users_purchases.purchases.median()

#Смотрю описательные хар-ки таблицы 
users_purchases.purchases.describe()

#Выбираю 75% квантиль, так как там кол-во покупок >=5(достаточно, чтобы определить лояльность покупателя)
users_purchases = user_df.groupby('user_id', as_index=False) \
    .agg({'brand_info': 'count'}) \
    .rename(columns={'brand_info': 'purchases'}) \
    .query('purchases >= purchases.quantile(q=0.75)')

#Смотрю, какой бренд любимый у пользователей (они его покупают чаще всего)
favourite_brand_purchases_df =user_df.groupby(['user_id', 'brand_name'], as_index=False) \
    .agg({'brand_info':'count'}) \
    .sort_values(['user_id', 'brand_info'], ascending= [False, False]) \
    .groupby('user_id') \
    .head(1) \
    .rename(columns=({'brand_name': 'favourite_brand', 'brand_info': 'favourite_brand_purchases'}))

#Смотрю кол-во уникальных брендов у каждого пользователя
user_unique_brands = user_df.groupby('user_id', as_index=False) \
    .agg({'brand_name': pd.Series.nunique}) \
    .rename(columns={'brand_name': 'unique_brands'})

#Объединяю 3 таблицы
loyalty_df=users_purchases.merge(user_unique_brands, on='user_id') \
    .merge(favourite_brand_purchases_df, on ='user_id')

#Выявляю тех пользователей, у кого один уникальный бренд (они точно лояльные)
loyal_users=loyalty_df[loyalty_df.unique_brands==1]

#Ввожу "меру лояльности"
loyalty_df['loyalty_score']=loyalty_df.favourite_brand_purchases/loyalty_df.purchases

#Визуализирую пользователей по мере лояльности
ax = sns.displot(loyalty_df.loyalty_score, kde=False)

#Группирую бренды по медианному значению меры лояльности
brand_loyalty=loyalty_df.groupby('favourite_brand', as_index=False) \
    .agg({'loyalty_score': 'median', 'user_id': 'count'}) \
    .sort_values('loyalty_score', ascending = False)

#Визуализирую эту группировку
ax = sns.barplot( x='favourite_brand', y="loyalty_score", data=brand_loyalty)










