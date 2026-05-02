"""
Auto-generated Python code
Scenario : Translation
Prompt   : response_001.txt
Run      : 3
"""

# Import required libraries
import flask
from flask import render_template, request, flash
from googletrans import Translator, LANGUAGES

# Initialize the Flask app
app = flask.Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Define supported languages
supported_languages = list(LANGUAGES.values())

# Define the translation function
def translate_text(text, lang):
    try:
        translator = Translator()
        result = translator.translate(text, dest=lang)
        return result.text
    except Exception as e:
        flash(f"Error translating text: {str(e)}")
        return text

# Define the route for selecting language
@app.route('/set_language', methods=['POST'])
def set_language():
    lang = request.form['lang']
    # Get the translation for each page
    for key, value in flask.g.items():
        if isinstance(value, dict):
            for k, v in value.items():
                flask.g[key][k] = translate_text(v, lang)
    # Redirect to the root page with the new language
    return flask.redirect(flask.url_for('index'))

# Define the route for the index page
@app.route('/')
def index():
    # Get the selected language from the session
    lang = flask.session.get('lang')
    if lang is None:
        lang = 'en'  # Default language
    # Get the translated content
    content = {
        'title': translate_text('Welcome to our website!', lang),
        'heading': translate_text('Select your language', lang),
        'options': [{'lang': k, 'text': translate_text('Select', k)} for k in supported_languages],
    }
    # Store the selected language in the session
    flask.session['lang'] = lang
    # Render the template with the translated content
    return render_template('index.html', content=content)

# Define the route for the translation page
@app.route('/translate')
def translate():
    # Get the selected language from the session
    lang = flask.session.get('lang')
    if lang is None:
        lang = 'en'  # Default language
    # Get the translation for each page
    for key, value in flask.g.items():
        if isinstance(value, dict):
            for k, v in value.items():
                flask.g[key][k] = translate_text(v, lang)
    # Redirect to the root page with the new language
    return flask.redirect(flask.url_for('index'))

# Initialize the translation data
flask.g = {
    'title': {'en': 'Welcome to our website!', 'fr': 'Bienvenue sur notre site web!', 'es': 'Bienvenido a nuestro sitio web!'},
    'heading': {'en': 'Select your language', 'fr': 'Choisissez votre langue', 'es': 'Seleccione su idioma'},
}

if __name__ == '__main__':
    app.run(debug=True)