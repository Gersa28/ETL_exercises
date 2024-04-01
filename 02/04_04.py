# Librerías a importar
from pyspark.sql import SparkSession

# Crear la sesión de spark
spark = SparkSession  \
    .builder \
    .appName("Motrar los libros de nuestra base de datos Librería") \
    .config('spark.driver.extraClassPath', "mysql-connector-j-8.0.32.jar") \
    .getOrCreate()

# Propiedades para la conexión usando spark jdbc
url = "jdbc:mysql://localhost:__________/__________"
propiedades = {
    "driver": "com.mysql.cj.jdbc.Driver",
    "user": "__________",
    "password": "__________"
}

# Leemos la tabla libro de la base de datos librería
libro_df = spark.read.jdbc(url=url, table="__________", properties=propiedades)

# Se muestra en pantalla los libros que tenemos
__________
