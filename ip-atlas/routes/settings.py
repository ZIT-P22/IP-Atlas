from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.settings import load_settings, save_settings
import os

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'logged_in' not in session:
        return redirect(url_for('settings.login'))

    settings = load_settings()

    if request.method == 'POST':
        ip_ranges = []
        for range, interface in zip(request.form.getlist('ip_ranges[range]'), request.form.getlist('ip_ranges[interface]')):
            ip_ranges.append({'range': range, 'interface': interface})
        
        settings['ip_ranges'] = ip_ranges
        settings['scan_frequency'] = int(request.form.get('scan_frequency'))
        settings['site_title'] = request.form.get('site_title')
        
        save_settings(settings)
        flash('Einstellungen wurden erfolgreich gespeichert.')
        return redirect(url_for('settings.settings'))

    return render_template('settingsPage.html', settings=settings)

@settings_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Load settings from .env file
    SETTINGS_USER = os.getenv('SETTINGS_USER')
    SETTINGS_PASSWORD = os.getenv('SETTINGS_PASSWORD')
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
