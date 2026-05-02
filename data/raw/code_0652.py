"""
Auto-generated Python code
Scenario : Translation
Prompt   : response_001.txt
Run      : 2
"""

# Import flask for web application framework
from flask import Flask, render_template, request, session
import googletrans as gt
from googletrans.models import Translation

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "secret_key"  # Add your secret key here

# Translate function using Google Translate API
def translate_text(text, lang):
    try:
        translator = gt.Translator()
        translation = translator.translate(text, dest=lang)
        return translation.text
    except Exception as e:
        return str(e)

# Route for the home page
@app.route('/')
def index():
    if 'lang' in session:
        lang = session['lang']
    else:
        lang = 'en'  # Default language
    return render_template('index.html', lang=lang)

# Route for language selection
@app.route('/lang', methods=['POST'])
def select_language():
    try:
        lang = request.form['lang']
        session['lang'] = lang
        return render_template('index.html', lang=lang)
    except Exception as e:
        return str(e)

# Route for translating content
@app.route('/translate', methods=['POST'])
def translate_content():
    try:
        content = request.form['content']
        lang = session['lang']
        translated_content = translate_text(content, lang)
        return render_template('translated_content.html', content=translated_content, lang=lang)
    except Exception as e:
        return str(e)

# Route for translating page content
@app.route('/translate_page', methods=['POST'])
def translate_page():
    try:
        content = request.form['content']
        lang = session['lang']
        translated_content = translate_text(content, lang)
        return render_template('translated_page.html', content=translated_content, lang=lang)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)