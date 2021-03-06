# -*- coding: utf-8 -*-
"""Practica2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nj7BVLDUJpbuJVZ0ZLlxVGmJvdfgFRD9

# **Lectura de les dades des del drive**

Cal guardar el csv en el drive personal. NO funciona en drive compartit perquè no ho troba. Jo el que he fet és crear una carpeta "data" en el meu drive i posar el csv allà dins.
"""

from google.colab import drive

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
from scipy.stats import shapiro 
from scipy.stats import fligner
from scipy.stats import kruskal
from scipy.stats import mannwhitneyu

!pip install shap
import shap


#Per la realització d'aquesta pràctica hem treballat amb google collaboratory
#Per això els processos de càrrega i guardat de les dades són en base al drive
drive.mount('/content/drive')

path = "/content/drive/MyDrive/data/caracteristiques_pisos_igualada.csv"
pisos = pd.read_csv(path, sep=',', encoding='latin-1')

"""---

# Neteja de valors missing
"""

#pisos
#pisos.isnull().sum()

#Transformar els valors missing de orientacion en un nivell més de la variable (no_definido)
pisos.orientacion[pisos.orientacion.isnull()] = "no_definido"
pisos.orientacion.value_counts()

pisos.describe(include = [np.number]).drop(columns = ['id'])

#les variables numèriques presenten valors de -1 que en realitat són NaN

#Transformar els valors -1 i -2022 en NA (valors missing)
pisos = pisos.replace(-1,np.NaN)
pisos = pisos.replace(-2022,np.NaN)
#pisos.describe(include = [np.number]).drop(columns = ['id'])
pisos.isnull().sum()

#imputar per la mitjana tots els valors null de les variables numèriques
pisos.fillna(pisos.mean(), inplace = True)
pisos.isnull().sum()

"""**Altres neteges**



"""

#Cal netejar la variable orientación perquè hi han valors duplicats amb commes
pisos['orientacion'] = pisos['orientacion'].str.replace(',','')
pisos.orientacion.value_counts()

#transformació de la variable planta en categòrica + neteja de valors missing

#creació de nivell "no definido"
pisos.planta = pisos.planta.replace(np.NaN,-1)
pisos.planta = pisos.planta.astype(int).apply(str)
pisos.planta[pisos.planta == "-1"] = "no_definido"

#agregació dels casos menys freqüents en una nova categoria
plantes_low = pd.value_counts(pisos.planta)
mask = (plantes_low/plantes_low.sum() * 100).lt(5) #menys del 5% dels casos
pisos['planta'] = np.where(pisos['planta'].isin(plantes_low[mask].index),'5_o_superior',pisos['planta'])
pisos.planta.value_counts()

"""
# Deteccio outliers"""

outliers = pisos.drop(columns = ['id','terraza','balcon','estado', 'orientacion', 'garaje','ascensor','aire_acondicionado','zonas_verdes_o_jardin','ciudad','zona','etiqueta_energetica','calefaccion','titulo_anuncio'])
outliers.describe()

#com hem observat hi ha un outlier als metres útils i anem a veure si hi han mes elements afectats
out_mutil = list(set(outliers['utiles_m']))
out_mutil

#ara per tant veiem que hi ha el valor 1, i del 33 en amunt que ja son acceptables, per tant revertim el canvi 
#fet per contar els valors i asignarem la mitjana de la propietat als valors 1 dels metres utils
pisos.utiles_m[pisos.utiles_m == 1.0] = statistics.mean(pisos.utiles_m)

#veiem el resultat final
pisos.utiles_m.describe()

"""## Boxplots"""

#boxplot de les variables numèriques per detectar outliers
sns.set_theme(style="whitegrid")
sns.boxplot(x=pisos["construidos_m"])

pisos[pisos.construidos_m > 700]

sns.boxplot(x=pisos["utiles_m"])

sns.boxplot(x=pisos["habitaciones"])

sns.boxplot(x=pisos["baños"])

sns.boxplot(x=pisos["año_construido"])

sns.boxplot(x=pisos["precio"])

sns.boxplot(x=pisos["precio_anterior"])

"""# Guardar conjunt de dades net"""

#guardar el conjunt de dades net
path = "/content/drive/MyDrive/data/caracteristiques_pisos_igualada_clean.csv"

with open(path, 'w', encoding = 'utf-8-sig') as f:
  pisos.to_csv(f)

"""# Anàlisi de les dades"""

#descriprius basics
pisos.describe()

pisos.describe(include='object')

"""# Comprovació de la normalitat de les dades"""

#loop per comprovar la nomalitat de les dades numèriques

pisos_numeric = pisos.drop(columns = ['id','terraza','balcon','estado', 'orientacion', 'garaje','ascensor',
                                      'aire_acondicionado','zonas_verdes_o_jardin',
                                      'ciudad','zona','etiqueta_energetica','calefaccion','titulo_anuncio','planta'])

for var_pos in range(len(pisos_numeric.columns.to_list())):
  variable = pisos_numeric.columns.to_list()[var_pos]

  #test the Saphiro-Wilk per normalitat de les dades
  normality_test = shapiro(pisos_numeric[variable])
  print("Normalitat de la variable: "+pisos_numeric.columns.to_list()[var_pos])
  print(normality_test)
  print('\n')

