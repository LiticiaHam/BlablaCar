import requests
from time import sleep
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import datetime

# Initialiser la session Spark
spark = SparkSession \
    .builder \
    .appName("get-data") \
    .master("local[*]") \
    .getOrCreate()

# Clé d'API
headers = {'Authorization': 'Token 9_YiYsUW93g6NExNmInqhA'}

while True:
    try:
        # Utiliser la date actuelle
        date_today = datetime.now().strftime("%Y-%m-%d")
        
        # Requête API
        r = requests.get(f"https://bus-api.blablacar.com/v1/fares?date={date_today}", headers=headers)
        
        # Vérification du statut de la réponse
        if r.status_code == 200:
            # Convertir les données en DataFrame Spark
            df = spark.createDataFrame(r.json()["fares"]).withColumn("timestamp_ingestion", current_timestamp())
            
            # Écriture des données
            df.coalesce(1).write.format("json").mode("overwrite").save("hdfs://namenode:9000/data/data_bbc")
        else:
            print(f"Erreur lors de la récupération des données: {r.status_code}")
        
    except Exception as e:
        print(f"Erreur rencontrée : {e}")
    
    # Pause de 30 secondes
    sleep(30)
