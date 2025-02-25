# Backend & Frontend: app.py (Flask with Jinja templates)
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import random
import requests
from tabulate import tabulate

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)


endpoint = "http://localhost:7200/repositories/HistoriaPT"
def query_graphdb(endpoint_url, sparql_query):
    # Set up the headers
    headers = {
        'Accept': 'application/json',  # You can change this based on the response format you need
    }
    
    # Make the GET request to the GraphDB endpoint
    response = requests.get(endpoint_url, params={'query': sparql_query}, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response from the GraphDB endpoint
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


#####


#####
# Mock questions for now
test_questions = [
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Claude Monet"],
        "answer": "Leonardo da Vinci"
    },
    {
        "question": "Albert Einstein was born in Germany.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1942", "1945", "1939", "1950"],
        "answer": "1945"
    }
]

sparql_query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
prefix :  <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
    SELECT ?n ?o
    WHERE {
        ?s a :Rei .
    	?s :nome ?n .
    	?s :nascimento ?o.
    }
"""


result = query_graphdb(endpoint, sparql_query)
dates = [res["o"]["value"] for res in result["results"]["bindings"]]
for res in result["results"]["bindings"]:
    name = {res['n']['value'].split('#')[-1]}
    answer = res['o']['value'].split('#')[-1]
    options = random.sample(dates,3)
    
    if answer not in options: 
        options.append(answer)
        random.shuffle(options)
    else: 
        options.append(random.sample(dates,1))
    
    test_questions.append({
                    "question": f"qual a data de nascimento do rei {name}",
                    "options": options,
                    "answer": answer
                    })
                    

@app.route('/')
def home():
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_text = request.form.get('question')
        
        for question in test_questions:
            if question['question'] == question_text:
                correct = question['answer'] == user_answer
                session['score'] = session.get('score', 0) + (1 if correct else 0)
                return render_template('result.html', correct=correct, correct_answer=question['answer'], score=session['score'])
    
    question = random.choice(test_questions)
    return render_template('quiz.html', question=question)

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True)
