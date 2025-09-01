import nmap
import logging
import subprocess
import requests
from scapy.all import sniff
from sklearn.externals import joblib
from ollama_scanner import analyze_service_with_ollama, generate_payloads_with_ollama
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIEthicalHacker:
    """
    An AI-powered ethical hacking tool for vulnerability assessment.
    """

    def __init__(self, target):
        """
        Initializes the AIEthicalHacker with a target.

        :param target: The target to scan (e.g., an IP address or a domain name).
        """
        self.target = target
        self.nmap = nmap.PortScanner()
        self.ai_model = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'AIEthicalHacker/1.0'})

    def run_nmap_scan(self, arguments='-sV'):
        """
        Runs an Nmap scan on the target.

        :param arguments: The arguments to pass to Nmap (e.g., '-sV -p 1-1000').
        :return: The Nmap scan results.
        """
        logging.info(f"Running Nmap scan on {self.target} with arguments: {arguments}")
        try:
            self.nmap.scan(self.target, arguments=arguments)
            logging.info(f"Nmap scan completed for {self.target}")
            return self.nmap.csv()
        except nmap.PortScannerError as e:
            logging.error(f"Nmap scan failed: {e}")
            return None

    def run_burp_suite(self):
        """
        Placeholder for running Burp Suite.
        """
        logging.info("Burp Suite integration is not implemented in this version.")

    def run_metasploit(self):
        """
        Placeholder for running Metasploit.
        """
        logging.info("Metasploit integration is not implemented in this version.")

    def load_ai_model(self, model_path='vulnerability_scanner.pkl'):
        """
        Loads a pre-trained AI model for vulnerability scanning.
        """
        logging.info(f"Loading AI model from {model_path}")
        try:
            self.ai_model = joblib.load(model_path)
            logging.info("AI model loaded successfully.")
        except FileNotFoundError:
            logging.error(f"AI model file not found at {model_path}. Please train a model first.")
            self.ai_model = None

    def scan_with_ai(self, scan_results):
        """
        Uses the loaded AI model to predict vulnerabilities based on scan results.
        """
        if self.ai_model is None:
            logging.warning("AI model is not loaded. Cannot perform AI-powered scan.")
            return []
        logging.info("Scanning with AI model...")
        print("Placeholder: Scan with AI model.")
        return ["Potential SQL Injection", "Potential Cross-Site Scripting"]

    def fuzz_web_application(self, url, payloads):
        """
        Performs fuzzing on a web application by sending a list of payloads.
        """
        logging.info(f"Fuzzing {url} with {len(payloads)} payloads.")
        for payload in payloads:
            try:
                # This is a simplified fuzzer. A real one would substitute payloads in different places.
                fuzz_url = f"{url}?q={payload}"
                response = self.session.get(fuzz_url)
                # A simple check for potential issues. Real analysis would be more complex.
                if response.status_code == 500 or "error" in response.text.lower() or "exception" in response.text.lower():
                    logging.warning(f"Potential vulnerability found at {fuzz_url} with payload: {payload}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed for payload {payload}: {e}")

    def brute_force_login(self, url, usernames, passwords):
        """
        Performs a simple brute-force attack on a login page.
        """
        logging.warning("Starting brute-force attack. Use this responsibly.")
        for username in usernames:
            for password in passwords:
                try:
                    response = self.session.post(url, data={'username': username, 'password': password})
                    if "welcome" in response.text or "dashboard" in response.text:
                        logging.info(f"Successful login with {username}:{password}")
                        return username, password
                except requests.exceptions.RequestException as e:
                    logging.error(f"Request failed for {username}:{password}: {e}")
        logging.info("Brute-force attack finished. No credentials found.")
        return None, None

    def analyze_network_traffic(self, packet_count=100):
        """
        Captures and analyzes network traffic to detect suspicious patterns.
        """
        logging.info(f"Capturing {packet_count} packets for analysis...")
        packets = sniff(count=packet_count)
        logging.info(f"Captured {len(packets)} packets.")
        for packet in packets:
            if packet.haslayer("IP") and packet["IP"].flags == 4:
                logging.warning(f"Suspicious packet found: {packet.summary()}")

    def scan_service_with_ollama(self, service_info):
        """
        Analyzes a single service using the connected Ollama LLM.
        """
        logging.info(f"Scanning '{service_info}' with Ollama...")
        return analyze_service_with_ollama(service_info)

    def crawl_website(self, base_url):
        """
        Crawls a website to find all unique internal links.

        :param base_url: The URL to start crawling from.
        :return: A set of unique URLs found on the site.
        """
        logging.info(f"Crawling website: {base_url}")
        urls_to_visit = [base_url]
        visited_urls = set()
        base_netloc = urlparse(base_url).netloc

        while urls_to_visit:
            current_url = urls_to_visit.pop(0)
            if current_url in visited_urls:
                continue

            try:
                response = self.session.get(current_url, timeout=5)
                visited_urls.add(current_url)
                logging.info(f"Visiting: {current_url}")

                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(base_url, link['href'])
                    # Stay on the same domain
                    if urlparse(absolute_link).netloc == base_netloc:
                        if absolute_link not in visited_urls and absolute_link not in urls_to_visit:
                            urls_to_visit.append(absolute_link)

            except requests.exceptions.RequestException as e:
                logging.error(f"Could not get URL {current_url}: {e}")

        logging.info(f"Crawling finished. Found {len(visited_urls)} unique URLs.")
        return visited_urls

    def scan_website_with_ai_payloads(self, base_url):
        """
        Orchestrates a full website scan: crawls, generates AI payloads, and fuzzes.

        :param base_url: The base URL of the website to scan.
        """
        logging.info(f"Starting full AI-powered scan for {base_url}")

        # Step 1: Crawl the website to find targets
        target_urls = self.crawl_website(base_url)

        # Step 2: For each URL, generate payloads and fuzz
        for url in target_urls:
            logging.info(f"--- Scanning URL: {url} ---")

            # Step 2a: Create a context for the AI
            # A more advanced version could analyze the URL/page content for better context
            context = f"a generic web page with potential URL parameter vulnerabilities. The URL is {url}"

            # Step 2b: Generate payloads with AI
            ai_payloads = generate_payloads_with_ollama(context, num_payloads=5)
            if not ai_payloads or "Error" in ai_payloads[0]:
                logging.error(f"Could not generate payloads for {url}: {ai_payloads[0] if ai_payloads else 'Empty response'}")
                continue

            # Step 2c: Fuzz the URL with the generated payloads
            self.fuzz_web_application(url, ai_payloads)


if __name__ == '__main__':
    # This tool can be used to scan an IP address or a website.
    # Choose your target type. For web scanning, a domain is better.
    target = "127.0.0.1"
    hacker = AIEthicalHacker(target)

    # --- Example of Nmap Scan ---
    # print("--- Nmap Scan ---")
    # nmap_results = hacker.run_nmap_scan()
    # if nmap_results:
    #     print(nmap_results)

    # --- Example of using Ollama for service analysis ---
    # print("\n--- Ollama Analysis ---")
    # service_to_check = "vsftpd 2.3.4"
    # ollama_assessment = hacker.scan_service_with_ollama(service_to_check)
    # print(f"Ollama assessment for '{service_to_check}': {ollama_assessment}")

    # --- NEW: Example of Full AI-Powered Website Scan ---
    # Note: Replace with a URL from a test environment you are authorized to test.
    # Make sure Ollama is running!
    print("\n--- Full AI-Powered Website Scan ---")
    web_target = "http://testphp.vulnweb.com" # A known-vulnerable test site
    hacker.scan_website_with_ai_payloads(web_target)
