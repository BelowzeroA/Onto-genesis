from nltk.corpus import treebank
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn

iris_dataset = load_iris()
print("Ключи iris_dataset: \n{}".format(iris_dataset.keys()))
print(iris_dataset['DESCR'][:250] + "\n...")
print("Названия ответов: {}".format(iris_dataset['target_names']))
print("Названия признаков: \n{}".format(iris_dataset['feature_names']))


X_train, X_test, y_train, y_test = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)
print("форма массива X_train: {}".format(X_train.shape))
print("форма массива y_train: {}".format(y_train.shape))

iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
# создаем матрицу рассеяния из dataframe, цвет точек задаем с помощью y_train
grr = pd.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15), marker='o',
 hist_kwds={'bins': 20}, s=60, alpha=.8, cmap=mglearn.cm3)
