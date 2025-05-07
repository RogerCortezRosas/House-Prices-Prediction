# House-Prices-Prediction

![imagen](images/houses.jpg)

Este proyecto tiene como objetivo predecir los precios de casas utilizando técnicas de aprendizaje automático. Se emplea un conjunto de datos con características como  número de habitaciones, baños, tamaño del terreno y antigüedad. Aplicando el modelo de RandomForest para obtener predicciones precisas. Además, se realiza una exploración de datos y análisis estadístico previo para entender las variables más influyentes. Los resultados permiten estimar el valor de propiedades y apoyar decisiones de compra o venta.


## 📁 Estructura del Proyecto
- dags/ : Esta carpeta contiene el cosigo fuente de los DAGs(Directed Acyclic Graphs) , para orquestar el flujo de trabajo . Las tareas del DAG permiten automatizar procesos como la extraccion ,transformacion y carga(ETL)
- env/ : Entorno virtual para ejecucion  en el entorno local.
- model/ : Contiene los codigos de el API, llamda al modelo de ML , creacion y experimentacion del modelo  , Analisis exploratorio , archivo docker y  librerias a importar.
- scripts/ : Esta carpeta contiene el codigo para realizar el ETL , que es llamdao a traves de una tarea que conforman el DAG.
- docker-compose.yaml : Archivo que contiene el codigo para crear los contenedores.
- dockerfile : Archivo que contiene el codigo para crear la imagen de airflow y instalar dependencias.
- load : notebook para carga de data al DataLake.

## ETL

La tareas de Extraccion , Transformacion y Carga se realizan en una tarea con python y pandas que consiste en lo siguiente:

- Extraer: Se esxtrae la informacion de una base de datos Dat Lake donde la data aun no es transformada

- Transformacion: En el proceso de transformacion se realiza la eliminacion de columnas quet tengan mas de 80% de nulos y ceros , ademas se realiza un encoding a las variables categoricas con tecnicas como kfold_target_encoding y ordinal_encoding .

- Carga :  Una vez limpiado y transformado la data se carga a una nueva tabla que seria nuetro Data WareHouse.

- Eliminacion : Cuando es transformada y cargada con exito la informacion se elimina los registros del DataLake

## API

El Api cosnta de un metodo llamado /predict , el cual recibe de entrada un documento csv con la informacion de la casa.
Se realiza la validacion del formato y contenido recibido con el manejo de errores usando la mejores  practicas.

## Modelo

El modelo utilizado es RandomForestRegressor de la librerias de sckit-learn la cual es entrenada en el archivo Experimental_model.ipynb y se gurada el modelo en el archivo modelo.pkl.Posteriormente este archivo es cargado en Modelprediction.py para hacer la prediccion sin la necesidad de re-entreanr el modelo. Este codifgo cuenta con el manejo de errores adecuado para mostrar al usuario y ademas se almacena el error tecnico en los registros.

## ⚒️ Tecnologias⚒️


<br/>
<div align="center">
    <!-- Lenguajes de Programación -->
    <img src="https://skillicons.dev/icons?i=python" />
    <!-- Bibliotecas y Frameworks de Machine Learning -->
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/scikitlearn/scikitlearn-original.svg" width="60" height="60" />
    <img src="https://skillicons.dev/icons?i=git,github,vscode" />
    <!-- Entornos de Despliegue y MLOps -->
    <img src="https://skillicons.dev/icons?i=fastapi" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" width="60" height="60" />
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/numpy/numpy-original-wordmark.svg" width="60" height="60" />
    <img src="images/airflowLogoM.png" width="60" height="60" />
    <img src="images/dockerLogo.png" width="60" height="60" />
    <img src="images/PlotlyLogo.png" width="60" height="60" />
    <img src="images/PoweLogo.png" width="60" height="60" />

</div>

## Ejecucion  ⚙️

Ejecuta los siguientes comandos para la ejecucion en tu entorno local

  - git clone https://github.com/RogerCortezRosas/House-Prices-Prediction.git
  
  
  Ejecuta el siguiente comando para construccion de contnedores
  
  - docker-compose up --build

## Contacto

- Autor : Rogelio Cortez Rosas
- linkedin:https://www.linkedin.com/in/rogelio-cortez-rosas
- email : rcortezrosas@gmail.com

