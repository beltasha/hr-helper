import numpy as np
import pandas as pd
import sklearn.linear_model as lm
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_regression

# загружаем файл с данными
df = pd.DataFrame.from_csv("../datasets/GH_user_statistic_prepared.csv")

# нормализуем
scaled_features = StandardScaler().fit_transform(df.values)
# df = pd.DataFrame(scaled_features, index=df.index, columns=df.columns)

# x - таблица с исходными данными факторов
x = df.iloc[:,1:-1]
# print(x.head())
# y - таблица с исходными данными зависимой переменной
y = df.iloc[:,-1]
# print(y.head())

# выбираем лучшие признаки
selector = SelectKBest(f_regression, k=4)
selector.fit(x.values, y.values)
print(x.columns)
print(x.columns[selector.get_support()])

x_new = selector.transform(x)

# создаем пустую модель
skm = lm.LinearRegression()
# запускаем расчет параметров для указанных данных
skm.fit(x, y)
# и выведем параметры рассчитанной модели
print(skm.intercept_)
print(skm.coef_)