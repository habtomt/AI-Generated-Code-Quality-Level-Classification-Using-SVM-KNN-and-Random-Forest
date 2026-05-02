import os
import json

class AppLocalizationManager:
    def __init__(self, base_path="assets/locales"):
        self.base_path = base_path
        self.locales = {
            "en": {
                "greeting": "Hello, User!",
                "currency_symbol": "$",
                "date_format": "MM/DD/YYYY",
                "hero_image": "banner_en.png",
                "layout_direction": "LTR"
            },
            "es": {
                "greeting": "¡Hola, Usuario!",
                "currency_symbol": "€",
                "date_format": "DD/MM/YYYY",
                "hero_image": "banner_es.png",
                "layout_direction": "LTR"
            },
            "ar": {
                "greeting": "مرحباً مستخدم",
                "currency_symbol": "﷼",
                "date_format": "YYYY/MM/DD",
                "hero_image": "banner_ar.png",
                "layout_direction": "RTL"
            }
        }
        self.current_lang = "en"

    def set_language(self, lang_code):
        if lang_code in self.locales:
            self.current_lang = lang_code
            print(f">> App language switched to: {lang_code}")
        else:
            print(">> Language code not supported. Defaulting to English.")

    def get_string(self, key):
        return self.locales[self.current_lang].get(key, f"[{key}_missing]")

    def get_graphic(self, key):
        asset_name = self.locales[self.current_lang].get(key)
        return f"/path/to/assets/{self.current_lang}/{asset_name}"

    def render_ui(self):
        lang_data = self.locales[self.current_lang]
        
        print("\n--- UI RENDER START ---")
        print(f"Layout Direction: {lang_data['layout_direction']}")
        print(f"Header: {self.get_string('greeting')}")
        print(f"Loading Image: {self.get_graphic('hero_image')}")
        print(f"Price Display Example: {lang_data['currency_symbol']}100.00")
        print(f"System Date: {lang_data['date_format']}")
        print("--- UI RENDER END ---\n")

    def export_locales(self):
        """Simulates exporting locale files for a mobile project structure."""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        
        for code, data in self.locales.items():
            file_path = os.path.join(self.base_path, f"{code}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Locales exported to {self.base_path}")

if __name__ == "__main__":
    app = AppLocalizationManager()

    # 1. Default (English)
    app.render_ui()

    # 2. Switch to Spanish (Cultural Adaptation: Date & Currency)
    app.set_language("es")
    app.render_ui()

    # 3. Switch to Arabic (UI Adaptation: Right-to-Left Layout)
    app.set_language("ar")
    app.render_ui()

    # 4. Generate project files
    app.export_locales()