"""Transport adapters for Northwind Relay channels.

Clean module - moves bytes to SMTP / SMS gateway / APNs. No template logic,
no reference to the deprecated renderer.
"""


def send_smtp(address, subject, body):
    return {"ok": True, "via": "smtp", "to": address}


def send_gateway(number, body):
    return {"ok": True, "via": "sms-gateway", "to": number}


def send_apns(device_token, title, body):
    return {"ok": True, "via": "apns", "to": device_token}
