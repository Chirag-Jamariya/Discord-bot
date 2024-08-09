import requests
import json
import time  

def get_upcoming_ctfs(limit=20):

  # Current timestamp in seconds since epoch (adjust for your needs)
  current_timestamp = int(round(time.time()))

  # API endpoint URL with placeholders for limit and timestamp
  url = f"https://ctftime.org/api/v1/events/?limit={limit}&start={current_timestamp}&finish=9999999999"
  headers = {
    "User-Agent": "MyCTFScript/1.0"
  }
  # Send GET request to the API
  response = requests.get(url, headers=headers)

  # Check for successful response
  if response.status_code == 200:
    data = json.loads(response.content)
    return data
    
  else:
    print(f"Error retrieving upcoming CTFs: {response.status_code}")
    return []

if __name__ == "__main__":
  upcoming_ctf_data = get_upcoming_ctfs()

