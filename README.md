## ThreatHawk Enrichment

# Table of Contents
- [Installation](#installation)
- [How to run](#how-to-run)

## Installation
To install do the following
- clone the repository
```bash
$ git clone https://github.com/threathawkproject/enrichment.git
```
- install the dependencies
go into the module
```bash
$ cd enrichment
```
- install the dependencies via pip
```python
$ pip install -r requirements.txt
```

## How to run

### Meilisearch
Running Meilisearch
- Get docker image
```bash
$ docker pull getmeili/meilisearch:v0.30
```
- run meilisearch
```bash
$ docker run -it --rm -p 7700:7700  -v ./meili_data:/meili_data getmeili/meilisearch:v0.30 meilisearch --env="development"
```
### Enrichment module
To run the module do the following
- go to `src` directory
```bash
$ cd src
```
- run the follwoing command
```bash
$ uvicorn main:app --reload
```
