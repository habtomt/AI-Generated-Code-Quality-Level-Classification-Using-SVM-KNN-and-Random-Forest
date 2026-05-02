"""
Auto-generated Python code
Scenario : Text-to-Speech
Prompt   : response_003.txt
Run      : 1
"""

# Import required libraries
import googlemaps
import pyttsx3
import time
import threading

# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to retrieve directions from Google Maps
def get_directions(origin, destination):
    try:
        directions_result = gmaps.directions(origin, destination, mode="driving")
        if directions_result:
            steps = directions_result[0]['legs'][0]['steps']
            return steps
        else:
            return []
    except Exception as e:
        print(f"Error retrieving directions: {str(e)}")
        return []

# Function to offer spoken directions
def offer_spoken_directions(origin, destination):
    steps = get_directions(origin, destination)
    
    if not steps:
        engine.say("I could not retrieve the directions.")
        engine.runAndWait()
        return

    for step in steps:
        # Extract the navigation instruction in text format
        instruction = step['html_instructions']

        # Strip HTML tags if needed, here we use a simple replacement for this demo
        cleaned_instruction = instruction.replace('<b>', '').replace('</b>', '').replace('<div style="font-size:0.9em">', ' ').replace('</div>', '')
        
        # Speak the direction out loud
        engine.say(cleaned_instruction)
        engine.runAndWait()
        time.sleep(2)  # Pause for 2 seconds to allow the voice to finish speaking

    engine.say("You have arrived at your destination.")
    engine.runAndWait()

# Function to update the user with the current location
def update_location(origin, destination):
    while True:
        try:
            # Use the Google Maps API to get the current location
            current_location = gmaps.geocode(origin)
            if current_location:
                engine.say(f"Current location: {current_location[0]['formatted_address']}")
                engine.runAndWait()
            time.sleep(5)  # Update every 5 seconds
        except Exception as e:
            print(f"Error updating location: {str(e)}")
            time.sleep(5)  # Wait for 5 seconds before trying again

# Example usage
origin = "Times Square, New York, NY"
destination = "Central Park, New York, NY"

# Create a new thread to update the user's location
location_thread = threading.Thread(target=update_location, args=(origin, destination))
location_thread.daemon = True  # Set as daemon thread so it exits when the main program exits
location_thread.start()

# Offer spoken directions
offer_spoken_directions(origin, destination)

# Keep the program running until the user stops it
while True:
    pass