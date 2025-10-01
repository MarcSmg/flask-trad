from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from googletrans import Translator, LANGUAGES
from flasgger import Swagger
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

swagger = Swagger(app)

app.config['SECRET_KEY'] = 'hdsuh&cjsn'#Secret key for the sessions

correct_pin = os.getenv('CORRECT_PIN') #The correct PIN

language_codes = list(LANGUAGES.keys())
language_names = list(LANGUAGES.values())



"""
Pin entry view
Used to enter the web app

"""

@app.route('/', methods=['GET', 'POST'])
def pin_entry():

    if session.get('authenticated'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        user_pin = request.form.get('pin')

        if user_pin == correct_pin :
            session['authenticated'] = True
            return redirect(url_for('index'))
        else: 
            error= "Invalid PIN. Please try again."
            return render_template('pin_entry.html', error=error)
    return render_template('pin_entry.html')

"""Home page view"""

@app.route('/home')
def index():
    if session.get('authenticated'):
        return render_template('index.html', source_languages=zip(language_codes, language_names), target_languages=zip(language_codes, language_names))
    else:
        # If not authenticated, redirect them to the PIN entry page
        return redirect(url_for('pin_entry'))
    
"""Translation view"""

@app.route('/translate', methods=['POST'])
def translate_text():
    """
    Translate text using Form Data submission.
    This endpoint processes text, source, and target language codes submitted via HTML form data.
    ---
    tags:
      - Translation Service
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      # --- Parameters use 'in: formData' because they come from request.form ---
      - name: text
        in: formData
        type: string
        required: true
        description: The text string that needs to be translated.
        example: "The rain in Spain falls mainly on the plain."
      - name: source_language
        in: formData
        type: string
        required: true
        description: The language code of the source text (e.g., 'en', 'auto').
        example: "en"
      - name: target_language
        in: formData
        type: string
        required: true
        description: The language code to translate the text into (e.g., 'es', 'fr').
        example: "fr"
    responses:
      200:
        description: Translation successfully completed (200 OK for successful operation).
        schema:
          type: object
          properties:
            translation:
              type: string
              description: The resulting translated text.
              example: "La pluie en Espagne tombe principalement sur la plaine."
            source_language:
              type: string
            target_language:
              type: string
      400:
        description: Bad Request. Missing required form data fields.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Please provide text, source, and target languages."
    """

    text_to_translate = request.form.get('text')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    # 1. Input Validation
    if not text_to_translate or not source_language or not target_language:
        return jsonify({'error': 'Please provide text, source, and target languages.'}), 400
    
    translator = Translator()

    try:
        # --- ASYNC WRAPPER ---
        async def run_translation():
            """Helper function to await the coroutine."""
            return await translator.translate(
                text_to_translate, 
                src=source_language, 
                dest=target_language
            )

        # 2. Attempt Translation: Execute the async function synchronously
        translation_object = asyncio.run(run_translation())
        # --- END ASYNC WRAPPER ---
        
        # 3. Successful JSON Response
        return jsonify({
            'translation': translation_object.text, 
            'source_language': translation_object.src,
            'target_language': translation_object.dest
        })
        
    except Exception as e:
        # 4. Error Handling: Log and return an error JSON (503 Service Unavailable)
        print(f"Translation failed via googletrans: {e}")
        return jsonify({'error': 'Translation failed. The translation service may be unavailable.'}), 503

"""Logout view"""

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('pin_entry'))

if __name__ == '__main__':
    app.run(debug=True)