# RisingBrain

The goal of this project is to develop a phone operating system that replaces the traditional UI of an Android-based smartphone with ChatGPT. The AI will manage control of all apps via plugins, which can be prompted by the user.
[![CI/CD](https://github.com/ttt246/RisingBrain/actions/workflows/main.yml/badge.svg)](https://github.com/ttt246/RisingBrain/actions/workflows/main.yml)
[![CI/CD Develop](https://github.com/ttt246/RisingBrain/actions/workflows/main.yml/badge.svg?branch=develop)](https://github.com/ttt246/RisingBrain/actions/workflows/main.yml)
## 1. Description

#### 1.1 Achievement
Develop a langchain plugin that sends Android system notifications to the user. Should be able to use a langchain agent.
Allow user to launch browser app on a specific webpage or to search an image , and others more. 

<p align='center'>
  <img align='center' src='assets/img/achievement.gif' width='250px' height='500px'/>
</p>

#### 1.2 Architecture
<p align='center'>
  <img align='center' src='assets/img/langchain_architecture.jpg' width="30%"/>
</p>

- make app documentation and embed it.
- embed the query that risingphone sends to local llm
- calculate similarity between embedded app documentation and query and get the best similar app
- get completion based on query and app data using langchain
- send the result to risingphone using firebase clouding message

#### 1.3 Goal
Android-based smartphone operating system that utilizes ChatGPT as the primary user interface.
Control of all apps through AI prompting and execution via plugins.


## 2. Installing / Getting started
#### 2.1 how to run on local


    git clone https://github.com/ttt246/RisingBrain.git
    pip install virtualenv
    virtualenv venv
    pip install -r requirements.txt
    set flask = app.py
    run flask


#### 2.2 Create firebase project
Create firebase project and take its credentials named .json from Google Cloude IAM. 
#### 2.3 Get Heroku Api key
Deploy it to Heroku in CI/CD automatically whenever there are some changes in main or develop branch.
#### 2.4 Set Github Secrets With its Access Keys
All credentials including openai, replicate and pinecone are shared with Github Secrets to be referenced by Unit Tests of CI/CD on its building

## 3. Developing
#### 3.1.1 make app documentation

| Prompt Template |
| ------------ |
| If user is going to run web browsers such as Firefox, Google Chrome, Safari, Microsoft, Opera, Internet Explorer, Mosaic, Chromium, Brave, etc, please answer belowing json format. <br> The url user is going to open can exist or not. If user doesn't say exact url and want to open some sites, you have to find the best proper url. If user don't say url or you can't find proper url, please set url to "http://www.google.com". <br><br>{"program": "browser", "url": "website url that user is going to open"} |
| If user is going to send notification or alert, please answer belowing json format. If user didn't say what to send, please set content to "This is notification" <br><br>{"program": "alert", "content": "text that user is going to send"} |
| If user is going to say about a image with its description to search, please answer belowing json format. . {""program"": ""image"", ""content"": ""description of the image that user is going to search""}| 
| If user is going to ask about a image, please answer belowing json format. . {""program"": ""image"", ""content"": ""description of the image that user is going to search""}| 

#### 3.1 embedding & relatedness
- embed app documentation
- get completion using langchain
- send message using firebase clouding message and firestore
- management its vectoring data within pinecone

## 4. Testing

- pytest



    python -m pytest




- saucelabs test

  You can configure ./sauce/config.yml with your test cases and then run the saucelab unit tests with below command line.



    saucectl run




## 5. CI/CD & Deploy
- Lint With Black
- Integrated all Unit Tests
- Integrated Deployment Workflow

## Contributing
Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!