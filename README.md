# Linkedin Web scraper

## Table of contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Setup](#setup)
* [Example](#example)


## Introduction
A Python class that connects to Linkedin.com, using Selenium with a headless browser, search for job offers that meet certain criteria and  export the scraped data to a CSV file.


## Technologies
Project is created with:
* Python 3.8.9
* Selenium 3.141.0


## Setup
You need to manually download the webdriver for Firefox "Geckodriver" before you can use the python class and put on your system PATH. Also you need to set up the variables 'csv_path' and 'targets' in the script, the first is the path where the csv files are saved and the second are keywords of your interest that the job description must have. 

## Example

<img src="./images/screenshot1.png" width="650" height="800">
<img src="./images/screenshot2.png" width="650" height="800">
<img src="./images/screenshot3.png" width="650" height="800">
