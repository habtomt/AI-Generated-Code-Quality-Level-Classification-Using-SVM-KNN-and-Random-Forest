"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_004.txt
Run      : 3
"""

# Import necessary libraries
import random
import time

# Define a Story class to store and manage the story
class Story:
    def __init__(self, title, choices):
        self.title = title
        self.choices = choices
        self.current_choice = 0
        self.story_text = []

    def add_paragraph(self, text):
        self.story_text.append(text)

    def add_choice(self, text, next_choice):
        self.choices.append((text, next_choice))

    def start_story(self):
        print(self.title)
        self.print_story()

        while True:
            user_input = input("What do you want to do? (type 'next' to continue) ")
            if user_input.lower() == 'next':
                self.print_story()
            else:
                try:
                    self.current_choice = int(user_input) - 1
                    if self.current_choice < 0 or self.current_choice >= len(self.choices):
                        print("Invalid choice. Please try again.")
                    else:
                        self.print_story()
                except ValueError:
                    print("Invalid input. Please try again.")

    def print_story(self):
        print("\n" + self.story_text[self.current_choice])
        print("\nChoices:")
        for i, (text, _) in enumerate(self.choices):
            if i == self.current_choice:
                print(f"  {i+1}. {text} (you've chosen this option)")
            else:
                print(f"  {i+1}. {text}")

# Create a new story
story = Story("The Mysterious Island", [])

# Add paragraphs to the story
story.add_paragraph("You wake up on a mysterious island. You have no memory of how you got here.")
story.add_paragraph("The island is surrounded by a dense forest, and you see a few paths leading out of it.")

# Add choices to the story
story.add_choice("Follow the path to the left", 1)
story.add_choice("Follow the path to the right", 2)
story.add_choice("Stay here and explore the island", 3)

# Add more paragraphs and choices to the story
story.add_paragraph("You follow the path to the left. It leads you to a clearing with a small cottage.")
story.add_paragraph("The cottage looks abandoned, but you see smoke coming from the chimney.")

story.add_choice("Enter the cottage", 4)
story.add_choice("Explore the surrounding area", 5)
story.add_choice("Go back to the main path", 6)

# Start the story
story.start_story()