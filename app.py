from flask import Flask, render_template, request, send_file
from utils.qr_code_generator import generate_qr_code
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    qr_code_options = [
        "Link", "vCard", "Email", "SMS", "Phone Number", "Text", 
        "Wi-Fi", "Calendar Event", "Location", "Bitcoin Address"
    ]
    return render_template('index.html', options=qr_code_options)

@app.route('/link_form')
def link_form():
    return """
        <label for="data">Enter Link:</label>
        <input type="url" id="data" name="data" required>
    """

@app.route('/text_form')
def text_form():
    return """
        <label for="data">Enter Text:</label>
        <textarea id="data" name="data" required></textarea>
    """

@app.route('/vcard_form')
def vcard_form():
    return render_template('vcard_form.html')

@app.route('/email_form')
def email_form():
    return render_template('email_form.html')

@app.route('/sms_form')
def sms_form():
    return render_template('sms_form.html')

@app.route('/phone_number_form')
def phone_number_form():
    return render_template('phone_number_form.html')

@app.route('/wi-fi_form')
def wifi_form():
    return render_template('wi-fi_form.html')

@app.route('/bitcoin_address_form')
def bitcoin_address_form():
    return render_template('bitcoin_adress_form.html')

@app.route('/calendar_event_form')
def calendar_event_form():
    return render_template('calendar_event_form.html')

@app.route('/location_form')
def location_form():
    return render_template('location_form.html')

@app.route('/generate', methods=['POST'])
def generate():
    data_type = request.form['data_type']
    with_logo = 'with_logo' in request.form
    logo_path = None

    if with_logo and 'logo' in request.files:
        logo = request.files['logo']
        if logo.filename != '':
            filename = secure_filename(logo.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logo.save(logo_path)

    if data_type == "vCard":
        data = {
            'first_name': request.form.get('first_name', ''),
            'last_name': request.form.get('last_name', ''),
            'mobile': request.form.get('mobile', ''),
            'phone': request.form.get('phone', ''),
            'fax': request.form.get('fax', ''),
            'email': request.form.get('email', ''),
            'company': request.form.get('company', ''),
            'job_title': request.form.get('job_title', ''),
            'street': request.form.get('street', ''),
            'city': request.form.get('city', ''),
            'state': request.form.get('state', ''),
            'zip': request.form.get('zip', ''),
            'country': request.form.get('country', ''),
            'website': request.form.get('website', '')
        }
    elif data_type == "Email":
        data = {
            'email': request.form.get('email', ''),
            'subject': request.form.get('subject', ''),
            'message': request.form.get('message', '')
        }
    elif data_type == "SMS":
        data = {
            'number': request.form.get('number', ''),
            'message': request.form.get('message', '')
        }
    elif data_type == "Phone Number":
        data = {
            'country_code': request.form.get('country_code', ''),
            'number': request.form.get('number', '')
        }
    elif data_type == "Wi-Fi":
        data = {
            'ssid': request.form.get('ssid', ''),
            'password': request.form.get('password', ''),
            'encryption': request.form.get('encryption', ''),
            'hidden': 'hidden' in request.form
        }
    elif data_type == "Bitcoin Address":
        data = {
            'cryptocurrency': request.form.get('cryptocurrency', ''),
            'amount': request.form.get('amount', ''),
            'receiver': request.form.get('receiver', ''),
            'message': request.form.get('message', '')
        }
    elif data_type == "Calendar Event":
        data = {
            'event_name': request.form.get('event_name', ''),
            'event_date': request.form.get('event_date', ''),
            'event_time': request.form.get('event_time', '09:00'),
            'event_location': request.form.get('event_location', ''),
            'event_notes': request.form.get('event_notes', ''),
            'event_invitees': request.form.get('event_invitees', '')
        }
    elif data_type == "Location":
        data = {
            'address': request.form.get('address', ''),
            'zip': request.form.get('zip', '')
        }
    else:
        data = request.form['data']

    qr_code_path = generate_qr_code(data, data_type, with_logo, logo_path)
    return send_file(qr_code_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
