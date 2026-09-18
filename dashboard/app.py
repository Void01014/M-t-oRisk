import streamlit as st
import pandas as pd
import plotly.express as px

from sqlalchemy import select

from load.database import engine
from load.models import WeatherForecast


st.set_page_config(page_title="MétéoRisk", layout="wide")

st.title("MétéoRisk — Risque météo logistique")


@st.cache_data(ttl=600)
def load_data():

    statement = select(WeatherForecast).order_by(
        WeatherForecast.city,
        WeatherForecast.date
    )

    with engine.connect() as connection:
        return pd.read_sql(statement, connection)


df_all = load_data()

if df_all.empty:
    st.warning("Aucune donnée disponible.")
    st.stop()

df_all["date"] = pd.to_datetime(df_all["date"])

df_all["risk_level"] = pd.cut(
    df_all["risk_score"],
    bins=[-1, 30, 60, 100],
    labels=["Low", "Medium", "High"]
)

st.sidebar.header("Filtres")

cities = st.sidebar.multiselect("Ville", sorted(df_all["city"].unique()))

date_min, date_max = df_all["date"].min(), df_all["date"].max()
date_range = st.sidebar.date_input(
    "Période", value=(date_min, date_max), min_value=date_min, max_value=date_max
)

risk_levels = st.sidebar.multiselect(
    "Niveau de risque", ["Low", "Medium", "High"], default=["Low", "Medium", "High"]
)

df = df_all.copy()
if cities:
    df = df[df["city"].isin(cities)]
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df[(df["date"] >= start) & (df["date"] <= end)]
if risk_levels:
    df = df[df["risk_level"].isin(risk_levels)]

if df.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Villes", df["city"].unique())
col2.metric("Risque moyen", round(df["risk_score"].mean(), 1))
col3.metric("Risque max", round(df["risk_score"].max(), 1))
col4.metric("Jours à risque élevé", int((df["risk_level"] == "High").sum()))

tab_overview, tab_business, tab_data = st.tabs(
    ["Vue d'ensemble", "Questions métier", "Données"]
)

with tab_overview:
    st.subheader("Carte du risque (dernier jour sélectionné par ville)")
    latest = df.sort_values("date").groupby("city", as_index=False).last()
    fig_map = px.scatter_map(
        latest,
        lat="latitude",
        lon="longitude",
        color="risk_score",
        size="risk_score",
        hover_name="city",
        hover_data={"risk_score": True, "temp_max": True, "precipitation": True},
        color_continuous_scale="YlOrRd",
        zoom=4.3,
        height=500,
    )
    fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Évolution du risque national par jour")
        daily = df.groupby("date", as_index=False)["risk_score"].mean()
        fig_trend = px.line(daily, x="date", y="risk_score", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)
    with c2:
        st.subheader("Répartition des catégories")
        cat_choice = st.selectbox(
            "Catégorie", ["temp_category", "precip_category", "wind_category"]
        )
        counts = df[cat_choice].value_counts().reset_index()
        counts.columns = [cat_choice, "count"]
        fig_pie = px.pie(counts, names=cat_choice, values="count")
        st.plotly_chart(fig_pie, use_container_width=True)

with tab_business:
    top_n = st.slider("Top N villes", 5, 20, 10)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Villes aux températures les plus élevées")
        top_temp = (
            df.groupby("city", as_index=False)["temp_max"]
            .max()
            .sort_values("temp_max", ascending=False)
            .head(top_n)
        )
        st.plotly_chart(
            px.bar(top_temp, x="city", y="temp_max"), use_container_width=True
        )

    with c2:
        st.subheader("Villes aux plus fortes précipitations")
        top_precip = (
            df.groupby("city", as_index=False)["precipitation"]
            .max()
            .sort_values("precipitation", ascending=False)
            .head(top_n)
        )
        st.plotly_chart(
            px.bar(top_precip, x="city", y="precipitation"), use_container_width=True
        )

    st.subheader("Villes au risque moyen le plus élevé")
    risk_by_city = (
        df.groupby("city", as_index=False)["risk_score"]
        .mean()
        .sort_values("risk_score", ascending=False)
        .head(top_n)
    )
    st.plotly_chart(
        px.bar(risk_by_city, x="city", y="risk_score"), use_container_width=True
    )

    st.subheader("Pour chaque ville, la période la plus à risque")
    idx = df.groupby("city")["risk_score"].idxmax()
    worst_per_city = df.loc[
        idx, ["city", "date", "risk_score", "temp_max", "precipitation", "wind_gust"]
    ].sort_values("risk_score", ascending=False)
    st.dataframe(worst_per_city, use_container_width=True)

with tab_data:
    st.dataframe(
        df[
            [
                "city",
                "date",
                "day_of_week",
                "temp_max",
                "precipitation",
                "wind_gust",
                "risk_score",
                "risk_level",
            ]
        ].sort_values(["date", "risk_score"], ascending=[True, False]),
        use_container_width=True,
    )
    st.download_button(
        "Télécharger (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        "meteorisk_export.csv",
        "text/csv",
    )