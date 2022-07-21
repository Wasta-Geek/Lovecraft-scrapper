# Lovecraft-scrapper

[Test] The goal is simple: create a python program that retrieves data from a specific URL and print some related statistics

## Usage

    usage: main.py [-h] [url]

    Scrap a HPL URL and print some data.

    positional arguments:
      url         the target URL to scrap

    optional arguments:
      -h, --help  show this help message and exit


## Requirements

>- \>= Python 3.8 (not tested below versions)
>- beautifulsoup4==4.11.1
>- pandas==1.4.3
>- pre-commit==2.20.0

## Install

    pip install -r requirements.txt

## Pre-commit install (optional)

Some hooks are executed to enforce code quality (PEP respect, valid requirements.txt, ...),
to install them, execute the following command:

    pre-commit install

## Test

Some basics tests can be launched to test the project against various URL with the following command:

    python3 -m unittest tests/test_main.py
