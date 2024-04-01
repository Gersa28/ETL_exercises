# Librerías a importar
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Crear la sesión de spark
spark = SparkSession  \
    .builder \
    .appName("La cantidad facturas por cliente") \
    .config('spark.driver.extraClassPath', "mysql-connector-j-8.0.32.jar") \
    .getOrCreate()

# Propiedades para la conexión usando spark jdbc
url = "jdbc:mysql://localhost:3306/libreria"
propiedades = {
    "driver": "com.mysql.cj.jdbc.Driver",
    "user": "root",
    "password": "123Queso."
}

# Leemos la tabla factura de la base de datos librería
factura_df = spark.read.jdbc(url=url, table="factura", properties=propiedades)

# Agrupamos la cantidad de facturas por el id del cliente
cliente_cantidad_factura_df = factura_df.groupBy("id_cliente").count()

# Leemos los datos de la tabla cliente
cliente_df = spark.read.jdbc(url=url, table="cliente", properties=propiedades)

# Unimos el dataframe cantidad_facturas_cliente_df con la tabla de cliente por medio del id del cliente
cliente_cantidad_factura_df = cliente_cantidad_factura_df.join(
    cliente_df,
    cliente_df.id == cliente_cantidad_factura_df.id_cliente)

# Seleccionamos solo la información necesaria: id del cliente, nombre, apellido, cantidad de facturas
cliente_cantidad_factura_df = cliente_cantidad_factura_df.select(
    col("id"),
    col("nombre"),
    col("apellido"),
    col("count").alias("cantidad_facturas")
).orderBy("cantidad_facturas", ascending=False)

# Mostramos el dataframe cantidad_facturas_cliente_df
print(cliente_cantidad_factura_df.show())

#Cargamos la informacion del dataframe cantidad_facturas_cliente_df en una tabla llamada cliente_cantidad_factura
cliente_cantidad_factura_df.write.jdbc(
    url=url, table="cliente_cantidad_factura", mode="overwrite", properties=propiedades)
