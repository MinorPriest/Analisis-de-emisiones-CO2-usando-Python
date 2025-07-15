#Bibliotecas
import pandas as pd  
import matplotlib.pyplot as plt 

#Configuración de estilos para los gráficos
plt.style.use('ggplot')

#Definir funciones
#Cargar datos
def cargar_filtrar_datos(url):
    #Carga los datos desde la URL
    #Se filtran solo las lineas necesarias.
    
    #Carga el archivo CSV
    df= pd.read_csv(url) 

    #Definir las casillas a usar, pueden agregar o quitar
    columnas = ['country', 'year', 'iso_code', 'population', 'gdp', 'co2']
    df = df[columnas]

    #Filtrar los países
    df = df[df['iso_code'].notna()]

    #Rellenar cuando hay 0 en la casilla co2.
    df['co2'] = df['co2'].fillna(0)

    return df

#Realiza el analisis y devuelve lo solicitado
def analisis_datos(df, pais_ejemplo):
    resultados = {}

    #Top 10 paises con mas emisiones en el último año.
    emisiones_total = df.groupby('country')['co2'].sum().sort_values(ascending=False)
    resultados['top_10_emisiones_total'] = emisiones_total.head(10)

    #Determina de la lista cual es el año mas reciente.
    anno_reciente = df['year'].max()
    resultados['año_reciente'] = anno_reciente

    #Top 10 emisiones en el año mas reciente
    df_reciente = df[df['year'] == anno_reciente].copy()
    df_reciente['co2_per_capita'] = df_reciente['co2'] / df_reciente['population']

    emisiones_recientes = df_reciente.groupby('country')['co2'].sum().sort_values(ascending=False)
    resultados['top_10_emisiones_recientes'] = emisiones_recientes.head(10)

    top_per_capita = df_reciente.groupby('country')['co2_per_capita'].sum().sort_values(ascending=False)
    resultados['top_10_per_capita'] = top_per_capita.head(10)

    #Valores a través del tiempo para un país específico.
    evolucion_pais = df[(df['country'] == pais_ejemplo) & (df['year'] >= 1950)].sort_values('year')
    resultados['evolucion_pais'] = evolucion_pais
    resultados['pais_ejemplo'] = pais_ejemplo

    return resultados

#Genera los gráficos, se pueden ajustar tamaños, colores y temas.
def generar_graficos(resultados):
    # Gráfico 1: Emisiones totales acumuladas (top 10)
    plt.figure(figsize=(12, 8))
    resultados['top_10_emisiones_total'].sort_values().plot(kind='barh', color='darkblue')
    plt.title('Top 10 países con mayores emisiones acumuladas de CO2 (histórico)')
    plt.xlabel('Emisiones totales de CO2 (millones de toneladas)')
    plt.ylabel('País')
    plt.tight_layout()
    plt.savefig('grafico_emisiones_totales.png')
    plt.close()
    
    # Gráfico 2: Emisiones en el año más reciente (top 10)
    plt.figure(figsize=(12, 6))
    resultados['top_10_emisiones_recientes'].plot(kind='bar', color='green')
    plt.title(f'Top 10 países con mayores emisiones de CO2 en {resultados["año_reciente"]}')
    plt.ylabel('Emisiones de CO2 (millones de toneladas)')
    plt.xlabel('País')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('grafico_emisiones_recientes.png')
    plt.close()
    
    # Gráfico 3: Evolución de emisiones para un país específico
    plt.figure(figsize=(12, 6))
    plt.plot(resultados['evolucion_pais']['year'], resultados['evolucion_pais']['co2'], 
             marker='o', linestyle='-', color='red')
    plt.title(f'Evolución de emisiones de CO2 en {resultados["pais_ejemplo"]} (1950-{resultados["año_reciente"]})')
    plt.xlabel('Año')
    plt.ylabel('Emisiones de CO2 (millones de toneladas)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('grafico_evolucion_pais.png')
    plt.close()
    
#Función principal.
def main():
    #Dirección URL
    url = "https://raw.githubusercontent.com/owid/co2-data/refs/heads/master/owid-co2-data.csv"

    print("En unos segundos estará listo, estoy cargando y ordenando tus datos...")
    df = cargar_filtrar_datos(url)

    #Obtener lista única de países disponibles
    paises_disponibles = sorted(df['country'].dropna().unique())

    #Mostrar menú numerado con los países (primeros 30 por ejemplo)
    print("\nPaíses disponibles para análisis individual:")
    for i, pais in enumerate(paises_disponibles[:30], 1):
        print(f"{i}. {pais}")
    print("...")  # indicar que hay más países

    #Solicitar al usuario que seleccione un país válido mediante número o nombre exacto
    while True:
        seleccion = input("\nEscribe el número o el nombre exacto del país para analizar su evolución de emisiones: ").strip()

        if seleccion.isdigit():
            indice = int(seleccion) - 1
            if 0 <= indice < len(paises_disponibles):
                pais_ejemplo = paises_disponibles[indice]
                break
        elif seleccion in paises_disponibles:
            pais_ejemplo = seleccion
            break

        print("Selección no válida. Intenta con el número o nombre exacto del país.")

    print("Analizando datos...")
    resultados = analisis_datos(df, pais_ejemplo)

    print("Generando gráficos...")
    generar_graficos(resultados)

    print("\nResultados del análisis:")
    print("\n1. Top 10 países con mayores emisiones acumuladas:")
    print(resultados['top_10_emisiones_total'])
    
    print(f"\n2. Top 10 países con mayores emisiones en {resultados['año_reciente']}:")
    print(resultados['top_10_emisiones_recientes'])
    
    print(f"\n3. Top 10 países con mayores emisiones per cápita en {resultados['año_reciente']}:")
    print(resultados['top_10_per_capita'])
    
    print(f"\n4. Evolución de emisiones para {resultados['pais_ejemplo']}:")
    print(resultados['evolucion_pais'][['year', 'co2']].set_index('year'))
    
    print("\nProceso completado. Gráficos guardados en el directorio actual.")

if __name__ == "__main__":
    main()
