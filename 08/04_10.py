# Librerías a importar
from pyspark.sql import SparkSession

# Crear la sesión de spark
spark = SparkSession  \
    .builder \
    .appName("Unión de la tabla cliente y tabla empleado") \
    .config('spark.driver.extraClassPath', "mysql-connector-j-8.0.32.jar") \
    .getOrCreate()

# Propiedades para la conexión usando spark jdbc
url = "jdbc:mysql://localhost:3306/__________"
propiedades = {
    "driver": "com.mysql.cj.jdbc.Driver",
    "user": "__________",
    "password": "__________."
}

# Leemos los datos de la tabla cliente
cliente_df = spark.read.jdbc(url=url, table="__________", properties=propiedades)
cliente_df = cliente_df.drop(*["telefono", "id"])

# Leemos los datos de la tabla empleado
empleado_df = spark.read.jdbc(url=url, table="__________", properties=propiedades)
empleado_df = empleado_df.drop("id")

#Unimos las dos tablas cliente y empleado
comunidad_df = cliente_df.union(__________)

# Mostramos el dataframe comunidad_df que contiene la información de los clientes y colaboradores
print(comunidad_df.show())

#Cargamos la informacion del dataframe comunidad_df en una tabla llamada comunidad
comunidad_df.__________.jdbc(
    url=url, table="__________", mode="overwrite", properties=propiedades)
