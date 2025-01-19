from joblib import Parallel, delayed
import requests
import random
 
SERVER_URL = "https://fastapi-analytics-webapp.azurewebsites.net/process_event"

def generate_user_id():
    return f"user{random.randint(1, 1000)}"

def generate_event_name():
    return f"event{random.randint(1, 1000)}"

def send_request():
    user_id = generate_user_id()
    event_name = generate_event_name()
    payload = {"userid": user_id, "eventname": event_name}
    response = requests.post(SERVER_URL, json=payload)
    return f"Sent: {payload}, Response: {response.status_code}, {response.text}"

if __name__ == "__main__":
    num_requests = 1000 
    print(f"Sending {num_requests} requests to {SERVER_URL} in parallel...")
    results = Parallel(n_jobs=-1)(delayed(send_request)() for _ in range(num_requests))
    for result in results[:10]:
        print(result)
    print(f"Completed {num_requests} requests.")