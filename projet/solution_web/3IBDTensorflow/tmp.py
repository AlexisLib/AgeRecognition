from keras.models import load_model
from config import *

model = load_model(crop_linear_model_framework_to_load)
model = load_model(linear_model_framework_to_load)
