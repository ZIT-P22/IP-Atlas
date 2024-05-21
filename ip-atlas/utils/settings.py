import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, '../data/settings.json')

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {
        'ip_ranges': [
            {'range': '192.168.120.0/24', 'interface': 'eth1'},
            {'range': '172.16.0.0/16', 'interface': 'eth0'}
        ],
        'scan_frequency': 10,
        'site_title': 'IP-Atlas'
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)
