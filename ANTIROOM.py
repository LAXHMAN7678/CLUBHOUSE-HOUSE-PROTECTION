import requests
import time

# Read the bad words from the specified file
with open('badword.txt', 'r') as f:
    bad_words = [line.strip() for line in f.readlines()]

url = "https://www.clubhouse.com/web_api/get_social_club"
headers = {
    'CH-Languages': 'en-US',
    'CH-Locale': 'en_US',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'CH-AppBuild': '304',
    'CH-AppVersion': '0.1.28',
    'CH-UserID': '1387526936',
    'User-Agent': 'clubhouse/304 (iPhone; iOS 14.4; Scale/2.00)',
    'Connection': 'close',
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': 'Token YOURTOKEN'  # Ensure correct token
}

data = {
    "social_club_id": "YOUR CLUBID",
    "is_for_social_club_open": True
}

def check_and_end_bad_rooms():
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        items = response_data.get("items", [])

        filtered_items = [
            {
                "creator_user_profile_id": item.get("channel", {}).get("creator_user_profile_id"),
                "channel_id": item.get("channel", {}).get("channel_id"),
                "channel": item.get("channel", {}).get("channel"),  # 'channel' is the identifier for the room
                "language": item.get("channel", {}).get("language"),
                "visited": item.get("channel", {}).get("visited"),
                "topic": item.get("channel", {}).get("topic")
            }
            for item in items
        ]

        print(filtered_items)

        # Check if any topic contains a bad word and end the channel
        for item in filtered_items:
            topic = item.get("topic", "").lower()
            for bad_word in bad_words:
                if bad_word.lower() in topic:
                    channel = item.get("channel")  # Use 'channel' here
                    print(f"Bad word found in room topic: {topic}")
                    print(f"Joining room with channel: {channel}")

                    # Step 1: Join the room using 'channel' instead of 'channel_id'
                    join_channel_url = "https://www.clubhouseapi.com:443/api/join_channel"
                    join_channel_data = {
                        "channel": channel  # Use 'channel' here
                    }
                    join_channel_response = requests.post(join_channel_url, headers=headers, json=join_channel_data)

                    if join_channel_response.status_code == 200:
                        print(f"Successfully joined the room with channel: {channel}")

                        # Step 2: End the room after successfully joining
                        print(f"Ending room with channel: {channel}")
                        end_channel_url = "https://www.clubhouseapi.com/api/end_channel"
                        end_channel_data = {
                            "channel": channel  # Use 'channel' here
                        }
                        end_channel_response = requests.post(end_channel_url, headers=headers, json=end_channel_data)

                        if end_channel_response.status_code == 200:
                            print(f"Room with channel {channel} ended successfully.")
                        else:
                            print(f"Failed to end room with channel {channel}. Error: {end_channel_response.status_code}")
                    else:
                        print(f"Failed to join room with channel {channel}. Error: {join_channel_response.status_code}")
                    break  # Exit the bad word loop once a match is found
    else:
        print(f"Error: {response.status_code}")

# Run the script 24/7
while True:
    check_and_end_bad_rooms()
    # Sleep for a specified time interval (e.g., 60 seconds) before checking again
    time.sleep(1)
