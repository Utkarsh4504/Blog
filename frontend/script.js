document.addEventListener('DOMContentLoaded', () => {
    const modeQueryRadio = document.getElementById('modeQuery');
    const modeScanRadio = document.getElementById('modeScan');
    const textInput = document.getElementById('textInput');
    const submitBtn = document.getElementById('submitBtn');
    const resultsOutput = document.getElementById('results-output');

    // Event listener for mode change
    document.querySelectorAll('input[name="mode"]').forEach(radio => {
        radio.addEventListener('change', (event) => {
            if (event.target.value === 'scan') {
                textInput.placeholder = 'Enter a URL to scan...';
            } else {
                textInput.placeholder = 'Enter your coding question...';
            }
        });
    });

    // Event listener for submit button
    submitBtn.addEventListener('click', async () => {
        const mode = modeQueryRadio.checked ? 'query' : 'scan';
        const input = textInput.value.trim();

        if (!input) {
            resultsOutput.textContent = 'Please enter some input.';
            return;
        }

        submitBtn.disabled = true;
        resultsOutput.textContent = 'Loading...';

        let endpoint = mode === 'query' ? '/query' : '/scan';
        let body = {};

        if (mode === 'query') {
            body = { query: input };
        } else {
            body = {
                url: input
            };
        }

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            });

            const data = await response.json();

            if (!response.ok) {
                // Display backend-provided error
                resultsOutput.textContent = `Error: ${data.error || response.statusText}`;
            } else {
                // Display success response
                if (mode === 'query') {
                    resultsOutput.textContent = data.response;
                } else {
                    resultsOutput.textContent = `Hostname: ${data.hostname}\n\n--- AI Summary ---\n${data.summary}\n\n--- Raw Nmap Output ---\n${data.raw_output}`;
                }
            }
        } catch (error) {
            resultsOutput.textContent = `An unexpected error occurred: ${error.message}`;
        } finally {
            submitBtn.disabled = false;
        }
    });
});
