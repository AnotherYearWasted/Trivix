# How to setup

## Install python:
If root required, add sudo before each command

```bash
$ sudo apt update
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```

## Install npm:
```bash
$ sudo apt update
$ sudo apt-get install npm 
```

## To run python3 virtual environment, first create .env folder and install required dependencies
```bash
$ sudo apt-get install python3.10-venv
$ python3 -m venv .env
$ source .env/bin/activate
$ python3 -m pip install -r py/requirements.txt
```

## To run node js, first install required dependencies
```bash
$ npm i
```
Javascript scripts are used to collect data
Run javascript code in background
```bash
$ source candles.sh
$ source longshort.sh
$ source liquidations.sh
```