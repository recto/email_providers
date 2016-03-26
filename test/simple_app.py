import sys
sys.path.append("../src")
import requests, json

def test_email():
    payload = {
      "to": "fake@example.com",
      "to_name": "Ms. Fake",
      "from": "noreply@uber.com",
      "from_name": "Uber",
      "subject": "A message from Uber.",
      "body": "<h1>Your billing amount:</h1><p>$10</p>"
    }
    return requests.post(
        "http://localhost:8000/email",
        data=json.dumps(payload),
        headers={"Content-Type" : "application/json"}
    )

if __name__ == "__main__":
    r = test_email()
    print r.content
