from flask import Flask, render_template, request, jsonify
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Claude client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Cheaper model to save credits
            max_tokens=1000,
            messages=[{"role": "user", "content": user_message}]
        )
        
        return jsonify({
            'success': True,
            'response': response.content[0].text
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
