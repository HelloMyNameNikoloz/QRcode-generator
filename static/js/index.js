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

function loadForm(option) {
    const formContent = document.getElementById('form-content');
    const optionFormatted = option.toLowerCase().replace(' ', '_');

    fetch(`/${optionFormatted}_form`)
        .then(response => response.text())
        .then(html => {
            formContent.innerHTML = html;
            // Add hidden input to store the data type
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'data_type';
            hiddenInput.value = option;
            formContent.appendChild(hiddenInput);
        })
        .catch(error => console.error('Error loading form:', error));
}

function selectOption(option) {
    const circles = document.querySelectorAll('.option-circle');
    circles.forEach(circle => {
        if (circle.textContent === option) {
            circle.classList.add('selected');
        } else {
            circle.classList.remove('selected');
        }
    });
    loadForm(option);
}

document.addEventListener('DOMContentLoaded', function () {
    selectOption('Link'); // Load default form on page load
});
