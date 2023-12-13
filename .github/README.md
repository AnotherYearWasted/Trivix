# Trivix - Market Analysis using Machine Learning

Trivix is an ongoing project for market analysis using machine learning techniques. The project is written in Python and currently in development. It is primarily intended for private use but may be opened in the future.

## Index

* [1. General infomation](#1-general-infomation)
* [2. Structures](#2-structure)
* [3. Installation](#3-installation)
* [4. Usage](#4-usage)
* [5. Contributing](#5-contributing)
* [6. Code of conduct](#6-code-of-conduct)
* [7. Funding](#7-funding)
* [8. License](#8-license)

## 1. General infomation

Trivix is a tool for analyzing financial market data using machine learning algorithms. It offers a range of features including data import, data exploration, clustering, linear regression, and predictive modeling. The tool is designed to make it easier for users to explore and understand complex financial data, enabling them to make informed investment decisions.

For more information on our project's code of conduct, contributing guidelines, funding sources, and licensing, please refer to the respective sections below.

## 2. Structure

The directory structure should look like this:

* `api` : API Directory that contains `api.py` functions to call API requests
* `data` : CSV for Model Training
* `.github` : GitHub Directory for Documents about Trivix
* `model` : Python Directory for Saved Model
* `getdata.py` : This file get data and extract data to .data
* `trivix.py` : This script runs the main code
* `requirements.txt` : Necessary Dependecies

## 3. Installation

### Requirements
Python3 or NodeJS

### Getting Started
```bash
$ git clone https://github.com/jaibtdou/Trivix.git
```

Install python3.10
```bash
$ sudo apt update
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```

Install NodeJS
```bash
$ sudo apt update
$ sudo apt-get install npm 
```

To run python3 virtual environment, first create .env folder and install required dependencies
```bash
$ sudo apt-get install python3.10-venv
$ python3 -m venv .env
$ source .env/bin/activate
$ python3 -m pip install -r py/requirements.txt
```

How to download data
In `py/getdata.py`, modified as follow:

By default, the script collects data in the previous 30 days and export to a csv file, depending on which function the user calls

Run the code:
```bash
source getdata.sh
```

## 4. Usage

Trivix use Python to run API requests directedly to Binance API service. Trivix also has Asynchronous API function to call APIs faster than normal requests.

Here are examples of how to run the code. In Terminal, run:

```bash
$ python trivix.py
```

## 5. Contributing

If you're interested in contributing to Trivix, we welcome your input. Whether you're a seasoned developer or just starting out, there are many ways you can help improve the project. You can contribute code, documentation, bug reports, or feature requests. To get started, check out the contributing guidelines in the [Contributing](CONTRIBUTING.md) file.

## 6. Code of conduct

We want everyone who participates in Trivix to feel welcome and respected. To ensure that happens, we've established a code of conduct that outlines our expectations for behavior. You can read the full text of the code of conduct in the [Code of Conduct](CODE_OF_CONDUCT.md) file.

## 7. Funding

Trivix is currently self-funded and developed on a volunteer basis. If you're interested in supporting the project financially, we welcome your contributions. You can donate through our [Open Collective][https://opencollective.com/phong-thien] page.

## 8. License

Trivix is released under the [MIT License](LICENSE.md). This means you're free to use, modify, and distribute the software for any purpose, including commercial use. However, we provide no warranties or guarantees, so use the software at your own risk.