import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('subprocess.run')
def test_scan_valid_hostname(mock_run, client):
    """Test scanning a valid hostname."""
    mock_run.return_value.stdout = "Nmap scan report for example.com"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0

    response = client.post('/scan', json={'url': 'http://example.com', 'confirm_ownership': True})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['hostname'] == 'example.com'
    assert 'Nmap scan report' in json_data['raw_output']
    mock_run.assert_called_with(["nmap", "-F", "example.com"], capture_output=True, text=True, timeout=180)


def test_scan_invalid_hostname_injection(client):
    """Test scanning an invalid hostname to prevent argument injection."""
    response = client.post('/scan', json={'url': 'http://-oA shell.txt', 'confirm_ownership': True})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'Invalid hostname provided' in json_data['error']

def test_scan_invalid_hostname_chars(client):
    """Test scanning a hostname with invalid characters."""
    response = client.post('/scan', json={'url': 'http://invalid-.com', 'confirm_ownership': True})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'Invalid hostname provided' in json_data['error']

def test_scan_hostname_with_underscore(client):
    """Test scanning a hostname with an underscore, which is not allowed."""
    response = client.post('/scan', json={'url': 'http://invalid_host.com', 'confirm_ownership': True})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'Invalid hostname provided' in json_data['error']


def test_scan_no_hostname(client):
    """Test scanning with no hostname."""
    response = client.post('/scan', json={'url': 'http://', 'confirm_ownership': True})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'Invalid URL provided' in json_data['error']
