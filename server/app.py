from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

# Game processes store
processes = {
    "car": None,
    "football": None
}

# Configure static files from React build
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join('../client/build', path)):
        return send_from_directory('../client/build', path)
    else:
        return send_from_directory('../client/build', 'index.html')

@app.route('/start/<game>', methods=['POST'])
def start_game(game):
    # Kill any existing game process
    stop_running_game()
    
    # Start new game
    game_script = f"{game}game.py" if game == "car" else f"{game}.py"
    script_path = os.path.join(os.path.dirname(__file__), game_script)
    
    if os.path.exists(script_path):
        try:
            processes[game] = subprocess.Popen(['python', script_path])
            return jsonify({"message": f"{game} game started"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Game not found"}), 404

def stop_running_game():
    for game, proc in processes.items():
        if proc and proc.poll() is None:
            proc.terminate()
            processes[game] = None

if __name__ == '__main__':
    app.run(port=5000, debug=True)