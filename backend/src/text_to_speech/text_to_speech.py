from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from src.text_to_speech.text_to_speech import WATSONConfig

# Authenticate
URL = WATSONConfig.URL
API_KEY = WATSONConfig.API_KEY

# Create IAM Authenticator object
authenticator = IAMAuthenticator(API_KEY)

# Create Text to Speech object
text_to_speech = TextToSpeechV1(authenticator=authenticator)
text_to_speech.set_service_url(URL)

# Convert at string


def convert_text_to_sound_file(message, filename, voice="en-US_AllisonV3Voice"):
    """
    Convert a string to a mp3 file.
    """
    with open(filename, "wb") as audio_file:
        result = text_to_speech.synthesize(
            message, accept="audio/mp3", voice=voice
        ).get_result()
        audio_file.write(result.content)


# Using new language models
