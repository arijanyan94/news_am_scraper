# News.am Scraper and Analizer

## Introduction
A Single page web application, which scraps the data from [News.am](https://news.am/eng/) "Top News" section, highlights the faces 
on the cover images, and summarizes the text article. The webpage uses lazy loading technique, so when the button is clicked,
the scraping is done first and rendered immediately to the page, afterwards the images are processes and rendered one by one,
and finaly the text summarization is done one by one as well. The purpose is that the user won't wait to long for the loading.
You can take a look at the webpage [here](http://54.153.75.61:5000/).

## Deployment
For the server is used this one: "Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.1.0 (Ubuntu 20.04)", with 2 CPUs and a GPU.
The reason is that the code uses text abstractive summarization model (Bart large CNN), and computational power is needed.

## Instalation
Clone the repo, create and activate the virtual environment and run

		pip install -r requirements.txt

**NOTE!!! LLM model requires latest version of pytorch, which on its place requires Python >= 3.9**

The **dlib** package may take a couple of minutes to build, kindly wait.

## Usage
After the installations you can run the following command to start the webapp

	python app.py

To stop the application, termiante the program with **CTRL + C**
During the first run of the LLM model will be downloaded (~ 1.6Gb) and then the app will be rendered on your localhost 5000 port.
Click on the **Load Articles** button, and you will get the results in seconds.

## Possible Improvements
Implement a request queue, for example Rabbit, to control the requests.
Build a Docker container, and run from it in AWS EC2
Detach the face recognition and summarization function to another services, for example SageMaker, or Lambda GPU
Optimization

## Citation
Author - Arsen Arijanyan
Email  - arsen.aridjanyan@gmail.com
