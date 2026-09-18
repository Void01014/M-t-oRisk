FROM apache/airflow:2.9.3

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    requests \
    sqlalchemy \
    psycopg2-binary \
    streamlit \
    plotly

COPY dags/ /opt/airflow/dags/