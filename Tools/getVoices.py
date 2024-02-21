from elevenlabs import voices, generate
from elevenlabs.client import ElevenLabs
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #It just works
import creds

def grab_voice_ids():
    # Get the API key from the creds.py file
    client = ElevenLabs(api_key=str(creds.ELEVENLABS_API_KEY))

    # Gather the voices
    response = client.voices.get_all()
    
    # Print the voices to console
    for voice in response.voices:
        voice_id = voice.voice_id
        name = voice.name
        category = voice.category
        print(f'Voice ID: {voice_id} - Name: {name} - Category: {category}')

    # Write the voices to a file, for easy reference
    with open('voice_ids.txt', 'w') as file:
        for voice in response.voices:
            voice_id = voice.voice_id
            name = voice.name
            category = voice.category
            file.write(f'Voice ID: {voice_id} - Name: {name} - Category: {category}\n')
            
# Call the function to grab the voice IDs and write them to a file and print them to console.
grab_voice_ids()