import json
import time

class InteractiveVideoPlayer:
    def __init__(self):
        self.overlays = []
        self.is_playing = False
        self.current_time = 0

    def add_interaction(self, timestamp, element_type, data):
        """
        Adds interactive elements like quizzes, annotations, or links.
        element_type: 'quiz', 'annotation', 'link'
        """
        interaction = {
            "timestamp": timestamp,
            "type": element_type,
            "data": data,
            "triggered": False
        }
        self.overlays.append(interaction)
        self.overlays.sort(key=lambda x: x['timestamp'])

    def trigger_quiz(self, data):
        print(f"\n--- QUIZ PAUSE at {self.current_time}s ---")
        print(f"Question: {data['question']}")
        for i, opt in enumerate(data['options']):
            print(f"{i+1}. {opt}")
        
        # Simulating user input
        choice = input("Your answer (number): ")
        if data['options'][int(choice)-1] == data['answer']:
            print("Correct! Resuming video...")
        else:
            print(f"Wrong! The correct answer was: {data['answer']}. Resuming...")

    def trigger_annotation(self, data):
        print(f"\n[ANNOTATION at {self.current_time}s]: {data['text']}")

    def trigger_link(self, data):
        print(f"\n[CLICKABLE LINK at {self.current_time}s]: {data['label']} -> {data['url']}")

    def play(self, duration):
        print(f"Starting interactive video playback ({duration}s)...")
        self.is_playing = True
        
        for second in range(duration + 1):
            self.current_time = second
            
            # Check for interactions scheduled at this second
            for interaction in self.overlays:
                if interaction['timestamp'] == self.current_time and not interaction['triggered']:
                    if interaction['type'] == 'quiz':
                        self.trigger_quiz(interaction['data'])
                    elif interaction['type'] == 'annotation':
                        self.trigger_annotation(interaction['data'])
                    elif interaction['type'] == 'link':
                        self.trigger_link(interaction['data'])
                    
                    interaction['triggered'] = True
            
            time.sleep(0.1) # Accelerated simulation
            if second % 5 == 0:
                print(f"Video playing... {second}s")

        print("End of video.")

if __name__ == "__main__":
    player = InteractiveVideoPlayer()

    # Define Interactive Elements
    player.add_interaction(
        timestamp=3, 
        element_type="annotation", 
        data={"text": "Note the specific coding syntax used here."}
    )

    player.add_interaction(
        timestamp=7, 
        element_type="link", 
        data={"label": "View Documentation", "url": "https://docs.python.org"}
    )

    player.add_interaction(
        timestamp=12, 
        element_type="quiz", 
        data={
            "question": "What is the result of 2 + 2?",
            "options": ["3", "4", "5"],
            "answer": "4"
        }
    )

    # Run the simulation
    player.play(duration=15)