# Webex_ChatGPT
 Webex Teamspace as the UI for ChatGPT. This program simply illustrates how to integrate Webex teamspace with ChatGPT and Nexus Dashboard Insights API. Whenever the user type in a message into the teamspace, it will trigger a Webex Webhook to execute. The Webhook will retrieve the message  from the room and interprete it. Several operations are defined as below:

 1. "HELP" - print out the functions supported by the webhook
 2. "ChatGPT" - followed by a question; the webhook will call the ChatGPT on behalf of the user via the OpenAI ChatGPT API and send the result back to the teamspace.
 3. "Anomaly" or "Advisory" - use Nexus Dashboard Insights API to retrieve any anomlies or advisories from the designated Nexus Dashboard Insights.
 4. "Anomaly+ChatGPT" or "Advisory+ChatGPT" - on top of action 3, the webook will call ChatGPT for the reason and resoluton of the anomalies or advisories.

    Below is the logic flow diagram:

    ![image](https://github.com/philiwon8868/Webex_ChatGPT/assets/8743281/681192be-158f-43bc-b3ca-99c8807df99e)


## Installation
1. Modify the webhook.py with the corresponding roomID, the IP address of your Nexus Dashboard Insights, the bearer tokens for Webex and OpenAI API and the credentials.
2. Deploy your webhook in an environment so that it can be assessed by a URL.
3. Register the webhook URL to webex teamspace.

## Usage
1. Call ChatGPT from Webex Team Space, simply type "ChatGPT " followed by the question to be asked:
![image](https://github.com/philiwon8868/Webex_ChatGPT/assets/8743281/04fe2eeb-1cfa-4b46-a7ff-2f5b46d301f6)

2. On the webex team space UI, type "Advisory" to tell the webhook to retrieve advisories from the designated Nexus Dashboard Insights:
![image](https://github.com/philiwon8868/Webex_ChatGPT/assets/8743281/a48a3b64-6202-44f5-afb7-418cc96b626d)

3. To feed the Nexus Dashboard Insights' Advisories into chatGPT, simply type "Advisory+ChatGPT":
![image](https://github.com/philiwon8868/Webex_ChatGPT/assets/8743281/b04178f0-5f7e-4952-a849-8eaea287acc7)

## Known Issues
The question to be submitted to ChatGPT cannot include attachments.





