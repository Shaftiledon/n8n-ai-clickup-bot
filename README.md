AI-Powered ClickUp Bot (n8n Workflow)

This repository contains an n8n workflow that creates an AI-powered bot to update ClickUp tasks directly from Google Chat.

The bot listens for @mentions in Google Chat, uses the Gemini AI to understand natural language commands, and performs actions in ClickUp. This eliminates the need for team members to constantly switch contexts between chat and project management, reducing friction and speeding up project velocity.

This project was built as part of the Stears Vibe Day (a one-day automation hackathon).

Workflow Diagram

Here is a high-level overview of the n8n automation flow.

How It Works: Node by Node

This workflow is triggered when a user @mentions the bot in a Google Chat channel.

1. Trigger: Webhook

Action: Catches the incoming POST request from Google Chat.

Output: The raw JSON payload from Google Chat, including the user's message (e.g., "@bot Hey, I am all finished with 869b5xjne") and the sender's details.

2. AI: Google Gemini (Parse Intent)

Action: Takes the raw text from the user's message and feeds it to the Gemini AI.

Prompt: "You are a project management bot. Extract the task_id (e.g., '869b5xjne') and a target_status_hint (e.g., 'finished') from the user's message. Respond only with valid JSON."

Output: A clean JSON object, e.g., {"task_id": "869b5xjne", "target_status_hint": "finished"}.

3. ClickUp: HTTP Request (Get Task)

Action: Uses the task_id from the Gemini node to make a GET request to the ClickUp API (/api/v2/task/{task_id}).

Purpose:

Validates: Confirms the task actually exists. (If it doesn't, the node fails and can trigger an error-handling branch).

Gathers Data: Fetches the task's data, most importantly the list.id that the task belongs to.

4. ClickUp: HTTP Request (Get List Statuses)

Action: Uses the list.id from the previous node to make a GET request to the ClickUp API (/api/v2/list/{list_id}).

Purpose: Fetches the full array of available statuses for that specific list (e.g., [{"status": "to do"}, {"status": "in progress"}, {"status": "complete"}]).

5. AI: Google Gemini (Fuzzy Match Status)

Action: Performs the second, more advanced AI call. It takes the user's simple hint (e.g., "finished") and the full array of available statuses.

Prompt: "You are a smart project bot. Find the single best status name from the available_statuses array that matches the user's hint. Respond only with the single, lowercase status string."

Output: The single, exact status name, e.g., complete.

6. ClickUp: HTTP Request (Update ClickUp Task)

Action: This is the final step. It makes a PUT request to the ClickUp API (/api/v2/task/{task_id}).

Body: It sends a JSON payload containing the final status from the "Fuzzy Match" node: {"status": "complete"}.

Result: The task is instantly updated in ClickUp for everyone to see.

Tech Stack

Automation: n8n (Self-Hosted)

Language Model: Google Gemini (via API)

Chat Platform: Google Chat (via Webhook)

Project Management: ClickUp (via OAuth2 and HTTP Request)

How to Use

Download the clickup-bot.json file from this repository.

Import the workflow into your n8n instance.

Create a Google Gemini API credential.

Create a ClickUp OAuth2 API credential (using the generic OAuth2 API node) with the required access_type: offline parameter.





Configure a Google Chat bot to send @mentions to the n8n Webhook URL.
