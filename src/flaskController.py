from flask import Flask, render_template, request, jsonify, make_response
from openai import OpenAI
import requests
import random
import json
import os

# Flask init
app = Flask(__name__)

# OpenAI API Key 
OPENAI_API_KEY = "sk-proj-67o9ARwUNPngj69gW2LiT3BlbkFJxCf6OmyYRCETIMwK54aQ"

# API links
API_LINKS = ['http://numbersapi.com/random/trivia',
             'http://numbersapi.com/random/year',
             'http://numbersapi.com/random/date',
             'http://numbersapi.com/random/math']

# Setting client key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", OPENAI_API_KEY))

def getNumFact(num=None):
    """Queries one of the API_LINKS and returns the fact for GPT to interpreit.

    Args:
        num (int, optional): Given number to get fact about. Defaults to None.

    Returns:
        _type_: Returns json
    """
    if (num):
        response = requests.get("http://numbersapi.com/" + str(num)).text
    else:
        random.seed(None)
        randomURL = random.choice(API_LINKS)
        response = requests.get(randomURL).text
    print("INFO: API Responded with => " + response)
    return response

def getCompletion(prompt):
    """Initializes a query to completions and sends a prompt to the api. Once the api sends a response, 
    it will obtain the message and return it. 

    Args:
        prompt (String): A string prompt of what to query the API

    Returns:
        String: Returns a string of the chatGPT api response
    """
    print("INFO: User Prompt => " + prompt)
    
    getNumFactFunction = [
        {
            "name": "getNumFact",
            "description": "Retrieve and elaborate on the given fact",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {
                        "type": "number",
                        "description": "Number to get fact about."
                    },
                },
            },
        }
    ]
    
    # Generates a response to probe the user for number inquiries
    # If number is provided or question is formulated in a way that asks a number question, call getNumFact
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chat bot that gives facts about numbers."},
            {"role": "user", "content": prompt}],
        functions=getNumFactFunction,
        function_call="auto",
        temperature=0.5
    )
    
    # If response has a function call, proceed. Else return default message
    if dict(response.choices[0].message).get('function_call'):
        response = response.choices[0].message
        
        # Which function call was invoked
        functionCalled = response.function_call.name
        
        # Extracting the arguments
        functionArgs  = json.loads(response.function_call.arguments)
        
        available_functions = {
            "getNumFact": getNumFact,
        }
        
        fuction_to_call = available_functions[functionCalled]
        
        # Cleans up response, if function args are not empty, add them, if they are empty, exclude from call
        if (functionArgs != "{}"):
            prompt = fuction_to_call(dict(functionArgs).get('number'))
        else: prompt = fuction_to_call()
        
        # Query GPT to elaborate on given fact, providing more information about the fact
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Elaborate on the following fact" + prompt}
            ],
            temperature=0.5
        ).choices[0].message.content
        
        print("INFO: GPT Response: " + str(response))
        return response
    print("INFO: GPT Response: " + str(response))
    return response.choices[0].message.content

@app.route("/", methods=['POST', 'GET'])
def index():
    """Flask interface with the front end, accepts user input and sends response based off get_completion function

    Returns:
        Template: Renders the template for the html page`
    """
    if request.method == 'POST':
        # Gets prompt from form
        prompt = request.form['prompt']
        # Sets response to GPT response
        response = getCompletion(prompt)
        # Adds response to front end
        return jsonify({'response': response})
    return render_template('index.html')

def init():
    """Basic init to start flask (no more socketio)
    """
    Flask.run(app, debug=True)

if __name__ == '__main__':
    Flask.run(app, debug=True)