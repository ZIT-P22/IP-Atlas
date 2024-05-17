from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import os
import json

settings_bp = Blueprint('settings', __name__)

# Pfad zur JSON-Datei
SETTINGS_FILE = 'ip-atlas/data/settings.json'

# Laden Sie die Einstellungen aus der JSON-Datei
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
    else:
        settings = {
            'ip_ranges': [{'range': '', 'interface': ''}],
            'scan_frequency': '',
            'site_title': ''
        }
    return settings

# Speichern Sie die Einstellungen in die JSON-Datei
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('settings.login'))

    if request.method == 'POST':
        ip_ranges = [
            {'range': request.form[f'ip_ranges[{i}][range]'], 'interface': request.form[f'ip_ranges[{i}][interface]']}
            for i in range(len(request.form)//2) if f'ip_ranges[{i}][range]' in request.form
        ]
        settings = {
            'ip_ranges': ip_ranges,
            'scan_frequency': request.form['scan_frequency'],
            'site_title': request.form['site_title']
        }
        save_settings(settings)
        flash('Einstellungen erfolgreich gespeichert.', 'success')
        return redirect(url_for('settings.settings'))

    settings = load_settings()
    return render_template('settingsPage.html', settings=settings)

@settings_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == os.getenv('ADMIN_USER') and password == os.getenv('ADMIN_PASSWORD'):
            session['logged_in'] = True
            flash('Erfolgreich eingeloggt.', 'success')
            return redirect(url_for('settings.settings'))
        else:
            flash('Ungültiger Benutzername oder Passwort.', 'danger')

    return render_template('login.html')
