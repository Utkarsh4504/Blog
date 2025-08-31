import requests
import json

# The default URL for the Ollama API
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def analyze_service_with_ollama(service_info, model="llama2"):
    """
    Analyzes a service by sending a prompt to a running Ollama LLM.

    :param service_info: The string of the service to analyze (e.g., "apache httpd 2.4.29").
    :param model: The name of the Ollama model to use.
    :return: The LLM's response.
    """
    print(f"Analyzing '{service_info}' with Ollama model '{model}'...")

    # A carefully crafted prompt to guide the LLM
    prompt = f"""
    You are a cybersecurity vulnerability analyst. Your task is to provide a brief, one-sentence assessment of a software service based on its name and version.
    Based on your knowledge of public CVEs and common vulnerabilities, is the following service likely to have known critical vulnerabilities?

    Service: "{service_info}"

    Provide your assessment in one sentence.
    """

    # The data payload for the Ollama API
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # We want the full response at once
    }

    try:
        # Send the request to the Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the JSON response
        response_data = response.json()
        return response_data.get("response", "No response from model.").strip()

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the Ollama server. Is Ollama running?"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    # --- Example Usage ---
    print("--- Ollama Vulnerability Scanner Example ---")
    print("Make sure you have Ollama running with a model like 'llama2' or 'mistral'.")
    print("Example: `ollama run llama2` in your terminal.\n")

    # List of services to test
    services_to_test = [
        "vsftpd 2.3.4",          # Known to be very vulnerable
        "apache httpd 2.4.54",   # A more recent, likely patched version
        "openssh 7.6p1",         # Has some known vulnerabilities
        "proftpd 1.3.5"          # Known to be vulnerable
    ]

    for service in services_to_test:
        assessment = analyze_service_with_ollama(service)
        print(f"\n- Service: {service}")
        print(f"  Ollama's Assessment: {assessment}")
