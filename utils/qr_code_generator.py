import qrcode
from PIL import Image
from datetime import datetime
import base64

def generate_qr_code(data, data_type, with_logo, logo_path=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    if data_type == "Link":
        qr.add_data(data)
    elif data_type == "vCard":
        vcard_data = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"N:{data['last_name']};{data['first_name']}\n"
            f"FN:{data['first_name']} {data['last_name']}\n"
            f"ORG:{data['company']}\n"
            f"TITLE:{data['job_title']}\n"
            f"TEL;WORK;VOICE:{data['mobile']}\n"
            f"TEL;CELL:{data['phone']}\n"
            f"TEL;FAX:{data['fax']}\n"
            f"EMAIL;WORK;INTERNET:{data['email']}\n"
            f"ADR;WORK:;;{data['street']};{data['city']};{data['state']};{data['zip']};{data['country']}\n"
            f"URL:{data['website']}\n"
            "END:VCARD"
        )
        qr.add_data(vcard_data)
    elif data_type == "Email":
        email_data = (
            f"mailto:{data['email']}?subject={data['subject']}&body={data['message']}"
        )
        qr.add_data(email_data)
    elif data_type == "SMS":
        sms_data = f"smsto:{data['number']}:{data['message']}"
        qr.add_data(sms_data)
    elif data_type == "Phone Number":
        phone_number_data = f"tel:{data['country_code']}{data['number']}"
        qr.add_data(phone_number_data)
    elif data_type == "Wi-Fi":
        wifi_data = f"WIFI:T:{data['encryption']};S:{data['ssid']};P:{data['password']};H:{'true' if data['hidden'] else 'false'};;"
        qr.add_data(wifi_data)
    elif data_type == "Bitcoin Address":
        bitcoin_data = f"{data['cryptocurrency']}:{data['receiver']}?amount={data['amount']}&message={data['message']}"
        qr.add_data(bitcoin_data)
    elif data_type == "Calendar Event":
        event_start = datetime.strptime(f"{data['event_date']} {data['event_time']}", "%Y-%m-%d %H:%M")
        event_end = event_start  # or add a default duration if desired
        event_start_str = event_start.strftime("%Y%m%dT%H%M%S")
        event_end_str = event_end.strftime("%Y%m%dT%H%M%S")

        calendar_data = (
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "BEGIN:VEVENT\n"
            f"SUMMARY:{data['event_name']}\n"
            f"DTSTART:{event_start_str}\n"
            f"DTEND:{event_end_str}\n"
            f"LOCATION:{data['event_location']}\n"
            f"DESCRIPTION:{data['event_notes']}\n"
            f"ATTENDEE;CN={data['event_invitees']}\n"
            "END:VEVENT\n"
            "END:VCALENDAR"
        )
        qr.add_data(calendar_data)
    elif data_type == "Location":
        address = f"{data['address']} {data['zip']}".replace(" ", "+")
        location_data = f"https://www.google.com/maps/search/?api=1&query={address}"
        qr.add_data(location_data)
    # Add more data type handling as needed

    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    if with_logo and logo_path:
        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")

        # Calculate logo size
        basewidth = img.size[0] // 4
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        # Calculate positioning
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo)

    qr_code_path = 'static/qr_code.png'
    img.save(qr_code_path)
    return qr_code_path
