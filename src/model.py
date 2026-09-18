import torch 
import torch.nn as nn
import pandas as pd
import numpy as np
import os
from transformers import CLIPProcessor , CLIPModel # -> Import a vision model train for handbag


#Setup the vision model 
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processeur = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")




