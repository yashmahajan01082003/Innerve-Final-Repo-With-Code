from flask import Blueprint, jsonify, request
import datetime
import pyjokes
import requests
import wolframalpha
from ..config import config

bp = Blueprint('jarvis', __name__, url_prefix='/api/jarvis')

# Initialize services
app_id = config.wolframalpha_id
client = wolframalpha.Client(app_id)


@bp.route('/process', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()
    response = {"response": "", "action": None}

    if not command:
        return jsonify({"error": "No command provided"}), 400

    # Time and Date
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response["response"] = f"Sir the time is {current_time}"

    elif 'date' in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        response["response"] = current_date

    # Web Operations
    elif 'open' in command and 'http' not in command:
        domain = command.split(' ')[-1]
        response["response"] = f"Opening {domain}"
        response["action"] = {"type": "open_website", "target": domain}

    elif 'search google for' in command:
        query = command.replace('search google for', '').strip()
        response["response"] = f"Searching Google for {query}"
        response["action"] = {"type": "google_search", "query": query}

    # Knowledge
    elif 'tell me about' in command:
        topic = command.split(' ')[-1]
        response["response"] = f"Here's what I found about {topic}"
        response["action"] = {"type": "wikipedia", "query": topic}

    # Calculations
    elif 'calculate' in command or 'what is' in command:
        try:
            result = client.query(command)
            answer = next(result.results).text
            response["response"] = answer
        except:
            response["response"] = "Sorry, I couldn't calculate that"

    # Jokes
    elif 'joke' in command:
        response["response"] = pyjokes.get_joke()

    # System Info
    elif 'system' in command:
        # Implement system info gathering
        response["response"] = "Here's your system information"

    # Default response
    else:
        response["response"] = "I didn't understand that command"

    return jsonify(response)
