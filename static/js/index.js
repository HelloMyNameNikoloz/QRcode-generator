// static/js/index.js
document.getElementById('qr-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    
    fetch('/generate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const img = document.createElement('img');
        img.src = url;
        const qrCodeDiv = document.getElementById('qr-code');
        qrCodeDiv.innerHTML = '';  // Clear previous QR code
        qrCodeDiv.appendChild(img);
    })
    .catch(error => console.error('Error:', error));
});

function toggleLogoUpload() {
    const logoUpload = document.getElementById('logo-upload');
    if (document.getElementById('with_logo').checked) {
        logoUpload.style.display = 'block';
    } else {
        logoUpload.style.display = 'none';
    }
}

function loadForm() {
    const dataType = document.getElementById('data_type').value;
    const formContent = document.getElementById('form-content');

    if (dataType === "vCard") {
        fetch('/vcard_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else if (dataType === "Email") {
        fetch('/email_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else if (dataType === "SMS") {
        fetch('/sms_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else if (dataType === "Phone Number") {
        fetch('/phone_number_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else if (dataType === "Wi-Fi") {
        fetch('/wifi_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else if (dataType === "Bitcoin Address") {
        fetch('/bitcoin_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else if (dataType === "Calendar Event") {
        fetch('/calendar_event_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else if (dataType === "Location") {
        fetch('/location_form')
            .then(response => response.text())
            .then(html => {
                formContent.innerHTML = html;
            })
            .catch(error => console.error('Error:', error));
    } else {
        formContent.innerHTML = `
            <label for="data">Enter Data:</label>
            <input type="text" id="data" name="data" required>
        `;
    }
}
