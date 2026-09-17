import torch 
import torch.nn as nn
from torchvision.models import resnet50 , ResNet50_Weights # -> Import a vision model train for handbag
from torchvision import transforms
from PIL import Image
import pandas as pd
import numpy as np
import os
vectors = []

#Download the pre-trained ResNet50 weights
model = resnet50(weights=ResNet50_Weights.DEFAULT)

#Remove the final classification layer
modele_extractor = nn.Sequential(*list(model.children())[:-1])
modele_extractor.eval()

#resnet50 accept only a square format for the image (224*224)
transformation = transforms.Compose([
    transforms.Resize((224, 224)),       
    transforms.ToTensor(),               
    transforms.Normalize(               
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    )
])

#Read the csv file 
df = pd.read_csv('../data/dataset_bag.csv')


#Store all image features in a vector
for index , line in df.iterrows():
    path_img = '../' + line['img_file'] 
    if not os.path.exists(path_img):
        continue

    img = Image.open(path_img).convert('RGB')
    tenseur = transformation(img).unsqueeze(0)

    #We don't train the model 
    with torch.no_grad():
        vector = modele_extractor(tenseur).numpy().flatten()

    vectors.append(vector)


df['vector'] = vectors
df.to_pickle('../data/dataset_vectorise.pkl')
print('End of the vectorisation')