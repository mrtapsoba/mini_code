import streamlit as st
import pandas as pd

import os
import matplotlib.pyplot as plt
import seaborn as sns
import math


# Chemin du dossier à parcourir
dossier = r"C:\Users\boubakar\Documents\Master_projet\data\insitu\output/"

# Extension des fichiers à rechercher (par exemple, ".txt")
extension_recherchee = ".csv"

# Liste pour stocker les chemins des fichiers trouvés
chemins_fichiers = []

# Parcourir le dossier
for dossier_racine, sous_dossiers, fichiers in os.walk(dossier):
    for fichier in fichiers:
        if fichier.endswith(extension_recherchee):
            chemin_complet = os.path.join(dossier_racine, fichier)
            chemins_fichiers.append(chemin_complet)

st.title("Visualisation des données manquantes")
st.sidebar.title("Choix du fichier")

file = st.sidebar.selectbox("Selectionner un fichier ", chemins_fichiers)

st.write("Vous avez choisi le fichier ", file)
data = pd.read_csv(file)

time_min = data['Year'].min()
time_max = data['Year'].max()

st.write("La periode ", time_min, " ", time_max)

col1, col2 = st.columns(2)

missing_pourcentage = data.isnull().mean() * 100
missing_number = data.isnull().sum()
st.text("Nombre de ligne : " +str(len(data)))
st.text("")
with col1 :
    st.text("Nombre le ligne manquant")
    st.text(missing_number)

with col2 :
    st.text("Pourcentage manquant pour chaque colonne")
    st.text(missing_pourcentage)

st.text("Nombre de ligne total : " +str(len(data)))

st.title("Visualisation graphique")
data['date'] = pd.to_datetime(data[['Year', 'Month', 'Day', 'Hour']])
dataset = data.set_index(['Year', 'Month', 'Day', 'Hour'])
dataset = dataset.drop(columns=['Doy', 'Unnamed: 0', 'longitude', 'latitude'])
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(dataset.isnull(), cmap='viridis') #, cbar=False)
plt.title("Visualisation des données manquantes")
st.pyplot(fig)

st.title("Evolution des variables en fontions du temps")
cola, colb = st.columns(2)

group_by = dataset
with cola :
    selected_columns = st.multiselect("Selection des variables ", dataset.columns)

with colb :
    periode = st.selectbox("Selection de la période ", ['Hour', 'Day', 'Month', 'Year'])
    

if periode == 'Hour':
    group_by = dataset.groupby('date').mean()
if periode == 'Day':
    group_by = dataset.resample('D', on='date').mean()
if periode == 'Month':
    group_by = dataset.resample('M', on='date').mean()
if periode == 'Year':
    group_by = dataset.resample('Y', on='date').mean()
st.write("Moyenne des variables choisies sur la période choisie")
st.write(group_by[selected_columns])
st.write("Représentation graphique")
if selected_columns:
    num_cols = 2
    num_plots = len(selected_columns)
    num_rows = math.ceil(num_plots / num_cols)
    fig2, ax2 = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(10, 6*num_rows))
    plot_idx = 0

    for column in selected_columns:

        plot_row = plot_idx // num_cols
        plot_col = plot_idx % num_cols

        if num_rows == 1:
            axs = ax2[plot_col]
        else:
            axs = ax2[plot_row, plot_col]
        
        axs.plot(group_by.index, group_by[column], label = column)
        axs.set_xlabel("Temps")
        axs.set_ylabel("Valeur")
        axs.set_title(f"Evolution de {column} en fonction du temps")
        axs.legend()

        plot_idx += 1

    for i in range(plot_idx, num_rows * num_cols):
        if num_rows == 1:
            ax2[i].axis('off')
        else:
            ax2[i // num_cols, i % num_cols].axis('off')

    st.pyplot(fig2)

else:
    st.write("Selectionner au moins une varible pour visualiser son evolution")