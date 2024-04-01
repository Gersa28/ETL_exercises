# Librerías a importar
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Crear la sesión de spark
spark = SparkSession  \
    .builder \
    .appName("El total de ventas por libro") \
    .config('spark.driver.extraClassPath', "mysql-connector-j-8.0.32.jar") \
    .getOrCreate()

# Propiedades para la conexión usando spark jdbc
url = "jdbc:mysql://localhost:3306/__________"
propiedades = {
    "driver": "com.mysql.cj.jdbc.Driver",
    "user": "__________",
    "password": "__________."
}

# Leemos la tabla detalle_factura de la base de datos librería
detalle_factura_df = spark.read.jdbc(
    url=url, table="__________", properties=propiedades)

# Leemos la tabla libro de la base de datos librería
libro_df = spark.read.jdbc(url=url, table="__________", properties=propiedades)

# Creamos una nueva columna que contiene el total vendido por cada registro del dataframe, 
# donde se multiplican la columna "cantidad" con "precio_unitario" del dataframe detalle_factura_df
detalle_factura_df = detalle_factura_df.withColumn(
    "total", detalle_factura_df.__________ * detalle_factura_df.__________)

# Agrupamos el total de ventas por el id del libro
total_vendido_libro = detalle_factura_df.__________("id_libro").__________("total")

# Unimos la tabla detalle_factura con la tabla de libro por medio del id del libro
total_vendido_libro = total_vendido_libro.join(
    libro_df, libro_df.__________ == total_vendido_libro.__________)

# Mostramos solo la información necesaria: título y total vendido.
total_vendido_libro = total_vendido_libro.select(
    col("titulo"),
    col("__________").alias("total_ventas")
).orderBy("total_ventas", ascending=__________)

# Mostramos el dataframe total_vendido_libro
print(__________)