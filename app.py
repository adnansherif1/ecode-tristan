from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routes.v1.iris_predict import app_iris_predict_v1
# from routes.home import app_home
import json
import nltk
# import jsonify
from schema import DataInput, PredictionResponse
from classifier import select_and_classify, model
import pickle


app = FastAPI(title="Autofiller", description="API for autofilling AI", version="1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def load_model():
    nltk.download('stopwords')
    nltk.download('wordnet')
    model.clf = pickle.load(open("classifier.sav", 'rb'))
    model.clf_sel = pickle.load(open("classifier_sel.sav", 'rb'))
    model.td = pickle.load(open("td.sav", 'rb'))
    model.td_sel = pickle.load(open("td_sel.sav", 'rb'))
    with open("category", "r") as fh:
        model.category = json.load(fh)[0]
    with open("labels", "r") as fh:
        model.labels = json.load(fh)[0]
    with open("unique", "r") as fh:
        model.unique = json.load(fh)[0]
    print("models loaded")


@app.post('/predict',tags=["Predictions"],response_model=PredictionResponse,description="classify input boxes")
async def get_prediction(data_input: DataInput):
    
    html = data_input.html
    user_data = data_input.user_data
    
    out = select_and_classify(html,user_data,model.labels,model.unique,model.category,model.td,
                               model.clf,model.td_sel,model.clf_sel)
    return {"out":out}

@app.get('/hello',tags=["hello"],response_model=PredictionResponse,description="hello world")
async def get_prediction():

    return {"out":"Hello world"}
