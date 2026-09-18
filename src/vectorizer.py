import torch 
import torch.nn as nn
from model import model, processeur
from PIL import Image
import pandas as pd
import os


#Read the csv file 
vectors = []
df = pd.read_csv('../data/dataset_bag.csv')


#Store all image features in a vector
for index , line in df.iterrows():
    path_img = '../' + line['img_file'] 
    if not os.path.exists(path_img):
        continue

    img = Image.open(path_img).convert('RGB')
    inputs = processeur(images=img, return_tensors="pt")

    #We don't train the model 
    with torch.no_grad():
        features = model.get_image_features(pixel_values=inputs['pixel_values'])
        if isinstance(features, torch.Tensor):
            vector = features.detach().numpy().flatten()
        
        else:
            vector = features.pooler_output.detach().numpy().flatten()

    vectors.append(vector)


df['vector'] = vectors
df.to_pickle('../data/dataset_vectorise.pkl')
print('End of the vectorisation')