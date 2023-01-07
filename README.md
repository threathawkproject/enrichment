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
To run the module do the following
- go to `src` directory
```bash
$ cd src
```
- run the follwoing command
```bash
$ uvicorn main:app --reload
```
