import requests

def control_smart_home(device, action):
    url = "http://your-smart-home-api-endpoint"
    data = {"device": device, "action": action}
    response = requests.post(url, json=data)
    return f"{device} turned {action}" if response.status_code == 200 else f"Failed to control {device}"
