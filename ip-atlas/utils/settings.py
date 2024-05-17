import os
import json

SETTINGS_FILE = 'ip-atlas/data/settings.json'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {
        'ip_ranges': [
            {'range': '192.168.0.0/24', 'interface': 'eth0'},
            {'range': '10.0.0.0/24', 'interface': 'wlan0'}
        ],
        'scan_frequency': 10,
        'site_title': 'IP-Atlas'
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)