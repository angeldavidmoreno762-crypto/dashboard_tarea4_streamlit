import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats

st.set_page_config(page_title="Global Power Plant Database", page_icon="⚡", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("global_power_plant_database.csv")
    for col in ["capacity_mw", "estimated_generation_gwh", "generation_gwh_2013",
                "generation_gwh_2014", "generation_gwh_2015", "generation_gwh_2016"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df = load_data()

st.title("⚡ Análisis exploratorio de plantas eléctricas")
st.caption("Dataset: Global Power Plant Database | Exploración de capacidad instalada, combustibles y generación estimada.")

# Sidebar filters
st.sidebar.header("Filtros interactivos")
fuel_options = sorted(df["fuel1"].dropna().unique().tolist())
selected_fuels = st.sidebar.multiselect("Tipo de combustible (fuel1)", fuel_options, default=fuel_options)
capacity_values = df["capacity_mw"].dropna()
min_capacity, max_capacity = float(capacity_values.min()), float(capacity_values.max())
capacity_range = st.sidebar.slider(
    "Capacidad instalada (MW)", min_value=min_capacity, max_value=max_capacity,
    value=(min_capacity, max_capacity), step=1.0
)

filtered = df[
    df["fuel1"].isin(selected_fuels) &
    df["capacity_mw"].between(capacity_range[0], capacity_range[1], inclusive="both")
].copy()

st.subheader("Exploración de datos")
metric_data = filtered["capacity_mw"].dropna()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Registros filtrados", f"{len(filtered):,}")
m2.metric("Capacidad promedio", f"{metric_data.mean():,.2f} MW" if len(metric_data) else "N/D")
m3.metric("Desviación estándar", f"{metric_data.std():,.2f} MW" if len(metric_data) > 1 else "N/D")
m4.metric("Capacidad total", f"{metric_data.sum():,.2f} MW" if len(metric_data) else "N/D")

st.markdown("### Tabla de datos filtrados")
st.dataframe(filtered, use_container_width=True, height=320)

st.subheader("Visualizaciones")
c1, c2 = st.columns(2)

with c1:
    counts = filtered["fuel1"].value_counts().reset_index()
    counts.columns = ["Tipo de combustible", "Número de plantas"]
    fig1 = px.bar(counts, x="Tipo de combustible", y="Número de plantas",
                   title="Cantidad de plantas por tipo de combustible",
                   labels={"Tipo de combustible": "Combustible", "Número de plantas": "Cantidad"},
                   color="Tipo de combustible")
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    scatter_data = filtered[["capacity_mw", "estimated_generation_gwh", "fuel1", "country_long", "name"]].dropna()
    fig2 = px.scatter(scatter_data, x="capacity_mw", y="estimated_generation_gwh",
                       color="fuel1", hover_data=["country_long", "name"],
                       title="Capacidad instalada vs. generación estimada",
                       labels={"capacity_mw": "Capacidad instalada (MW)",
                               "estimated_generation_gwh": "Generación estimada (GWh)", "fuel1": "Combustible"})
    st.plotly_chart(fig2, use_container_width=True)

# Distribution by fuel, limit to categories with most records to keep chart legible
with st.container():
    top_fuels = filtered["fuel1"].value_counts().head(8).index.tolist()
    violin_data = filtered[filtered["fuel1"].isin(top_fuels)][["fuel1", "capacity_mw"]].dropna()
    violin_data = violin_data[violin_data["capacity_mw"] > 0]
    if not violin_data.empty:
        fig3 = px.box(violin_data, x="fuel1", y="capacity_mw", color="fuel1",
                      title="Distribución de capacidad instalada por combustible (8 categorías principales)",
                      labels={"fuel1": "Tipo de combustible", "capacity_mw": "Capacidad instalada (MW)"})
        fig3.update_yaxes(type="log")
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

# Optional temporal graph from the notebook's yearly generation variables
year_cols = ["generation_gwh_2013", "generation_gwh_2014", "generation_gwh_2015", "generation_gwh_2016"]
if all(col in filtered.columns for col in year_cols):
    yearly = pd.DataFrame({
        "Año": [2013, 2014, 2015, 2016],
        "Generación registrada (GWh)": [filtered[col].sum(skipna=True) for col in year_cols],
        "Registros disponibles": [filtered[col].notna().sum() for col in year_cols]
    })
    fig4 = px.line(yearly, x="Año", y="Generación registrada (GWh)", markers=True,
                    title="Evolución de la generación registrada (2013–2016)")
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("La disponibilidad de registros cambia entre años; la tendencia debe interpretarse teniendo en cuenta esa cobertura desigual.")

st.subheader("Validación estadística: prueba t de Welch")
st.write("Se compara la capacidad instalada promedio entre plantas Hydro y Gas. La prueba usa los datos dentro del rango de capacidad seleccionado y no depende del filtro de combustible, para mantener ambos grupos comparables.")
test_data = df[df["capacity_mw"].between(capacity_range[0], capacity_range[1], inclusive="both")][["fuel1", "capacity_mw"]].dropna()
g_hydro = test_data.loc[test_data["fuel1"].str.lower() == "hydro", "capacity_mw"]
g_gas = test_data.loc[test_data["fuel1"].str.lower() == "gas", "capacity_mw"]
if len(g_hydro) >= 2 and len(g_gas) >= 2:
    t_stat, p_val = stats.ttest_ind(g_hydro, g_gas, equal_var=False)
    a, b, c = st.columns(3)
    a.metric("Media Hydro", f"{g_hydro.mean():,.2f} MW", f"n={len(g_hydro):,}")
    b.metric("Media Gas", f"{g_gas.mean():,.2f} MW", f"n={len(g_gas):,}")
    c.metric("Valor p", f"{p_val:.3e}")
    st.write(f"Estadístico t: **{t_stat:.4f}**")
    if p_val < 0.05:
        st.success("Interpretación: el valor p es menor que 0,05. Existe evidencia estadística de que la capacidad instalada promedio de las plantas Hydro y Gas es diferente. Esto no significa que todas las plantas de un grupo sean mayores que las del otro.")
    else:
        st.info("Interpretación: el valor p es igual o mayor que 0,05. No hay evidencia suficiente para afirmar que las capacidades promedio de Hydro y Gas sean diferentes. Esto no demuestra que ambas sean iguales.")
else:
    st.warning("No hay suficientes registros de Hydro y Gas dentro del rango seleccionado para calcular la prueba.")

st.subheader("Hallazgos principales")
st.markdown("""
- El dataset permite comparar la capacidad instalada de plantas de diferentes fuentes energéticas.
- El tipo de combustible con mayor número de registros cambia según los filtros aplicados.
- La relación entre capacidad instalada y generación estimada se puede explorar visualmente; una relación positiva no implica por sí sola causalidad.
- Los valores extremos de capacidad pueden influir en promedios y escalas de los gráficos.
""")
st.caption("Aplicación académica elaborada para la Tarea 4. Los resultados se actualizan al cambiar los filtros.")
