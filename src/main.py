from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models.analyzersForm import AnalyzersForm
import json
import nanoid
import importlib
import utils
import meilisearch

client = meilisearch.Client('http://localhost:7700')
client.create_index('reports', {'primaryKey': 'id'})

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/analyze")
async def analyze(form: AnalyzersForm):
    report = {}
    with open('./configurations/analyzers.json', 'r') as f:
        data = json.load(f)
    for analyzer in form.selected_analyzers:
        analyzerInfo = data[analyzer]
        MyClass = getattr(importlib.import_module(
            analyzerInfo["path"]), analyzerInfo["className"])
        instance = MyClass()
        result = instance.run(form.ioc, form.type)
        print(result)
        report[analyzer] = result
    report["id"] = nanoid.generate('0123456789abcdefghij', 4)
    report["ioc"] = form.ioc
    utils.add_report(client, report)
    return report


@app.post("/test")
def test_docker_analyzer():
    pass


@app.post("/uploadFile")
async def uploadFile(file: UploadFile = File(...)):
    return file
