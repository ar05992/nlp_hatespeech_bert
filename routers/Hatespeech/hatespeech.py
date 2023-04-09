from fastapi import APIRouter
from tensorflow.keras.models import load_model
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np

class Entities(BaseModel):
    text: str

# model_load = pickle.load(open("model_load.pkl", "rb"))
localhost_save_option = tf.saved_model.LoadOptions(experimental_io_device="/job:localhost")
model_load = load_model('D:\\Desktop\\8th Semester\\UPDATED_FYP\\routers\\Hatespeech\\BERT_HATESPEECH',options=localhost_save_option)
label_encoder = pickle.load(open("D:\\Desktop\\8th Semester\\UPDATED_FYP\\routers\\Hatespeech\\label_encoder.pkl", "rb"))
tokenizer = pickle.load(open("D:\\Desktop\\8th Semester\\UPDATED_FYP\\routers\\Hatespeech\\tokenizer.pkl", "rb"))

router = APIRouter(
    prefix="/hatespeech",
    tags=["hatespeech"],
    responses={404: {"description": "Not found"}},
)


@router.get('/')
def index():
    return {'Message': 'Hello world'}


@router.post('/prediction')
async def prep_data(text:Entities):
    sentence = text.text
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

