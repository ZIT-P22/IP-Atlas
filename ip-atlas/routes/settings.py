from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os

settings_bp = Blueprint('settings', __name__)

# Load settings from .env file
SETTINGS_USER = os.getenv('SETTINGS_USER')
SETTINGS_PASSWORD = os.getenv('SETTINGS_PASSWORD')

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'logged_in' not in session:
        return redirect(url_for('settings.login'))

    # Load settings from JSON or other storage
    settings = {
        'ip_ranges': [
            {'range': '192.168.0.0/24', 'interface': 'eth0'},
            {'range': '10.0.0.0/24', 'interface': 'wlan0'}
        ],
        'scan_frequency': 10,
        'site_title': 'IP-Atlas'
    }

    if request.method == 'POST':
        # Process form data and save settings
        settings['ip_ranges'] = request.form.getlist('ip_ranges')
        settings['scan_frequency'] = request.form.get('scan_frequency')
        settings['site_title'] = request.form.get('site_title')
        # Save the settings to JSON or other storage
        flash('Einstellungen wurden erfolgreich gespeichert.')
        return redirect(url_for('settings.settings'))

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
            flash('Ungültige Anmeldeinformationen.')
    return render_template('login.html')


@settings_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('settings.login'))
