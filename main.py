import altair as alt
import streamlit as st
import pandas as pd
import os

# Configurar el modo ancho para acercar el contenido al panel lateral
st.set_page_config(layout="wide")

# Encabezado
st.write("""
# Analisis Curva de Luz
Nova Sco V1716
""")

# Panel lateral
sidebar = st.sidebar

# Espacio para el gráfico
figura = st.empty()

# Seguimiento de archivos cargados
archivos_cargados = []

# Carpeta que contiene los archivos CSV
carpeta_datos = 'data'

# Obtener la lista de archivos CSV en la carpeta
archivos_en_carpeta = [archivo for archivo in os.listdir(carpeta_datos) if archivo.endswith('.csv')]

# Mostrar mensaje de error si no se encuentran archivos CSV en la carpeta
if not archivos_en_carpeta:
    st.error("No se encontraron archivos CSV en la carpeta especificada.")
else:
    nombres = archivos_en_carpeta

    # Opciones para el gráfico
    sidebar.markdown("# Ajustes del gráfico")
    seleccionados = sidebar.multiselect("Selecciona los datos a visualizar", nombres)

    if seleccionados:
        tamaño_circulos = sidebar.slider("Ajustar tamaño de círculos", 1.0, 100.0)

    variables = {}  # Diccionario vacío

    for nombre in seleccionados:
        # Construir la ruta completa al archivo
        ruta_completa = os.path.join(carpeta_datos, nombre)

        # Verificar si el archivo ya ha sido cargado
        if nombre in archivos_cargados:
            st.warning(f"El archivo '{nombre}' ya ha sido cargado. Por favor, selecciona otro archivo.")
            continue

        # Leer el contenido del archivo como un DataFrame
        df = pd.read_csv(ruta_completa, sep=";", decimal=",")
        # Borrar los valores NaN del DataFrame
        df = df.dropna()
        # Asignar el DataFrame a una variable con el nombre del archivo
        variables[nombre] = df

        # Agregar el nombre del archivo a la lista de archivos cargados
        archivos_cargados.append(nombre)


    # Crear gráfico de dispersión para cada archivo seleccionado
    charts = [
        alt.Chart(variables[nombre]).mark_point(filled=False).encode(
            x='Tiempo desde erupcion (d)',
            y=alt.Y('Magnitud', scale=alt.Scale(domain=(variables[nombre]['Magnitud'].min(), variables[nombre]['Magnitud'].max()), reverse=True)),  # Invertir el eje Y
            size=alt.value(tamaño_circulos),
            color=alt.Color('Archivo:N', scale=alt.Scale(scheme='plasma')),
            opacity=alt.value(0.5),
            tooltip=['Tiempo desde erupcion (d)', 'Magnitud']
        ).transform_calculate(
            Archivo='"' + nombre + '"'
        )
        for nombre in seleccionados
    ]

    # Combinar gráficos en uno solo
    if charts:
        combined_chart = alt.layer(*charts).interactive()
        figura.altair_chart(combined_chart, use_container_width=True)

        # Expander con la conclusión de los datos
        with st.expander("Conclusion de los datos"):
            st.write("""
            Segun los datos del grafico podemos decir que bla bla bla bla y eso nos permite afirmar que bla bla bla, asi como un maximo de 103949 en comparacion a bla bla 
                     bla bla bla y eso hubiese pasado si chile hubiese ganado 1093293 medallas de oro y fiu seria presidente de chile.
            """)

    else:
        st.error("Por favor, selecciona al menos un dato para ver el gráfico.")

    # Mostrar DataFrames seleccionados y medidas de dispersión después de los gráficos
    if seleccionados:
        # Sección para Ajustes de DataFrame en el menú lateral
        sidebar.markdown("# Ajustes de DataFrame")
        archivo_seleccionado = sidebar.selectbox("Selecciona un archivo para ver sus datos", seleccionados)

        st.write(f"Datos para {archivo_seleccionado}:")
        st.dataframe(variables[archivo_seleccionado], use_container_width=True)
        st.write(f"Medidas de dispersión para {archivo_seleccionado}:")
        st.dataframe(variables[archivo_seleccionado].describe(), use_container_width=True)
