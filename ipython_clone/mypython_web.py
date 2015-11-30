#!/usr/bin/env python
# encoding: utf-8
"""
Web-interface using Flask and Jinja-templates to create a graphic 
user interface implementing feedline.py.
"""
from flask import Flask
from flask import request
from flask import render_template
from feedline import *

app = Flask(__name__)

@app.route('/')
def console():
    """ This function Renders the template console.html

    Raises:
        TemplateNotFound: If templates/console.html.
        ImportError: If Flask-module not installed.

    """
    return render_template('console.html')

@app.route('/mypython', methods=['POST'])
def handle_mypython():
    """ This function handles the post requests. It retrieves
    an input-code from the web-interface and calls the feeline-
    function() with it. It then updates the web-interface by 
    retrieving all data (history) from feedline and returns a
    updated page.

    Returns:
        updated_page: The updated and rendered webpage.
    Raises:
        TemplateNotFound: If templates/console.html.
        ImportError: If feedline.py is not in directory.

    """

    # retrieves text from input (web interface)
    code = request.form["code"] 
    feedline(code) 
    # retrieves data stored in feedline (history)
    input_list = get_input() 
    output_list = get_output()
    # updates and renders the data in the web insterface 
    updated_page = render_template("console.html", outp=output_list, inp=input_list)
    return updated_page

if __name__=="__main__":
    app.run(debug=True)
