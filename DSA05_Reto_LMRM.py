import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import codecs

#---------------------
#     FUNCIONES
#---------------------
@st.cache
def load_data(nrows):
    doc = codecs.open('Employees.csv','rU','latin1')
    data = pd.read_csv(doc, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    return data

def search_employees(search_term,column):
    if search_term:
        results = data[data[column].str.contains(search_term, case=False, na=False)]
        return results
    return data

def filter_data_by_education_level(level):
    filtered_data_education = data[data['Education_Level'] == level]
    return filtered_data_education

def filter_data_by_hometown(hometown):
    filtered_data_hometown = data[data['Hometown'] == hometown]
    return filtered_data_hometown

def filter_data_by_unit(unit):
    filtered_data_unit = data[data['Unit'] == unit]
    return filtered_data_unit

#---------------------
# CARGA DE DATOS
#---------------------
DATE_COLUMN = 'released'
DATA_URL = ('Employees.csv')

#Cargar datos de empleados
data = load_data(501)

#---------------------
#  ELEMENTOS GRAFICOS
#---------------------

#Título
st.title("DSA05 Reto | Aplicación web de Ciencia de Datos")
st.write("---")

#Estudiante
st.markdown("*Elaborador por:* ***Leonardo Miguel Ramos Morán***.")
st.write("---")

#Descripción proyecto
st.header("Aplicación web de Ciencia de Datos:")
st.write("Actualmente en las empresas, la gente ya no tiende a envejecer durante su estadía en las mismas. Cada vez es más frecuente ver casos en donde la gente cambia de trabajo. Los siguientes datos fueron tomados del Hackathon HackerEarth 2020 y se complementaron con información propocionada por los departamentos de T.I. de las empresas encuestadas.")
st.write("Utiliza los diferentes gráficos y filtros para realizar diferentes análisis:")


#SIDEBAR

#-- Instrucción 8 --
if st.sidebar.checkbox('Mostrar todos los empleados'):
    st.subheader('Todos los empleados')
    st.write(data)

st.sidebar.write("---")

#-- Instrucción 10: Filtrar empleados por nivel educativo con control selectedbox dentro del sidebar
st.sidebar.header("Búsqueda de Empleados por Nivel Educativo")
selected_education = st.sidebar.selectbox("Seleccionar Nivel Educativo", data['Education_Level'].unique())
btnFilterbyEducation = st.sidebar.button('Filtrar Nivel ')

if (btnFilterbyEducation):
   st.write("---")
   filterbyedu = filter_data_by_education_level(selected_education)
   count_row = filterbyedu.shape[0]  # Gives number of rows
   st.write(f"Total empleados : {count_row}")

   st.dataframe(filterbyedu)
   st.write("---")

st.sidebar.write("---")

#-- Instrucción 11: Mostrar empleados por Ciudad con un control selectedbox dentro del sidebar
st.sidebar.header("Empleados por Ciudad")
ciudades = data['Hometown'].unique()
city_selection = st.sidebar.selectbox("Selecciona una Ciudad:",ciudades)

if city_selection:
    st.sidebar.write(f"Total de empleados en {city_selection}:", len(filter_data_by_hometown(city_selection)))
    st.sidebar.dataframe(filter_data_by_hometown(city_selection))


#----------------------------------
#SECCIONES DE CONTENIDO

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Buscador", "Unidad funcional", "Histograma", "Frecuencias", "Ciudades", "Edad vs Deserción", "T. Servicio vs Deserción"])

with tab1:
    #-- Instrucción 9: Buscador de empleados por ID, Ciudad o Unidad Funcional 
    st.header("Búsqueda de Empleados por ID, Ciudad o Unidad Funcional")
    search_column = st.selectbox("Selecciona el campo de búsqueda:", ["Employee_ID","Hometown","Unit"])
    search_term = st.text_input(f"Ingrese {search_column}:","")

    if st.button("Buscar"):
        results = search_employees(search_term, search_column)
        st.write("Total de empleados encontrados", len(results))
        st.dataframe(results)
   

with tab2:
    #-- Instrucción 12: Filtrar por Unidad Funcional con un control selectedbox
    st.header("Empleados por Unidad Funcional")
    unidades = data['Unit'].unique()
    unit_selection = st.selectbox("Selecciona una Unidad Funcional:",unidades)

    if unit_selection:
        st.write(f"Total de empleados en {unit_selection}:", len(filter_data_by_unit(unit_selection)))
        st.dataframe(filter_data_by_unit(unit_selection))
  

with tab3:
    #-- Instrucción 13: Crear histograma de empleados agrupados por edad
    data['Age'] = pd.to_numeric(data['Age'])
    st.header("Histograma de Empleados por Edad")

    plt.figure(figsize=(10,6))
    plt.hist(data['Age'], bins=15, color="mediumaquamarine", edgecolor="black")
    plt.xlabel("Edad")
    plt.ylabel("Número de Empleados")
    plt.title("Distribución de Empleados por Edad")
    st.pyplot(plt)

with tab4:
    #-- Instrucción 14: Gráfica de frecuencias para las Unidades Funcionales y determinar cuántos empleados hay en cada Unidad
    st.header("Gráfica de Frecuencias por Unidad Funcional")

    sns.set(style="whitegrid")

    plt.figure(figsize=(10,6))
    sns.countplot(x=data['Unit'], palette='pastel')
    plt.xlabel("Unidad Funcional")
    plt.ylabel("Frecuencia")
    plt.title("Frecuencia por Unidad Funcional")
    plt.xticks(rotation=90)
    st.pyplot(plt)

    unit_counts = data['Unit'].value_counts()
    st.write("Cantidad de empleados por unidad funcional:")
    st.write(unit_counts)

with tab5:
    #-- Instrucción 15: Visualizar las Ciudades que tienen el mayor índice de deserción 
    cities = data['Hometown'].unique()
    avg_attrition_by_city = data.groupby('Hometown')['Attrition_rate'].mean()
    avg_attrition_by_city = avg_attrition_by_city.sort_values(ascending=False)

    st.header("Ciudades con Mayor Índice de Deserción")

    plt.figure(figsize=(10,6))
    bars = plt.bar(avg_attrition_by_city.index, avg_attrition_by_city.values, color='salmon')
    plt.xlabel("Ciudad")
    plt.ylabel('Índice de Deserción Promedio')
    plt.title("Índice de Deserción por Ciudad")
    plt.xticks(rotation=45)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval,3), ha='center', va='bottom')

    st.pyplot(plt)

    city_max_attrition = data.loc[data['Attrition_rate'].idxmax()]['Hometown']
    st.write(f"Ciudad con mayor índice de deserción: {city_max_attrition}")

