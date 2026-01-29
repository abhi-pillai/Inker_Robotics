from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-3-flash-preview')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Create prompt for Gemini
        prompt = f"""Analyze the emotion in the following message and classify it as one of: happy, sad, angry, or neutral.
        
Message: "{message}"

Respond in this exact format:
Emotion: [happy/sad/angry/neutral]
Explanation: [Brief 1-2 sentence explanation of why this emotion was detected]"""
        
        # Generate response
        response = model.generate_content(prompt)
        result_text = response.text
        
        # Parse the response
        lines = result_text.strip().split('\n')
        emotion = ""
        explanation = ""
        
        for line in lines:
            if line.startswith('Emotion:'):
                emotion = line.replace('Emotion:', '').strip().lower()
            elif line.startswith('Explanation:'):
                explanation = line.replace('Explanation:', '').strip()
        
        return jsonify({
            'emotion': emotion,
            'explanation': explanation
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)