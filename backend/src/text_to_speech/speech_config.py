import os
from dotenv import load_dotenv

load_dotenv()

class WATSONConfig:
    VOICES = [
        "en-US_AllisonV3Voice",
        "en-AU_HeidiExpressive",
        "en-AU_JackExpressive",
        "en-US_AllisonExpressive",
        "en-US_EmmaExpressive",
        "en-US_LisaExpressive",
        "en-US_MichaelExpressive",
        "en-GB_CharlotteV3Voice",
        "en-GB_JamesV3Voice",
        "en-GB_KateV3Voice",
        "en-US_AllisonV3Voice",
        "en-US_EmilyV3Voice",
        "en-US_HenryV3Voice",
        "en-US_KevinV3Voice",
        "en-US_LisaV3Voice",
        "en-US_MichaelV3Voice",
        "en-US_OliviaV3Voice",
        

    ]
    API_KEY = os.getenv('WATSON_API_KEY')
    URL = os.getenv('WATSON_URL')
