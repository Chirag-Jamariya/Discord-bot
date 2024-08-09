import requests
import json
import time 
def get_upcoming_hackathons(limit=20):
   
   current_timestamp = int(round(time.time()))

   url=f"https://devpost.com/api/hackathons/?limit={limit}&start={current_timestamp}&finish=9999999999"
   headers = {
    "User-Agent": "MyCTFScript/1.0"
  }
   
   response= requests.get(url,headers=headers)

   if response.status_code==200:
      data = json.loads(response.content)
      return data
   else:
    print(f"Error retrieving upcoming CTFs: {response.status_code}")
    return []

              
if __name__ == "__main__":
    upcoming_hackathon_data = get_upcoming_hackathons()