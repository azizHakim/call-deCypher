import os
import csv
import json
import urllib
import logging
import threading
from pydantic import ValidationError
from flask import request, jsonify, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from flasgger import swag_from
from flask_openapi3 import Info, Tag

from app import app
from app.facts_rag import get_facts
from app.models import SubmitQuestionAndUrls, GetQuestionAndFactsResponse



# default route
@app.route("/health", methods=['GET', 'POST'])
def health():
    return "OK"


book_tag = Tag(name="process_call-log", description="Some Book")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('input.html')


@app.route('/response', methods=['GET', 'POST'])
def web_response():
    question = request.form.get('question')
    urls = []
    for key in request.form.keys():
        if key.startswith('url'):
            urls.append(request.form.get(key))

    print(question, urls)
    # Process the files and the question here
    # And generate your response
    facts = get_facts(len(urls), question, urls, False)
    print("facts",facts)
    #print(response)
    
    return render_template('response.html', question=question, responses=facts)


@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    query = request.json
    try:
        query = SubmitQuestionAndUrls.model_validate(query)

    # Catch pydantic's validation errors:
    except ValidationError as exc:
        print(f"ERROR: Invalid schema: {exc}")
        return exc, 400
    
    result = {}
    result["question"] = query.question
    result["facts"] = []
    result["status"] = "processing"

    with open(app.config["RESULT_PATH"], "w") as file:
        json.dump(result, file, indent=4)
    
    file.close()

    background_thread = threading.Thread(target=get_facts, args=(len(query.documents), query.question, query.documents, True))
    background_thread.start()
    background_thread.join()

    return result, 200


@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    with open(app.config["RESULT_PATH"], "r") as file:
        result = json.load(file)
    
    file.close()

    try:
        GetQuestionAndFactsResponse.model_validate(result)

    # Catch pydantic's validation errors:
    except ValidationError as exc:
        print(f"ERROR: Invalid schema: {exc}")
        return exc, 500

    return result, 200
