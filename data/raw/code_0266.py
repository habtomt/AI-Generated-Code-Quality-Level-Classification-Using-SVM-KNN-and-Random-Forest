from flask import Flask, render_template_string, request, session, redirect, url_for
from googletrans import Translator

app = Flask(__name__)
app.secret_key = "translation_secret_key"
translator = Translator()

# Mock website content
site_content = {
    "title": "Welcome to Our Platform",
    "header": "Global Services for Everyone",
    "description": "We provide innovative solutions to help your business grow worldwide.",
    "cta": "Get Started Now",
    "footer": "© 2026 TechCorp International. All rights reserved."
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ content.title }}</title>
    <style>
        body { font-family: sans-serif; padding: 50px; text-align: center; }
        .lang-picker { margin-bottom: 30px; }
        .container { border: 1px solid #ccc; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="lang-picker">
        <form action="/set_language" method="post">
            <label>Select Language:</label>
            <select name="language" onchange="this.form.submit()">
                <option value="en" {% if session.get('lang') == 'en' %}selected{% endif %}>English</option>
                <option value="es" {% if session.get('lang') == 'es' %}selected{% endif %}>Spanish</option>
                <option value="fr" {% if session.get('lang') == 'fr' %}selected{% endif %}>French</option>
                <option value="de" {% if session.get('lang') == 'de' %}selected{% endif %}>German</option>
                <option value="zh-cn" {% if session.get('lang') == 'zh-cn' %}selected{% endif %}>Chinese</option>
            </select>
        </form>
    </div>

    <div class="container">
        <h1>{{ content.title }}</h1>
        <h3>{{ content.header }}</h3>
        <p>{{ content.description }}</p>
        <button>{{ content.cta }}</button>
    </div>
    <footer>
        <p>{{ content.footer }}</p>
    </footer>
</body>
</html>
"""

@app.route("/")
def index():
    lang = session.get('lang', 'en')
    
    if lang == 'en':
        return render_template_string(HTML_TEMPLATE, content=site_content)
    
    # Translate all static content to the selected language
    translated_content = {}
    try:
        for key, text in site_content.items():
            translation = translator.translate(text, dest=lang)
            translated_content[key] = translation.text
    except Exception:
        # Fallback to English if API fails
        translated_content = site_content

    return render_template_string(HTML_TEMPLATE, content=translated_content)

@app.route("/set_language", methods=["POST"])
def set_language():
    selected_lang = request.form.get("language")
    session['lang'] = selected_lang
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Requirements: pip install Flask googletrans==4.0.0-rc1
    app.run(debug=True)