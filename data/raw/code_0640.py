"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_004.txt
Run      : 2
"""

import tkinter as tk
from tkinter import messagebox
import random

# Initialize Tkinter window
class StorytellerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Storyteller")

        # Create text area for story display
        self.story_text = tk.Text(self.root, height=20, width=80)
        self.story_text.pack(padx=10, pady=10)

        # Create button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(padx=10, pady=10)

        # Create buttons for navigation
        self.prev_button = tk.Button(self.button_frame, text="Previous", command=self.prev_chapter)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_chapter)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Initialize story variables
        self.chapter = 1
        self.story = {
            "chapter1": ["You are standing at the entrance of a dark forest.", "The trees seem to be whispering to each other."],
            "chapter2": ["As you venture deeper into the forest, you hear the sound of rushing water.", "A clearing appears, and you see a beautiful waterfall."],
            "chapter3": ["The waterfall leads you to a hidden cave.", "Inside the cave, you find a mysterious artifact."],
        }

        # Display first chapter
        self.display_chapter()

    # Function to display current chapter
    def display_chapter(self):
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, "\n".join(self.story[f"chapter{self.chapter}"]))

    # Function to navigate to previous chapter
    def prev_chapter(self):
        if self.chapter > 1:
            self.chapter -= 1
            self.display_chapter()

    # Function to navigate to next chapter
    def next_chapter(self):
        if self.chapter < len(self.story):
            self.chapter += 1
            self.display_chapter()

# Create Tkinter root window
root = tk.Tk()

# Create StorytellerApp instance
app = StorytellerApp(root)

# Start Tkinter event loop
root.mainloop()