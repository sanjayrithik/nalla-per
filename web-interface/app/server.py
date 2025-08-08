# web-interface/app/server.py
import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from threading import Lock

app = Flask(__name__, static_folder='static', template_folder='templates')

# Read CLI server host from env (use service name when using docker-compose)
CLI_SERVER_HOST = os.environ.get('CLI_SERVER_HOST', 'cli-server:5000')
CLI_RUN_URL = f'http://{CLI_SERVER_HOST}/run'

# In-memory keys store (simple)
key_lock = Lock()
KEYS = []  # list of dicts: { "key": "...", "status": "working"|"invalid" }

# Helper: test a single Gemini-like key with a minimal "health check" request
# NOTE: adapt the URL/payload to your actual Gemini endpoint if different.
def test_key_health(key):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "prompt": {"messages":[{"role":"user", "content":"Say ok"}]},
        "temperature": 0
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=6)
        # treat 200 as ok, 401/403 as invalid
        if r.status_code == 200:
            return True, r.text
        else:
            return False, f"status:{r.status_code} body:{r.text[:200]}"
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/api/initKeys', methods=['POST'])
def init_keys():
    data = request.json or {}
    keys = data.get('keys', [])
    if not isinstance(keys, list):
        return jsonify({"error": "keys must be a list"}), 400

    results = []
    new_working = []
    # Test each key (quick)
    for k in keys:
        ok, info = test_key_health(k)
        status = "working" if ok else "invalid"
        results.append({"key": k, "status": status, "info": info if not ok else ""})
        if ok:
            new_working.append(k)

    # Save working keys in-memory, order preserved (first = preferred)
    with key_lock:
        KEYS.clear()
        for wk in new_working:
            KEYS.append({"key": wk, "status": "working"})

    return jsonify({"keys": results, "working_count": len(new_working)})

# Internal: pick a working key (rotate if needed)
def pick_working_key():
    with key_lock:
        if not KEYS:
            return None
        # simple rotation: pop first and append it back
        k = KEYS.pop(0)
        KEYS.append(k)
        return k["key"]

@app.route('/api/processCommand', methods=['POST'])
def process_command():
    """
    Accepts: { "task": "scan example.com" }
    Flow:
      - Use a working key to send 'task -> cli command' request to Gemini (pseudo)
      - Send generated command to CLI server at CLI_RUN_URL
      - Get raw output, optionally summarize via Gemini
      - Return both raw and summary
    """
    data = request.json or {}
    task = data.get('task', '').strip()
    if not task:
        return jsonify({"error": "task is required"}), 400

    key = pick_working_key()
    if not key:
        return jsonify({"error": "no working API key available"}), 503

    # 1) Convert user task -> CLI command (here we assume the model returns a plain command string)
    # NOTE: Replace URL/payload with your real Gemini conversion flow.
    model_url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    prompt_payload = {
        "prompt": {
            "messages": [
                {"role":"system", "content": "You convert user tasks to a single CLI command only."},
                {"role":"user", "content": f"Task: {task}\nRespond with only the command to run (no explanation)."}
            ]
        },
        "temperature": 0
    }
    try:
        r = requests.post(model_url, headers=headers, json=prompt_payload, timeout=12)
        if r.status_code != 200:
            return jsonify({"error": "model error", "status": r.status_code, "body": r.text}), 502
        # Extract text - adapt to your model's response structure
        model_resp_text = r.text
        # crude attempt: assume the full response body contains the command; you may need to parse JSON
        # For safety, try to parse JSON and extract likely field(s)
        try:
            jr = r.json()
            # Attempt common paths (update if your Gemini wrapper differs)
            # These are defensive; change to the real field names you receive.
            # Example: jr['candidates'][0]['content'][0]['text'] etc.
            command = None
            if isinstance(jr, dict):
                # search for first string in nested structure
                import collections, json
                def find_first_string(o):
                    if isinstance(o, str):
                        return o
                    if isinstance(o, dict):
                        for v in o.values():
                            s = find_first_string(v)
                            if s:
                                return s
                    if isinstance(o, list):
                        for v in o:
                            s = find_first_string(v)
                            if s:
                                return s
                    return None
                command = find_first_string(jr)
            if not command:
                command = model_resp_text.strip()
        except Exception:
            command = model_resp_text.strip()
    except Exception as e:
        return jsonify({"error": "model request failed", "detail": str(e)}), 502

    # 2) Send command to CLI server
    try:
        cli_resp = requests.post(CLI_RUN_URL, json={"command": command}, timeout=30)
    except Exception as e:
        return jsonify({"error": "failed to reach CLI server", "detail": str(e), "cli_url": CLI_RUN_URL}), 502

    if cli_resp.status_code not in (200, 201):
        # forward CLI server error
        try:
            return jsonify({"error": "cli_server_error", "body": cli_resp.json()}), cli_resp.status_code
        except Exception:
            return jsonify({"error": "cli_server_error", "body": cli_resp.text}), cli_resp.status_code

    raw_output = cli_resp.json().get('output', cli_resp.text)

    # 3) Ask model to summarize raw_output (optional) - we'll skip heavy summarization if no key
    try:
        summarize_payload = {
            "prompt": {
                "messages": [
                    {"role":"system", "content": "You must summarize terminal output in short bullet points."},
                    {"role":"user", "content": f"Summarize the following output:\n\n{raw_output}"}
                ]
            },
            "temperature": 0.2
        }
        # Reuse same key for summarization
        rsum = requests.post(model_url, headers=headers, json=summarize_payload, timeout=12)
        summary = None
        if rsum.status_code == 200:
            try:
                summary = rsum.json()
                # fallback to text
                summary = str(summary)[:2000]
            except Exception:
                summary = rsum.text
        else:
            summary = f"summary_failed status:{rsum.status_code}"
    except Exception as e:
        summary = f"summary_exception: {e}"

    return jsonify({"command": command, "raw": raw_output, "summary": summary})

@app.route('/api/directCommand', methods=['POST'])
def direct_command():
    """
    Bypass AI: directly forward { "command": "<shell command>" } to the CLI server.
    Useful for testing connectivity or for when keys fail.
    """
    data = request.json or {}
    cmd = data.get('command', '').strip()
    if not cmd:
        return jsonify({"error": "command required"}), 400

    try:
        r = requests.post(CLI_RUN_URL, json={"command": cmd}, timeout=30)
    except Exception as e:
        return jsonify({"error": "failed to reach CLI server", "detail": str(e), "cli_url": CLI_RUN_URL}), 502

    if r.status_code not in (200, 201):
        try:
            return jsonify({"error": "cli_server_error", "body": r.json()}), r.status_code
        except Exception:
            return jsonify({"error": "cli_server_error", "body": r.text}), r.status_code

    return jsonify(r.json())

if __name__ == '__main__':
    # Allow external Docker container to specify host/port via env
    host = os.environ.get('WEB_HOST', '0.0.0.0')
    port = int(os.environ.get('WEB_PORT', '3000'))
    app.run(host=host, port=port, debug=True)
