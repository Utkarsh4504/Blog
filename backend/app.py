import subprocess
from urllib.parse import urlparse
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Initialize the Flask app, pointing to the frontend directory for static files
app = Flask(__name__, static_folder='../frontend', static_url_path='/')

# Enable CORS for all routes
CORS(app)

def get_mock_ai_response(system_prompt, user_content):
    """
    Returns a mock AI response for demonstration purposes.
    """
    if "coding assistant" in system_prompt:
        return f"[MOCK AI RESPONSE] A real AI would provide a helpful answer to your query: '{user_content[:50]}...'"
    elif "cybersecurity expert" in system_prompt:
        return "[MOCK AI SUMMARY] A real AI would analyze the Nmap scan results and provide a detailed, easy-to-understand summary here."
    else:
        return "[MOCK AI RESPONSE] A real AI would respond here."

# API route for AI queries
@app.route('/query', methods=['POST'])
def handle_query():
    """Handles coding-related queries using a mock AI response."""
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is required."}), 400
    system_prompt = "You are a helpful and knowledgeable coding assistant."
    mock_response = get_mock_ai_response(system_prompt, query)
    return jsonify({"response": mock_response})

# API route for vulnerability scans
@app.route('/scan', methods=['POST'])
def handle_scan():
    """Handles vulnerability scan requests and provides a mock AI summary."""
    data = request.json
    url = data.get('url')
    confirm_ownership = data.get('confirm_ownership', False)

    if not url:
        return jsonify({"error": "URL is required."}), 400
    if not confirm_ownership:
        return jsonify({"error": "You must confirm ownership of the domain to scan."}), 403

    try:
        hostname = urlparse(url).hostname
        if not hostname:
            return jsonify({"error": "Invalid URL provided."}), 400

        command = ["nmap", "-F", hostname]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180
        )

        scan_output = result.stdout
        if result.stderr:
            scan_output += "\n--- STDERR ---\n" + result.stderr

        summary_prompt = "You are a cybersecurity expert."
        mock_summary = get_mock_ai_response(summary_prompt, scan_output)

        return jsonify({
            "status": "scan_completed",
            "hostname": hostname,
            "summary": mock_summary,
            "raw_output": scan_output
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": f"Scan for {hostname} timed out."}), 504
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Route to serve the main index.html file
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Route to serve other static files (CSS, JS)
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
