from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
import asyncio
import aiohttp
from datetime import datetime
import pandas as pd
import os

# Configurar Spark para ejecución local
def init_local_spark():
    """Inicializar Spark en modo local"""
    return (SparkSession.builder
            .master("local[*]")  # Usar todos los cores disponibles
            .appName("WebScrapingLocal")
            .config("spark.driver.memory", "2g")
            .config("spark.executor.memory", "2g")
            .getOrCreate())

# Schema para los datos
schema = StructType([
    StructField("url", StringType(), True),
    StructField("data", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("status", StringType(), True)
])

class LocalSparkScraper:
    def __init__(self, spark):
        self.spark = spark
    
    @staticmethod
    async def fetch_url(session, url):
        """Obtener datos de una URL"""
        try:
            async with session.get(url, timeout=30) as response:
                return {
                    "url": url,
                    "data": await response.text(),
                    "timestamp": datetime.now(),
                    "status": "success"
                }
        except Exception as e:
            return {
                "url": url,
                "data": str(e),
                "timestamp": datetime.now(),
                "status": "error"
            }

    @staticmethod
    async def process_batch(urls):
        """Procesar un batch de URLs"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(asyncio.create_task(
                    LocalSparkScraper.fetch_url(session, url)
                ))
            return await asyncio.gather(*tasks, return_exceptions=True)

def main():
    # Inicializar Spark
    spark = init_local_spark()
    print("Spark iniciado en modo local")

    # Crear datos de ejemplo
    urls_data = [
        ("https://www.example1.com",),
        ("https://www.example2.com",),
        ("https://www.example3.com",),
        # Agrega más URLs según necesites
    ]

    # Crear DataFrame de Spark con las URLs
    urls_df = spark.createDataFrame(urls_data, ["url"])
    print(f"Número de URLs a procesar: {urls_df.count()}")

    # Configurar el procesamiento por batches
    BATCH_SIZE = 5
    urls_list = [row.url for row in urls_df.collect()]
    batches = [urls_list[i:i + BATCH_SIZE] 
               for i in range(0, len(urls_list), BATCH_SIZE)]

    # Procesar los batches
    all_results = []
    for batch in batches:
        results = asyncio.run(LocalSparkScraper.process_batch(batch))
        all_results.extend(results)

    # Convertir resultados a DataFrame de Spark
    results_df = spark.createDataFrame(all_results, schema)

    # Mostrar resultados
    print("\nResultados del scraping:")
    results_df.show(truncate=False)

    # Guardar resultados
    output_path = "scraping_results"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Guardar como CSV
    results_df.toPandas().to_csv(
        f"{output_path}/results.csv", 
        index=False
    )

    # Guardar como Parquet
    results_df.write.mode("overwrite").parquet(
        f"{output_path}/results.parquet"
    )

    print(f"\nResultados guardados en: {output_path}")
    
    # Algunas estadísticas básicas
    print("\nEstadísticas de scraping:")
    results_df.groupBy("status").count().show()

    return results_df

if __name__ == "__main__":
    # Ejecutar el script
    try:
        df = main()
        print("Proceso completado exitosamente")
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
