import webbrowser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Your API key
API_KEY = "AIzaSyA91expuv1IJ2UHEI7W-zYEw5yrgAwpypU"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Get search query
domain = input("Enter the song name: ").strip()
if not domain:
    print("No input provided.")
else:
    try:
        # Initialize the API client
        youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
        
        # Perform the search
        search_response = youtube.search().list(
            q=domain,
            part="id",
            type="video",
            maxResults=1
        ).execute()

        # Extract video ID
        items = search_response.get("items", [])
        if items:
            video_id = items[0]["id"]["videoId"]
            url = "https://www.youtube.com/watch?v=" + video_id
            print("Opening:", url)
            webbrowser.open_new(url)
        else:
            print("No results found for:", domain)

    except HttpError as e:
        print("API error:", e)
    except Exception as e:
        print("An error occurred:", e)  