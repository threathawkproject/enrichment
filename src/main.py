from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models.analyzersForm import AnalyzersForm
import json
import nanoid
import importlib
import utils
import meilisearch


# Initialize the Meiisearch client
client = meilisearch.Client('http://localhost:7700')
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
    return {"message": "ThreatHawk"}


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


        result = instance.run(form.ioc, form.type, form.root_id)

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
