from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.analyzersForm import AnalyzersForm
import json
import nanoid
import importlib
import utils
import meilisearch
import consts
import os

# Initialize the Meiisearch client
MEILI_URL = os.getenv("MEILI_URL", default="http://localhost:7700")


client = meilisearch.Client(MEILI_URL)
client.create_index('reports', {'primaryKey': 'id'})

# Initialize FastAPI
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
    return {"message": "ThreatHawk Enrichment is Running!"}


@app.get("/get_investigation_analyzers")
async def get_analyzers(analyzer_type: str | None = None):
    print(analyzer_type)
    type = analyzer_type if analyzer_type is not None else None
    found = utils.check_type(type)
    print(found)
    if (type is not None) and (len(type) > 0) and found:
        try:
            analyzers = utils.get_analyzers(type)
            return analyzers
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")    
    else:
        raise HTTPException(status_code=400, detail="please enter a valid analyzer type!")

@app.get("/analyzers")
async def analyzers():
    # Load the configuration file
    with open("../src/configurations/analyzers.json") as jsonFile:
        configurations = json.load(jsonFile)
        jsonFile.close()

    return configurations


@app.get("/iocTypes")
async def iocTypes():
    # Load the ioc types file
    with open("../src/configurations/iocTypes.json") as jsonFile:
        configurations = json.load(jsonFile)
        jsonFile.close()

    return configurations


@app.post("/analyze")
async def analyze(form: AnalyzersForm):
    # Initialize the report
    report = {}

    # Load the configuration file
    with open('./configurations/analyzers.json', 'r') as f:
        configuration = json.load(f)

    # Instantiate the selected analyzers
    for analyzer in form.selected_analyzers:
        analyzerConfig = configuration[analyzer]
        analyzerClass = getattr(importlib.import_module(
            analyzerConfig["path"]), analyzerConfig["className"])
        instance = analyzerClass()


        result = instance.run(form.ioc, form.type, form.node_id)

        # if file is not None:
        #     result = instance.run(file, form.type)
        # else:
        #     result = instance.run(form.ioc, form.type)

        # Add the data returned by the analyzer to the report
        report[analyzer] = result

    # Finalize the report
    report["id"] = nanoid.generate('0123456789abcdefghij', 4)
    # if file is not None:
    #     report["ioc"] = file.filename

    # else:
    report["ioc"] = form.ioc

    # Add the report to Meiisearch
    utils.add_report(client, report)

    return report



@app.post("/test")
def test_docker_analyzer():
    pass
