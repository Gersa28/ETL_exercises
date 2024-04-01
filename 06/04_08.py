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
url = "jdbc:mysql://localhost:3306/libreria"
propiedades = {
    "driver": "com.mysql.cj.jdbc.Driver",
    "user": "root",
    "password": "123Queso."
}

# Leemos la tabla detalle_factura de la base de datos librería
detalle_factura_df = spark.read.jdbc(
    url=url, table="detalle_factura", properties=propiedades)

# Leemos la tabla libro de la base de datos librería
libro_df = spark.read.jdbc(url=url, table="libro", properties=propiedades)

# Creamos una nueva columna que contiene el total vendido por cada registro del dataframe, 
# donde se multiplican la columna "cantidad" con "precio_unitario" del dataframe detalle_factura_df
detalle_factura_df = detalle_factura_df.withColumn(
    "total", detalle_factura_df.cantidad * detalle_factura_df.precio_unitario)

# Agrupamos el total de ventas por el id del libro
total_vendido_libro = detalle_factura_df.groupBy("id_libro").sum("total")

# Unimos la tabla detalle_factura con la tabla de libro por medio del id del libro
total_vendido_libro = total_vendido_libro.join(
    libro_df, libro_df.id == total_vendido_libro.id_libro)

# Mostramos solo la información necesaria: título y total vendido.
total_vendido_libro = total_vendido_libro.select(
    col("titulo"),
    col("sum(total)").alias("total_ventas")
).orderBy("total_ventas", ascending=False)

# Mostramos el dataframe total_vendido_libro
print(total_vendido_libro.show())
