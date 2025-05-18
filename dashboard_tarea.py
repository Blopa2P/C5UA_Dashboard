import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# Título principal
st.title("📊 Dashboard de Ventas - Supermercado")

# Cargar los datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = cargar_datos()

# Barra lateral con filtros
st.sidebar.header("Filtros")
sucursales = st.sidebar.multiselect("Sucursal", df["Branch"].unique(), default=df["Branch"].unique())
lineas = st.sidebar.multiselect("Línea de Producto", df["Product line"].unique(), default=df["Product line"].unique())
rango_fechas = st.sidebar.date_input("Rango de fechas", [df["Date"].min(), df["Date"].max()])

# Aplicar filtros
df_filtrado = df[
    (df["Branch"].isin(sucursales)) &
    (df["Product line"].isin(lineas)) &
    (df["Date"] >= pd.to_datetime(rango_fechas[0])) &
    (df["Date"] <= pd.to_datetime(rango_fechas[1]))
]

# Visualizaciones
st.subheader("1️⃣ Evolución de las Ventas Totales")
ventas = df_filtrado.groupby("Date")["Total"].sum()
fig1, ax1 = plt.subplots()
ventas.plot(marker='o', ax=ax1)
ax1.set_title("Ventas Totales por Fecha")
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Total")
st.pyplot(fig1)

st.subheader("2️⃣ Ingresos por Línea de Producto")
fig2, ax2 = plt.subplots()
df_filtrado.groupby("Product line")["Total"].sum().sort_values().plot(kind="barh", ax=ax2)
ax2.set_title("Ingresos por Línea de Producto")
ax2.set_xlabel("Total")
st.pyplot(fig2)

st.subheader("3️⃣ Distribución de Calificaciones de Clientes")
fig3, ax3 = plt.subplots()
sns.histplot(df_filtrado["Rating"], bins=10, kde=True, ax=ax3)
ax3.set_title("Distribución de Calificaciones")
ax3.set_xlabel("Rating")
st.pyplot(fig3)

st.subheader("4️⃣ Gasto por Tipo de Cliente")
fig4, ax4 = plt.subplots()
sns.boxplot(data=df_filtrado, x="Customer type", y="Total", ax=ax4)
ax4.set_title("Gasto por Tipo de Cliente")
st.pyplot(fig4)

st.subheader("5️⃣ Relación entre Costo y Ganancia Bruta")
fig5, ax5 = plt.subplots()
sns.scatterplot(data=df_filtrado, x="cogs", y="gross income", ax=ax5)
ax5.set_title("Costo vs Ingreso Bruto")
st.pyplot(fig5)

st.subheader("6️⃣ Métodos de Pago Preferidos")
fig6, ax6 = plt.subplots()
df_filtrado["Payment"].value_counts().plot(kind="bar", ax=ax6)
ax6.set_title("Métodos de Pago")
ax6.set_xlabel("Método")
ax6.set_ylabel("Frecuencia")
st.pyplot(fig6)

st.subheader("7️⃣ Correlación entre Variables Numéricas")
fig7, ax7 = plt.subplots(figsize=(10, 6))
sns.heatmap(df_filtrado[["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]].corr(), annot=True, cmap="coolwarm", ax=ax7)
ax7.set_title("Matriz de Correlación")
st.pyplot(fig7)

st.subheader("8️⃣ Ingreso Bruto por Sucursal y Línea de Producto")
pivot = df_filtrado.groupby(["Branch", "Product line"])["gross income"].sum().unstack()
fig8, ax8 = plt.subplots(figsize=(10, 6))
pivot.plot(kind="bar", stacked=True, ax=ax8)
ax8.set_title("Ingreso Bruto por Sucursal y Línea de Producto")
ax8.set_ylabel("Ingreso Bruto")
ax8.set_xlabel("Sucursal")
ax8.legend(title="Línea de Producto", bbox_to_anchor=(1.05, 1))
st.pyplot(fig8)
