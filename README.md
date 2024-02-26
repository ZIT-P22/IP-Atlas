# IP-Atlas
IP Navigator ist eine Flask-Anwendung für die unkomplizierte Verwaltung von IP-Adressen in großen Netzwerken. Benutzer können Adressen speichern, Namen zuweisen und durch die Oktetten-Sortierung den Überblick behalten. Ideal für Netzwerkadministratoren, bietet eine benutzerfreundliche Oberfläche und Netzwerkstatistiken.

# IP-Atlas

IP Navigator is a Flask application designed for the efficient management of IP addresses in large networks. It allows users to store addresses, assign names, and maintain an overview through octet sorting. Ideal for network administrators, it offers a user-friendly interface and network statistics.

## Features
- Efficient IP address management
- User-friendly interface
- Octet sorting for easy navigation
- Comprehensive network statistics

## Prerequisites
- Python 3
- Node.js and npm

## Setup
1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd ip-atlas
    ```
3. Create a virtual environment:
    ```sh
    python3 -m venv .atlas
    ```
4. Activate the virtual environment:
    - For bash: `source .atlas/bin/activate`
    - For fish: `. .atlas/bin/activate.fish`
    - For csh: `source .atlas/bin/activate.csh`
    - For PowerShell: `. .atlas/bin/Activate.ps1`
5. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
6. Install Node.js and npm, then install the required npm packages and create the CSS files:
    ```sh
    npm install
    npm run create-css
    ```

## Setup ARP Scanner

- Scapy
    - https://rootinstall.com/tutorial/how-to-install-scapy-on-windows/
    - https://rootinstall.com/tutorial/how-to-install-scapy-on-ubuntu/

1. Open a terminal on your Linux system.
Run the following command to edit the sudoers file using the visudo command:

``` bash
sudo visudo
```
2. Add a sudoers configuration for your Flask project
Scroll to the end of the sudoers file and add the following line:

```ruby
username ALL=(ALL) NOPASSWD: /usr/bin/python3 /path/to/ip-atlas/utils/netscan.py
```
Replace username with the username under which your Flask project runs.
Replace /path/to/ip-atlas/utils/netscan.py with the actual path to your script.

For example, if your Flask project runs under the username flaskuser and the script is located at /home/flaskuser/ip-atlas/utils/netscan.py, the line would look like this:

```ruby
flaskuser ALL=(ALL) NOPASSWD: /usr/bin/python3 /home/flaskuser/ip-atlas/utils/netscan.py
```
Save the sudoers file and exit the text editor.

## Starting the Application
Run the [`atlasapp`](ip-atlas/app.py) script:
```sh
python ip-atlas/app.py
```

## Routes
Application routes are defined in the [`atlas`](ip-atlas/routes/atlas.py) module.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
