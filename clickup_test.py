import requests
import json

# --- Configuration ---
# ❗️ Paste your ClickUp API token here
CLICKUP_API_TOKEN = "pk_81887607_JZUD8R77CLCGZN7RXAG3D03RHS1A5GCH"

# ❗️ Change this to a real Task ID from your ClickUp workspace (e.g., "abc-123")
TEST_TASK_ID = "869b4g4c7"
# --- End Configuration ---

def get_task_details(token, task_id):
    """
    Fetches the details for a specific ClickUp task.
    """
    # This is the standard ClickUp API v2 endpoint for tasks
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    
    # We must provide the API token in the 'Authorization' header
    headers = {
        "Authorization": token
    }
    
    print(f"Attempting to fetch task: {task_id}...")
    
    try:
        # Make the GET request to the ClickUp API
        response = requests.get(url, headers=headers)
        
        # This will raise an error if the HTTP request failed (e.g., 404, 500)
        response.raise_for_status()
        
        # If we get here, the request was successful (200 OK)
        task_data = response.json()
        
        print("\n--- ✅ SUCCESS! ---")
        print(f"Task Name: {task_data.get('name')}")
        print(f"Task Status: {task_data.get('status', {}).get('status')}")
        print(f"Task URL: {task_data.get('url')}")
        
        # Uncomment this line if you want to see all the data
        # print(json.dumps(task_data, indent=2))
        
    except requests.exceptions.HTTPError as http_err:
        print(f"\n--- ❌ HTTP Error ---")
        if response.status_code == 401:
            print("Error: 401 Unauthorized. Is your API token correct?")
        elif response.status_code == 404:
            print(f"Error: 404 Not Found. Does Task ID '{task_id}' exist?")
        else:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response: {response.text}")
            
    except Exception as err:
        print(f"\n--- ❌ An other error occurred ---")
        print(str(err))

# --- Run the test ---
if __name__ == "__main__":
    if CLICKUP_API_TOKEN == "YOUR_API_TOKEN_HERE" or TEST_TASK_ID == "YOUR_TASK_ID_HERE":
        print("Error: Please update 'CLICKUP_API_TOKEN' and 'TEST_TASK_ID' at the top of the file.")
    else:
        get_task_details(CLICKUP_API_TOKEN, TEST_TASK_ID)
