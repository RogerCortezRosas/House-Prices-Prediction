FROM apache/airflow:2.7.2

USER root

# Instala dependencias del sistema primero
RUN apt-get update && \
    apt-get install -y \
    openjdk-11-jdk \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    wget\
    && rm -rf /var/lib/apt/lists/*
# Descarga el conector MySQL JDBC (versión 8.0.x)
RUN wget https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar \
    -O /usr/share/java/mysql-connector-java.jar
# Configura variables de entorno para mysqlclient
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

USER airflow

# Copia e instala requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt