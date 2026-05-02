import http.client
import urllib.parse
import json

def translate_text(text, target_lang='es', source_lang='en'):
    """
    Translates text using the MyMemory API (Free tier, no key required for basic use).
    """
    base_url = "api.mymemory.translated.net"
    pair = f"{source_lang}|{target_lang}"
    params = urllib.parse.urlencode({'q': text, 'langpair': pair})
    
    conn = http.client.HTTPSConnection(base_url)
    try:
        conn.request("GET", f"/get?{params}")
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        return data.get("responseData", {}).get("translatedText", "Translation error.")
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

def main():
    # Example sentences for translation
    translations_to_perform = [
        {"text": "Hello, how are you today?", "to": "es"},    # Spanish
        {"text": "Python is a great language.", "to": "fr"}, # French
        {"text": "Good morning, friend.", "to": "de"}        # German
    ]

    print(f"{'Source (EN)':<30} | {'Target Language':<10} | {'Translated Text'}")
    print("-" * 80)

    for item in translations_to_perform:
        result = translate_text(item["text"], target_lang=item["to"])
        print(f"{item['text']:<30} | {item['to']:<15} | {result}")

if __name__ == "__main__":
    main()