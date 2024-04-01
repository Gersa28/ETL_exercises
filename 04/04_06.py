# Librerías a importar
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Crear la sesión de spark
spark = SparkSession  \
    .builder \
    .appName("La cantidad de libros vendidos") \
    .config('spark.driver.extraClassPath', "mysql-connector-j-8.0.32.jar") \
    .getOrCreate()

# Propiedades para la conexión usando spark jdbc
url = "jdbc:mysql://localhost:3306/libreria"
propiedades = {
    "driver": "com.mysql.cj.jdbc.Driver",
    "user": "root",
    "password": "123Queso."
}

# Leemos la tabla detalle_factura de la base de datos librería
detalle_factura_df = spark.read.jdbc(
    url=url, table="detalle_factura", properties=propiedades)

# Agrupamos la cantidad de ventas por el id del libro
cantidad_libros_vendidos_df = detalle_factura_df.groupBy(
    "id_libro").sum("cantidad")

# Mostramos la cantidad de libros vendidos por el id del libro
print(cantidad_libros_vendidos_df.show())

# Leemos la tabla libro de la base de datos librería
libro_df = spark.read.jdbc(url=url, table="libro", properties=propiedades)

# Unimos el dataframe cantidad_libros_vendidos_df con la tabla de libro por medio del id del libro
cantidad_libros_vendidos_df = cantidad_libros_vendidos_df.join(
    libro_df,
    libro_df.id == cantidad_libros_vendidos_df.id_libro)

# Seleccionamos solo la información necesaria: título, puntación y cantidad vendida.
cantidad_libros_vendidos_df = cantidad_libros_vendidos_df.select(
    col("titulo"),
    col("puntuacion"),
    col("sum(cantidad)").alias("cantidad_vendidos")
).orderBy("cantidad_vendidos", ascending=True)

# Mostramos el dataframe cantidad_libros_vendidos_df
cantidad_libros_vendidos_df.show()
