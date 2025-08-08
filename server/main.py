from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_command():
    """
    Accepts: { "command": "<shell command>" }
    Runs the command inside the container and returns the output.
    """
    data = request.json or {}
    cmd = data.get('command', '').strip()

    if not cmd:
        return jsonify({"error": "command required"}), 400

    try:
        # Execute the command in the container's shell
        output = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            timeout=30
        )
        return jsonify({"output": output.decode(errors='ignore')})
    except subprocess.CalledProcessError as e:
        # Command returned non-zero exit code
        return jsonify({
            "output": e.output.decode(errors='ignore'),
            "error": str(e)
        }), 400
    except subprocess.TimeoutExpired:
        return jsonify({"output": "Command timed out"}), 408

if __name__ == '__main__':
    # Listen on all interfaces so web container can reach it
    app.run(host='0.0.0.0', port=5000)
