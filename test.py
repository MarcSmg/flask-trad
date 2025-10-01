import asyncio
import pyttsx3
from googletrans import Translator
async def t():
    trans = Translator()
    tr = await trans.translate('bonjour', src='fr')
    print(tr)

# asyncio.run(t())

text_speech = pyttsx3.init()
text_speech.say("Hello, how're you doing ?")
text_speech.runAndWait()

