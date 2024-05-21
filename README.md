---

# IP-Atlas

IP-Atlas ist eine Flask-Anwendung zur effizienten Verwaltung von IP-Adressen in großen Netzwerken. Benutzer können Adressen speichern, Namen zuweisen und durch Oktettensortierung den Überblick behalten. Ideal für Netzwerkadministratoren, bietet es eine benutzerfreundliche Oberfläche und Netzwerkstatistiken.

## Features

- Effiziente Verwaltung von IP-Adressen
- Benutzerfreundliche Oberfläche
- Oktettensortierung zur einfachen Navigation
- Umfassende Netzwerkstatistiken

## Voraussetzungen

- Linux-Distribution (empfohlen: Ubuntu über WSL auf Windows)
- Python 3
- Node.js und npm
  - [Download und Installation](https://nodejs.org/en/download/package-manager)

## Einrichtung

1. WSL (Windows Subsystem for Linux) installieren und Ubuntu einrichten:
   - [Installationsanleitung für WSL](https://docs.microsoft.com/en-us/windows/wsl/install)

2. Repository klonen:
    ```sh
    git clone <repository-url>
    ```
3. In das Projektverzeichnis wechseln:
    ```sh
    cd ip-atlas
    ```
4. Installieren Sie die Python-Abhängigkeiten global mit sudo:
    ```sh
    sudo pip install -r requirements.txt
    ```
5. Installieren Sie Node.js und npm, dann die erforderlichen npm-Pakete und erstellen Sie die CSS-Dateien:
    ```sh
    npm install
    npm run create-css
    ```
6. Erstellen Sie eine `.env` Datei im IP-Atlas Ordner und fügen Sie die notwendigen Umgebungsvariablen hinzu:
    ```sh
    touch .env
    nano .env
    ```
    Fügen Sie die folgenden Zeilen hinzu und speichern Sie die Datei:
    ```
    PASSWORD="___"
    SETTINGS_USER="___"
    SETTINGS_PASSWORD="___"
    SECRET_KEY="___"
    ```

## ARP Scanner einrichten

- Scapy
  - [Installationsanleitung für Ubuntu](https://rootinstall.com/tutorial/how-to-install-scapy-on-ubuntu/)

Derzeit funktioniert der Scanner nur auf Linux-Distributionen.

## Anwendung starten

Führen Sie das [`atlasapp`](ip-atlas/app.py) Skript aus:
```sh
python3 ip-atlas/app.py
```

## Routen

Die Anwendungsrouten sind im [`atlas`](ip-atlas/routes/atlas.py) Modul definiert.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

---