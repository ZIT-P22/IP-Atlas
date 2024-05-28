let currentDeviceId = null;
let currentIPv4 = null;

function openModal(ipv4, id) {
    currentDeviceId = id;
    currentIPv4 = ipv4;

    fetch(`/check_ipv4/${ipv4}`)
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                document.getElementById("existingDeviceModal").classList.remove("hidden");
            } else {
                document.getElementById("modal-ipv4").value = ipv4;
                document.getElementById("addIpModal").classList.remove("hidden");
            }
        })
        .catch(error => console.error('Error:', error));
}

function closeModal() {
    document.getElementById("addIpModal").classList.add("hidden");
    document.getElementById("existingDeviceModal").classList.add("hidden");
}

function validateInput() {
    var ipv4Regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    var ipv6Regex = /^(([0-9a-fA-F]{1,4}:){6}|([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){5}:(:[0-9a-fA-F]{1,2}){1,2}|([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4})$/i;
    var portsRegex = /^(\d+\s*,\s*)*\d+$/;

    var ipv4Input = document.getElementById("modal-ipv4").value;
    var ipv6Input = document.getElementById("ipv6").value;
    var portsInput = document.getElementById("ports").value;

    var isValid = true;

    if (ipv4Input && !ipv4Regex.test(ipv4Input)) {
        isValid = false;
        alert("Ungültige IPv4-Adresse");
    }

    if (ipv6Input && !ipv6Regex.test(ipv6Input)) {
        isValid = false;
        alert("Ungültige IPv6-Adresse");
    }

    if (portsInput && !portsRegex.test(portsInput)) {
        isValid = false;
        alert("Ungültiges Format für Ports");
    }

    return isValid;
}

function handleFormSubmit(event) {
    event.preventDefault();
    if (validateInput()) {
        fetch(`/set_used/${currentDeviceId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'used_set') {
                document.getElementById("addIpForm").submit();
            } else {
                alert("Fehler: Gerät konnte nicht als verwendet markiert werden");
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function handleExistingDeviceResponse(choice) {
    if (choice === 'delete') {
        // Logic to delete the existing device goes here
        alert("Delete functionality not implemented yet.");  // Replace this with actual delete logic
    } else if (choice === 'replace') {
        document.getElementById("existingDeviceModal").classList.add("hidden");
        document.getElementById("modal-ipv4").value = currentIPv4;
        document.getElementById("addIpModal").classList.remove("hidden");

        // Set the form's onsubmit handler to handleEditFormSubmit
        document.getElementById("addIpForm").onsubmit = handleEditFormSubmit;
    }
}

function handleEditFormSubmit(event) {
    event.preventDefault();
    if (validateInput()) {
        const formData = new FormData(document.getElementById("addIpForm"));
        formData.append("id", currentDeviceId);  // Add the current device ID to the form data

        fetch(`/edit_device`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                fetch(`/set_used/${currentDeviceId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'used_set') {
                        alert("Gerät wurde erfolgreich ersetzt.");
                        location.reload();  // Refresh the page to reflect changes
                    } else {
                        alert("Fehler: Gerät konnte nicht als verwendet markiert werden.");
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                alert("Fehler: Gerät konnte nicht ersetzt werden.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Fehler beim Senden der Daten.");
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const startScanButton = document.getElementById('start-scan');
    const progressBar = document.getElementById('progress-bar');
    const progressElement = document.getElementById('progress');

    startScanButton.addEventListener('click', function() {
        progressBar.classList.remove('hidden');
        startScanButton.disabled = true;

        fetch('/start_scan', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'scan_started') {
                    updateProgress();
                }
            });
    });

    function updateProgress() {
        fetch('/scan_progress')
            .then(response => response.json())
            .then(data => {
                const percentage = (data.completed / data.total) * 100;
                progressElement.style.width = percentage + '%';
                progressElement.textContent = Math.round(percentage) + '%';

                if (data.status === 'scanning') {
                    setTimeout(updateProgress, 1000);
                } else {
                    fetchResults();
                    startScanButton.disabled = false;
                }
            });
    }

    function fetchResults() {
        fetch('/get_results')
            .then(response => response.json())
            .then(data => {
                const deviceList = document.querySelector('.flex.flex-wrap');
                deviceList.innerHTML = '';
                data.devices.forEach(device => {
                    const deviceElement = `
                        <div class="p-4 w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                            <div class="p-6 bg-gray-800 rounded-lg shadow-lg">
                                <div class="mb-6">
                                    <h2 class="text-xl font-semibold text-white">${device.id}</h2>
                                    <div class="mt-2 text-sm text-gray-400">
                                        <p>IP: <span class="text-gray-300">${device.ipv4}</span></p>
                                        <p>MAC Address: <span class="text-gray-300">${device.mac}</span></p>
                                        <p>Vendor: <span class="text-gray-300">${device.vendor}</span></p>
                                        <p>First Seen: <span class="text-gray-300">${device.first_seen}</span></p>
                                        <p>Last Seen: <span class="text-gray-300">${device.last_seen}</span></p>
                                    </div>
                                </div>
                                <div class="flex justify-end space-x-4">
                                    <button aria-label="Add to IP list" class="text-4xl" onclick="openModal('${device.ipv4}', ${device.id})">
                                        <span class="text-gray-400 material-symbols-outlined hover:text-blue-400">add_circle</span>
                                    </button>
                                    <button aria-label="Delete device" class="text-4xl">
                                        <span class="text-gray-400 material-symbols-outlined hover:text-red-400">delete</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    deviceList.innerHTML += deviceElement;
                });
                progressBar.classList.add('hidden');
            });
    }
});
