from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from googletrans import Translator

translator = Translator()

LANG_MAP = {
    "English": "en",
    "Turkish": "tr",
    "Spanish": "es",
    "German": "de",
    "French": "fr",
    "Arabic": "ar"
}

BASE_TEXTS = {
    "title": "Welcome",
    "description": "This app adapts to different languages and cultures.",
    "button": "Click Me"
}

def translate(text, lang):
    if lang == "en":
        return text
    try:
        return translator.translate(text, dest=lang).text
    except:
        return text

class MainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.selected_lang = "en"

        self.spinner = Spinner(
            text="English",
            values=list(LANG_MAP.keys())
        )
        self.spinner.bind(text=self.change_language)

        self.title_label = Label(text=BASE_TEXTS["title"], font_size=32)
        self.desc_label = Label(text=BASE_TEXTS["description"], font_size=18)

        self.button = Button(text=BASE_TEXTS["button"], size_hint=(1, 0.3))
        self.button.bind(on_press=self.on_button)

        self.add_widget(self.spinner)
        self.add_widget(self.title_label)
        self.add_widget(self.desc_label)
        self.add_widget(self.button)

    def change_language(self, spinner, text):
        lang = LANG_MAP[text]
        self.selected_lang = lang

        self.title_label.text = translate(BASE_TEXTS["title"], lang)
        self.desc_label.text = translate(BASE_TEXTS["description"], lang)
        self.button.text = translate(BASE_TEXTS["button"], lang)

        if lang in ["ar"]:
            self.layout_direction(True)
        else:
            self.layout_direction(False)

    def layout_direction(self, rtl):
        if rtl:
            self.title_label.halign = "right"
            self.desc_label.halign = "right"
        else:
            self.title_label.halign = "left"
            self.desc_label.halign = "left"

    def on_button(self, instance):
        instance.text = translate("Clicked!", self.selected_lang)

class MultilingualApp(App):
    def build(self):
        return MainUI()

if __name__ == "__main__":
    MultilingualApp().run()