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

    # --- Example of generating payloads ---
    print("\n--- AI Payload Generation Example ---")
    context = "a numeric ID parameter in a URL that might be vulnerable to SQL injection"
    generated_payloads = generate_payloads_with_ollama(context)
    print(f"\nPayloads generated for context: '{context}'")
    for payload in generated_payloads:
        print(f"- {payload}")

def generate_payloads_with_ollama(context, num_payloads=10, model="llama2"):
    """
    Generates a list of fuzzing payloads using an Ollama LLM.

    :param context: A string describing the context for the payloads (e.g., "SQL injection").
    :param num_payloads: The number of payloads to generate.
    :param model: The name of the Ollama model to use.
    :return: A list of payload strings.
    """
    print(f"Generating {num_payloads} payloads for context: '{context}'...")

    prompt = f"""
    You are a cybersecurity expert specializing in web application penetration testing.
    Based on the following context, generate a list of {num_payloads} creative and effective fuzzing payloads.
    The payloads should be designed to test for common web vulnerabilities.

    Context: "{context}"

    IMPORTANT: Return ONLY a Python-parseable list of strings and nothing else. Do not include any explanation or surrounding text.
    Example output: ["' OR 1=1 --", "<script>alert('XSS')</script>", " UNION SELECT null,null--"]
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        response_text = response.json().get("response", "[]").strip()

        # The LLM might sometimes include markdown backticks. We remove them.
        if response_text.startswith("```python"):
            response_text = response_text.replace("```python", "").replace("```", "")

        # Safely evaluate the string as a Python literal (list)
        payloads = json.loads(response_text)
        if isinstance(payloads, list):
            return payloads
        else:
            return ["Error: LLM did not return a valid list."]

    except requests.exceptions.ConnectionError:
        return ["Error: Could not connect to the Ollama server."]
    except json.JSONDecodeError:
        return [f"Error: Could not decode the LLM's response: {response_text}"]
    except Exception as e:
        return [f"An error occurred: {e}"]
