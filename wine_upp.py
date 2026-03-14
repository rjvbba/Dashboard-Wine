import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="🍷 Wine Upp 🍷",
    layout="wide"
)

st.title("🍷 Wine Upp 🍷")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("df.csv")
    return df

df = load_data()


# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filtros")

# Optional cluster filter
if "cluster" in df.columns:
    cluster = st.sidebar.multiselect(
        "Gama",
        options=sorted(df["cluster"].unique()),
        default=sorted(df["cluster"].unique())
    )
else:
    cluster = None



alcohol_range = st.sidebar.slider(
    "Alcool",
    float(df["alcohol"].min()),
    float(df["alcohol"].max()),
    (float(df["alcohol"].min()), float(df["alcohol"].max()))
)

sugar_range = st.sidebar.slider(
    "Açucar residual",
    float(df["residual sugar"].min()),
    float(df["residual sugar"].max()),
    (float(df["residual sugar"].min()), float(df["residual sugar"].max()))
)

va_range = st.sidebar.slider(
    "Acidez fixa",
    float(df["fixed acidity"].min()),
    float(df["fixed acidity"].max()),
    (float(df["fixed acidity"].min()), float(df["fixed acidity"].max()))
)
q_range = st.sidebar.slider(
    "Qualidade",
    float(df["quality"].min()),
    float(df["quality"].max()),
    (float(df["quality"].min()), float(df["quality"].max()))
)



# -------------------------
# Apply Filters
# -------------------------
filtered_df = df[
    
    (df["alcohol"].between(alcohol_range[0], alcohol_range[1])) &
    (df["residual sugar"].between(sugar_range[0], sugar_range[1])) &
    (df["fixed acidity"].between(va_range[0], va_range[1]))&
    (df["quality"].between(q_range[0], q_range[1]))
]


if cluster is not None:
    filtered_df = filtered_df[filtered_df["cluster"].isin(cluster)]

# -------------------------
# Metrics
# -------------------------
st.subheader("Gamas")


col1, col2, col3, col4, = st.columns(4)

with col1:
    st.metric("Vinhos", len(filtered_df))

with col2:
    st.metric("Raiz", (filtered_df["cluster"] == "Raiz").sum())
    st.image("raiz.jpeg", width=45)

with col3:
    st.metric("Grande Século", (filtered_df["cluster"] == "Grande Século").sum())
    st.image("grande.jpeg", width=65)

with col4:
    st.metric("Momento", (filtered_df["cluster"] == "Momento").sum())
    st.image("momento.jpeg", width=45)

# -------------------------
# Radar Chart
# -------------------------
categorias = ["residual sugar", "density", "alcohol", "fixed acidity","quality"]

if filtered_df.empty:
    st.warning("⚠️ Nenhum vinho encontrado com os filtros selecionados.")
else:
    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(filtered_df[categorias])

    scaled_df = filtered_df.copy()
    scaled_df[categorias] = scaled_values

    valores = scaled_df[categorias].mean().values

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        name='Perfil Médio',
        line=dict(color="#722F37"),
        fillcolor="rgba(114,47,55,0.4)"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,1] 
            )
        ),
        showlegend=True
    )

    st.subheader("Características")
    st.plotly_chart(fig, use_container_width=True)


# -------------------------
# Data Table
# -------------------------
st.subheader("Vinhos")
st.dataframe(filtered_df, hide_index=True)