with tab6:
    #-- Instrucción 16: Visualizar la edad y la tasa de deserción 
    st.header("Visualización de Edad y Tasa de Deserción")

    sns.set(style="whitegrid")

    fig, axes = plt.subplots(1, 2, figsize=(12,6))
    sns.histplot(data=data, x='Age', bins=15, color='blue', kde=True, ax=axes[0])
    axes[0].set_xlabel("Edad")
    axes[0].set_ylabel("Frecuencia")
    axes[0].set_title("Distribución de Edades")

    sns.histplot(data=data, x='Attrition_rate', bins=15, color='orange', kde=True, ax=axes[1])
    axes[1].set_xlabel("Tasa de Deserción")
    axes[1].set_ylabel("Frecuencia")
    axes[1].set_title("Distribución de Tasa de Deserción")

    plt.tight_layout()
    st.pyplot(plt)

with tab7:
    #-- Instrucción 16: Gráfica que determina la relación entre el Tiempo de Servicio y la Tasa de Deserción
    st.header("Relación entre Tiempo de Servicio y Tasa de Deserción")

    plt.figure(figsize=(10,6))
    plt.scatter(x=data['Time_of_service'], y=data['Attrition_rate'], color='orange', alpha=0.5)
    plt.xlabel("Tiempo de Servicio")
    plt.ylabel("Tasa de Deserción")
    plt.title("Relación entre Tiempo de Servicio y Tasa de Deserción")
    plt.grid(True)
    st.pyplot(plt)
            