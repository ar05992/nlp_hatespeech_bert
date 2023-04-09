from fastapi import APIRouter
from tensorflow.keras.models import load_model
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np

model_load = load_model('C:/Users/huzai/Desktop/FYP/ModelsApis/UPDATED_FYP/routers/Hatespeech/BERT_HATESPEECH')
label_encoder = pickle.load(open("C:/Users/huzai/Desktop/FYP/ModelsApis/UPDATED_FYP/routers/Hatespeech/label_encoder.pkl", "rb"))
tokenizer = pickle.load(open("C:/Users/huzai/Desktop/FYP/ModelsApis/UPDATED_FYP/routers/Hatespeech/tokenizer.pkl", "rb"))

class Entities(BaseModel):
    text: str

def prep_data(text):
    sentence = text
    tokens = tokenizer(sentence, max_length=150, truncation=True, 
                       padding='max_length', 
                       add_special_tokens=True, 
                       return_tensors='tf')
    tokens = {'input_ids': tf.cast(tokens['input_ids'], tf.float64), 'attention_mask': tf.cast(tokens['attention_mask'], tf.float64)}
    probs = model_load.predict(tokens)[0]
    pred = np.argmax(probs)
    pred = label_encoder.inverse_transform([pred])
    return {"Probability":str(np.round(probs,3)),
            "Prediction":str(pred[0])}

while(True):
    txt=input("Enter Text to predict: ")
    if txt == 'e':
        break
    res=prep_data(txt)
    print(dict(res))
   
