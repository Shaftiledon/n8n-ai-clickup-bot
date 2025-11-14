import requests
import json
import time

# --- Configuration ---
# ❗️ Paste your ClickUp API token here
CLICKUP_API_TOKEN = "pk_81887607_JZUD8R77CLCGZN7RXAG3D03RHS1A5GCH" 

# ❗️ Use the same Task ID from before (e.g., "869b4g4c7")
TEST_TASK_ID = "869b4g4c7"

# ❗️ IMPORTANT: Set this to a valid status *name* from your board.
# (e.g., "Done", "to do", "complete", "in review")
# This must be an *exact* string match (it's not case-sensitive).
NEW_STATUS = "In Review" 
# --- End Configuration ---


def get_task_details(token, task_id):
    """
    Fetches the details for a specific ClickUp task.
    """
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {"Authorization": token}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        task_data = response.json()
        return task_data.get('status', {}).get('status')
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching: {http_err}")
    except Exception as err:
        print(f"An error occurred while fetching: {str(err)}")
    return None

def update_task_status(token, task_id, new_status):
    """
    Updates the status of a specific ClickUp task.
    """
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    
    # We send the new status in a JSON payload
    payload = {
        "status": new_status
    }
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    print(f"\nAttempting to update status to '{new_status}'...")
    
    try:
        # Make the PUT request to the ClickUp API
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        
        # Check for errors
        response.raise_for_status()
        
        # If we get here, the update was successful
        print("--- ✅ SUCCESS! ---")
        print("Status update successful.")
        
    except requests.exceptions.HTTPError as http_err:
        print(f"\n--- ❌ HTTP Error ---")
        if response.status_code == 400:
            print(f"Error: 400 Bad Request. Is '{new_status}' a valid status for this task?")
            print(f"Response: {response.text}")
        elif response.status_code == 401:
            print("Error: 401 Unauthorized. Is your API token correct?")
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
        # 1. Show the "Before" status
        print("--- Fetching BEFORE status ---")
        before_status = get_task_details(CLICKUP_API_TOKEN, TEST_TASK_ID)
        if before_status:
            print(f"Current status is: '{before_status}'")
        
        # 2. Perform the update
        update_task_status(CLICKUP_API_TOKEN, TEST_TASK_ID, NEW_STATUS)
        
        # Wait a moment for ClickUp's API to process
        time.sleep(1) 
        
        # 3. Show the "After" status
        print("\n--- Fetching AFTER status ---")
        after_status = get_task_details(CLICKUP_API_TOKEN, TEST_TASK_ID)
        if after_status:
            print(f"New status is: '{after_status}'")
            
        if after_status and after_status.lower() == NEW_STATUS.lower():
            print("\n🎉 Test Passed! Status was updated successfully.")
        else:
            print("\n🚨 Test Failed! Status was not updated.")
