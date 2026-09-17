import psycopg2
from pgvector.psycopg2 import register_vector
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()

#Handshake co with docker 
co = psycopg2.connect(
    dbname=os.getenv("DB_NAME") ,
    user=os.getenv("DB_USER"),
    password =os.getenv("DB_PASSWORD"),
    host = 'localhost',
    port = '5432',
)
co.autocommit = True
cur = co.cursor()


#Enable the vector extension in PostgreSQL
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
register_vector(co)

#Setup the dataBase in docker 
cur.execute("DROP TABLE IF EXISTS handbags;")
cur.execute("""
    CREATE TABLE handbags (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(255),
        model VARCHAR(255),
        price VARCHAR(50),
        img_file VARCHAR(255),
        vector vector(2048)
    );
""")

#Store the data from the pickle file in the database
df = pd.read_pickle('../data/dataset_vectorise.pkl')

for index , line in df.iterrows():
    cur.execute("""
        INSERT INTO handbags (brand, model, price, img_file, vector)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        line['brand'], 
        line['model'], 
        line['price'], 
        line['img_file'], 
        line['vector']  
    ))

cur.close()
co.close()
print("Storage in DB done!")