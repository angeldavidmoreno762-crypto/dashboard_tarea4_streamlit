# Análisis exploratorio de plantas eléctricas

## Descripción del proyecto

Este proyecto desarrolla un dashboard interactivo para realizar un análisis exploratorio de datos de plantas eléctricas a partir del Global Power Plant Database. La aplicación permite explorar información relacionada con la capacidad instalada, las fuentes de energía y la generación estimada, con el propósito de identificar patrones y diferencias entre las tecnologías de generación eléctrica.

El dashboard fue desarrollado utilizando Python y Streamlit, incorporando filtros interactivos que permiten analizar los datos de acuerdo con el tipo de combustible y la capacidad instalada. Las visualizaciones y métricas se actualizan dinámicamente para facilitar la exploración y comprensión de la información.

## Dataset

**Fuente:** Global Power Plant Database.

El conjunto de datos contiene información de plantas eléctricas a nivel mundial, incluyendo variables como país, nombre de la planta, tipo de combustible, capacidad instalada, ubicación geográfica y generación estimada.

## Dashboard publicado

🌐 [Acceder al dashboard interactivo](https://dashboard-tarea4-angel-moreno.streamlit.app/)

## Visualizaciones incluidas

- Cantidad de plantas por tipo de combustible.
- Capacidad instalada frente a generación estimada.
- Distribución de capacidad instalada por combustible.
- Evolución de la generación registrada entre 2013 y 2016.

## Validación estadística

Se realizó una prueba t de Welch para comparar la capacidad instalada promedio de las plantas Hydro y Gas.

Resultados:

- Media Hydro: 148,69 MW.
- Media Gas: 384,46 MW.
- Estadístico t: -19,3333.
- Valor p: 9,535 × 10⁻⁸¹.

El resultado evidencia una diferencia estadísticamente significativa entre las capacidades promedio de ambos grupos, considerando un nivel de significancia de 0,05.

## Hallazgos principales

- El dataset permite comparar la capacidad instalada de plantas de diferentes fuentes energéticas.
- El tipo de combustible con mayor número de registros puede cambiar según los filtros aplicados.
- La relación entre capacidad instalada y generación estimada puede explorarse visualmente; una relación positiva no implica por sí sola causalidad.
- Los valores extremos de capacidad pueden influir en los promedios y en las escalas de los gráficos.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- SciPy

## Ejecución local

Para ejecutar la aplicación localmente:

1. Clonar el repositorio:

```bash
git clone https://github.com/angeldavidmoreno762-crypto/dashboard_tarea4_streamlit.git
```

2. Ingresar a la carpeta del proyecto:

```bash
cd dashboard_tarea4_streamlit
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:

```bash
streamlit run app.py
```

## Información académica

**Actividad:** Tarea 4 – Dashboard interactivo y comunicación de resultados.

**Universidad:** Universidad Nacional Abierta y a Distancia (UNAD).

**Estudiante:** Ángel Moreno.

