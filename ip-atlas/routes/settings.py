from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os
from dotenv import load_dotenv
from utils.settings import load_settings, save_settings

load_dotenv()

settings_bp = Blueprint('settings', __name__)

SETTINGS_USER = os.getenv('SETTINGS_USER')
SETTINGS_PASSWORD = os.getenv('SETTINGS_PASSWORD')

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'logged_in' not in session:
        return redirect(url_for('settings.login'))
    
    if request.method == 'POST':
        ip_ranges = []
        index = 0
        while True:
            ip_range = request.form.get(f'ip_ranges[{index}][range]')
            interface = request.form.get(f'ip_ranges[{index}][interface]')
            if ip_range and interface:
                ip_ranges.append({'range': ip_range, 'interface': interface})
            else:
                break
            index += 1

        settings = {
            'ip_ranges': ip_ranges,
            'scan_frequency': int(request.form.get('scan_frequency')),
            'site_title': request.form.get('site_title')
        }
        
        save_settings(settings)
        flash('Einstellungen wurden erfolgreich gespeichert.')
        return redirect(url_for('settings.settings'))
    
    settings = load_settings()
    return render_template('settingsPage.html', settings=settings)

@settings_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == SETTINGS_USER and password == SETTINGS_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('settings.settings'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')
