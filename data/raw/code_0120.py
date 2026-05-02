from flask import Flask, request, render_template_string
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

BASE_CONTENT = {
    "title": "Welcome to Our Website",
    "body": "This is a multilingual website. You can change the language from the selector."
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <form method="GET">
        <label>Select Language:</label>
        <select name="lang" onchange="this.form.submit()">
            <option value="en" {% if lang == 'en' %}selected{% endif %}>English</option>
            <option value="tr" {% if lang == 'tr' %}selected{% endif %}>Turkish</option>
            <option value="es" {% if lang == 'es' %}selected{% endif %}>Spanish</option>
            <option value="de" {% if lang == 'de' %}selected{% endif %}>German</option>
            <option value="fr" {% if lang == 'fr' %}selected{% endif %}>French</option>
        </select>
    </form>

    <h1>{{ title }}</h1>
    <p>{{ body }}</p>
</body>
</html>
"""

def translate_text(text, lang):
    if lang == "en":
        return text
    return translator.translate(text, dest=lang).text

@app.route("/")
def index():
    lang = request.args.get("lang", "en")

    title = translate_text(BASE_CONTENT["title"], lang)
    body = translate_text(BASE_CONTENT["body"], lang)

    return render_template_string(HTML_TEMPLATE, title=title, body=body, lang=lang)

if __name__ == "__main__":
    app.run(debug=True)