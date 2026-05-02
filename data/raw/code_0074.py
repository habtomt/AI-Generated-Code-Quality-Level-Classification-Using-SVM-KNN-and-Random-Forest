import os
import numpy as np
import tensorflow as tf

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

MODEL_PATH = "model.h5"
TFLITE_PATH = "model.tflite"


def create_and_save_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation="relu", input_shape=(4,)),
        tf.keras.layers.Dense(2, activation="softmax")
    ])

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")

    x = np.random.rand(100, 4)
    y = np.random.randint(0, 2, 100)

    model.fit(x, y, epochs=3, verbose=0)
    model.save(MODEL_PATH)


def convert_to_tflite():
    model = tf.keras.models.load_model(MODEL_PATH)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    with open(TFLITE_PATH, "wb") as f:
        f.write(tflite_model)


def load_interpreter():
    interpreter = tf.lite.Interpreter(model_path=TFLITE_PATH)
    interpreter.allocate_tensors()
    return interpreter


def predict(interpreter, input_data):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_data = np.array(input_data, dtype=np.float32).reshape(1, 4)

    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]["index"])
    return output


class MLApp(BoxLayout):
    def __init__(self, interpreter, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.interpreter = interpreter

        self.label = Label(text="Enter 4 values separated by space")
        self.add_widget(self.label)

        self.input_box = TextInput(multiline=False)
        self.add_widget(self.input_box)

        self.button = Button(text="Predict")
        self.button.bind(on_press=self.on_predict)
        self.add_widget(self.button)

        self.result = Label(text="")
        self.add_widget(self.result)

    def on_predict(self, instance):
        try:
            values = list(map(float, self.input_box.text.strip().split()))
            if len(values) != 4:
                self.result.text = "Enter exactly 4 values"
                return

            output = predict(self.interpreter, values)
            self.result.text = f"Prediction: {np.argmax(output)}"

        except Exception as e:
            self.result.text = f"Error: {str(e)}"


class MobileMLApp(App):
    def build(self):
        if not os.path.exists(MODEL_PATH):
            create_and_save_model()

        if not os.path.exists(TFLITE_PATH):
            convert_to_tflite()

        interpreter = load_interpreter()
        return MLApp(interpreter)


if __name__ == "__main__":
    MobileMLApp().run()