#Comprovar homogeneïtat de la variància de les dades

#Precio - construidos_m
print("Precio - construidos_m")
print(fligner(pisos.precio.to_list(), pisos.construidos_m.to_list()))
print('\n')

#Precio - utiles_m
print("Precio - utiles_m")
print(fligner(pisos.precio.to_list(), pisos.utiles_m.to_list()))
print('\n')

#Precio - habitaciones
print("Precio - habitaciones")
print(fligner(pisos.precio.to_list(), pisos.habitaciones.to_list()))
print('\n')

#Precio - baños
print("Precio - baños")
print(fligner(pisos.precio.to_list(), pisos.baños.to_list()))
print('\n')

#Precio - año_construido
print("Precio - año_construido")
print(fligner(pisos.precio.to_list(), pisos.año_construido.to_list()))
print('\n')

print("Homogeneitat de variances entre totes les variables")
print(fligner(pisos.precio.to_list(), pisos.año_construido.to_list(), pisos.construidos_m.to_list(), pisos.utiles_m.to_list(),pisos.baños.to_list()))

"""# Matriu de correlacions"""

pisos_numeric.corr()

# Compute the correlation matrix
#sns.pairplot(pisos_numeric)

"""# Test estadístics per comparar les medianes per més de dos grups"""

#kruskal wallis test d'igualtat de medianes

#Precio - planta
print("Precio - planta")
print(kruskal(pisos.precio.to_list(), pisos.planta.to_list()))
print('\n')

#Precio - orientación
print("Precio - orientación")
print(kruskal(pisos.precio.to_list(), pisos.orientacion.to_list()))
print('\n')

#Precio - zona
print("Precio - zona")
print(kruskal(pisos.precio.to_list(), pisos.zona.to_list()))
print('\n')

#Construidos_m - zona
print("Construidos_m - zona")
print(kruskal(pisos.construidos_m.to_list(), pisos.zona.to_list()))
print('\n')

ax = sns.boxplot(x="zona", y="construidos_m", data=pisos)

#Mann-Whitney test d'igualtat de medianes per 2 grups

#Precio - estado
print("Precio - estado")
print(mannwhitneyu(pisos.precio.to_list(), pisos.estado.to_list()))
print('\n')

#Precio - ascensor
print("Precio - ascensor")
print(mannwhitneyu(pisos.precio.to_list(), pisos.ascensor.to_list()))
print('\n')

ax = sns.boxplot(x="estado", y="precio", data=pisos)

ax = sns.boxplot(x="ascensor", y="precio", data=pisos)

"""# Model de predicció del preu d'un pis en base a les seves característiques"""

#agafem les característiques dels pisos
pisos.columns

features = list(pisos.columns)

#eliminar variables que no es volen afegir al model + variable objectiu
unwanted_feat = ['precio', 'id','utiles_m','ciudad','precio_anterior','titulo_anuncio']
features = [ele for ele in features if ele not in unwanted_feat]

#codificar variables categòriques en dummies
encoded_df = pd.get_dummies(pisos[features])

#Capturar variables explicatives i variable objectiu
X = encoded_df
Y = pisos['precio']

#Partició de les dades entrenament 95% i test 5%
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size = 0.05, random_state = 42)

features

"""## Model base"""

#Funció per evaluar l'accuracy del model = 100-mape
def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    errors = abs(predictions - test_labels)
    mape = 100 * np.mean(errors / test_labels)
    accuracy = 100 - mape
    print('Model Performance')
    print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
    print('Accuracy = {:0.2f}%.'.format(accuracy))
    
    return accuracy

from sklearn.ensemble import RandomForestRegressor

#model base amb els paràmetres per defecte
base_model = RandomForestRegressor(random_state = 42)

#entrenem el random forest
base_model.fit(X_train, y_train)

#Evaluació de la performance en mostra de test
base_accuracy = evaluate(base_model, X_test, y_test)

"""## Busqueda aleatòria - Random Hyperparameter Grid"""

from sklearn.model_selection import RandomizedSearchCV

# Numero d'arbres en el random forest
n_estimators = [int(x) for x in np.linspace(start = 1000, stop = 2000, num = 10)]

# Numero de característiques a considerar a cada split de l'arbre
max_features = ['auto', 'sqrt']

# Nombre màxim de nivells a l'arbre
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# nombre mínim de mostres requerides per separar un node
min_samples_split = [2, 5, 10]
#  nombre mínim de mostres requerides a cada fulla de l'arbre (node)
min_samples_leaf = [1, 2, 4]
# Mètode per seleccionar mostres per entrenar a cada arbre
bootstrap = [True, False]
# Crear el grid de paràmetres
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

# Busqueda aleatoria dels parametres usand 3 fold cross validation entre 100 combinacions diferents fent servir tots els cores
# search across 100 different combinations, and use all available cores
rf_random = RandomizedSearchCV(estimator = base_model, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
# Ajustar el random search
rf_random.fit(X_train, y_train)


#Millor combinació de hyper parametres
rf_random.best_params_

best_random = rf_random.best_estimator_
random_accuracy = evaluate(best_random, X_test, y_test)

"""## Interpretació del model"""

explainer = shap.TreeExplainer(best_random)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test, plot_type="bar")

shap.summary_plot(shap_values, X_test)