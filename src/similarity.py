import sys
from model import model, processeur
from PIL import Image
from dotenv import load_dotenv
from database import co_db
import pandas as pd
import torch 
import os
import psycopg2

def search_bag(original_img):
    inputs = processeur(images=original_img, return_tensors="pt")# -> Convert the input img into the good format to CLIP

    #Don't train the AI
    with torch.no_grad():
        #Extratc the pixel  from the the object features
        features = model.get_image_features(pixel_values=inputs['pixel_values'])
        if isinstance(features, torch.Tensor):
            vector = features.detach().numpy().flatten()
        else:
            vector = features.pooler_output.detach().numpy().flatten()

    #Co to the db 
    load_dotenv()
    co = co_db()
    curr = co.cursor()

    #Calculate the distance between the target vector and the vectors in the database
    curr.execute("""
        SELECT brand, model, price , img_file , vector  <=> %s::vector AS distance
        FROM handbags
        ORDER BY distance ASC
        LIMIT 1;
    """, (vector.tolist(),))

    result = curr.fetchall()
    
    curr.close()
    co.close()
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Using : python3 similarity.py <img_path>")
        sys.exit(1)

    #Input img 
    raw_img = sys.argv[1]
    original_img = Image.open(raw_img)
    
    result = search_bag(original_img)

    for line in result:
            brand, model, price, img_file, distance = line
            print(f"Score: {distance:.4f} | {brand} - {model} (~{price})")

    if distance <= 0.04:
        print(f"The exact model is the <{model}> bag from {brand}, usually priced at around {price}.")
    elif distance <= 0.09:
        print(f"The model is similar to the <{model}> bag from {brand}, usually priced at around {price}.")
    else :
        print('No arcticle find')