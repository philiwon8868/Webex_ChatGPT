from flask import Flask, request, Response
import json
import requests
import os
import openai

app = Flask(__name__)

# token of the BOT
token = 'Bearer ' + <Bearer Token>

openai_token = <OpenAI API Token>

# Header
headers = {
  'Authorization': token,
  'Content-Type': 'application/json'
}

# Room ID of the incoming message
roomID = ""

# Person ID of the incoming message
personID = ""

@app.route('/',methods=['POST','GET'])

# Default Listener for the incoming messages
def listener():
    if request.method == 'POST':
        message_id = request.json['data']['id']
# Fetch the roomID and personID
        roomID = request.json['data']['roomId']
        personID = request.json['data']['personId']
        payload={}
        url = "https://webexapis.com/v1/messages/"+message_id
        response = requests.request("GET", url, headers=headers, data=payload)
        # extract the message content from the BOT and change it to all upper case
        message = json.loads(response.text)['text'].upper()
        if message == "HELP":
            send_message("To ask ChatGPT a question...",personID)
            send_message("==>chatgpt <your question>",personID)
            send_message("To show Nexus Dashboard Insights anomalies...", personID)
            send_message("==>anomaly", personID)
            send_message("To show Nexus Dashboard Insights advisories...", personID)
            send_message("==>advisory", personID)
            send_message("To ask ChatGPT for advice to the NDI anomalies...",personID)
            send_message("==>anomaly+chatgpt",personID)
            send_message("To ask ChatGPT for advice to the NDI advisories...",personID)
            send_message("==>advisory+chatgpt",personID)
        if len(message) > 7:
            header = message[0:7]
            body = message[7:]
            if header == 'CHATGPT':
                print ("Ask the AI engine: " + body)
                chatgpt(body,personID)
        if message[0:7] == 'ANOMALY' and message[7:17] == '+CHATGPT':
            send_message ("Checking ... ND Insights Anomalies with ChatGPT",personID)
            ndi_anomaly_chatgpt(personID)
        if message[0:7] == 'ANOMALY' and len(message) < 8:
            send_message ("Checking... Nexus Dashboard Insights Anomalies",personID)
            ndi_anomaly(personID)
        if message[0:8] == 'ADVISORY' and message[8:18] == '+CHATGPT':
            send_message ("Checking ... ND Insights Advisories with ChatGPT",personID)
            ndi_advisory_chatgpt(personID)
        if message[0:8] == 'ADVISORY' and len(message) < 9:
            send_message ("Checking ... Nexus Dashboard Insights Advisories",personID)
            ndi_advisory(personID)
        send_message("***END***",personID)
        return 'success', 200
    elif request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        if challenge == None:
            return '',200
        else:
            return challenge
    else:
        return '',200

def chatgpt(body,personID):
    url = "https://api.openai.com/v1/chat/completions"
  
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
                {
                     "role": "system",
                     "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "??"
                }
            ]
        })
    headers = {
          'Authorization': 'Bearer <OpenAI API Token>',
          'Content-Type': 'application/json'
        }
    payload = json.loads(payload)
    payload["messages"][1]["content"] = body
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response_json = json.loads(response.text)
    print("\n")
    print(response.text)
      
    choices = len(response_json["choices"])
    if choices > 0:
        i = 0
        while i < choices:
            answer = response_json["choices"][i]["message"]["content"]
            print("\n")
            print(answer)
            send_message("chat-GPT replies\n\n" + answer,personID)
            i += 1

def ndi_anomaly(personID):
    print ("\nND Insights checking ... ")
    url = "https://<IP of Nexus Dashboard Insights>/login"
    payload = json.dumps({
        "username": "admin",
        "password": "<Password>"
    })
    headers = {
        'Content-Type': 'application/json'
        }
      
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        token = json.loads(response.text)["token"]
        url = "https://<IP of Nexus Dashboard Insights>/sedgeapi/v1/cisco-nir/api/api/v1/anomalies/details"
        payload={}
        headers = {
            'Authorization': 'Bearer ' + token
            }
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        if response.status_code == 200:
            anomalies = json.loads(response.text)
#            num_of_anomalies = anomalies["totalResultsCount"]
            num_of_anomalies = len(anomalies["entries"])
            i = 0
            while i < num_of_anomalies:
                anomalyID = anomalies["entries"][i]["anomalyId"]
                category = anomalies["entries"][i]["category"]
                anomalyReason = anomalies["entries"][i]["anomalyReason"]
                cleared = anomalies["entries"][i]["cleared"]
                if cleared == False:
                    send_message(category + ": " + anomalyReason, personID)
                i = i + 1
        else:
            print(response.status_code)
    else:
        print (response.status_code)

def ndi_anomaly_chatgpt(personID):
        print ("\nND Insights checking ... ")
        url = "https://<IP of Nexus Dashboard Insights>/login"
        payload = json.dumps({
                "username": "admin",
                "password": "<Password>"
        })
        headers = {
                'Content-Type': 'application/json'
                }
        
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        
        if response.status_code == 200:
                token = json.loads(response.text)["token"]
                url = "https://<IP of Nexus Dashboard Insights>/sedgeapi/v1/cisco-nir/api/api/v1/anomalies/details"
                payload={}
                headers = {
                        'Authorization': 'Bearer ' + token
                        }
                response = requests.request("GET", url, headers=headers, data=payload, verify=False)
                if response.status_code == 200:
                        anomalies = json.loads(response.text)
                        num_of_anomalies = len(anomalies["entries"])
                        i = 0
                        while i < num_of_anomalies:
                                category = anomalies["entries"][i]["category"]
                                anomalyReason = anomalies["entries"][i]["anomalyReason"]
                                cleared = anomalies["entries"][i]["cleared"]
                                if cleared == False:
                                        chatgpt("what is the reason for this error: " + anomalyReason, personID)
                                        chatgpt("how to solve this error: " + anomalyReason, personID)
                                i = i + 1
                else:
                        print(response.status_code)
        else:
                print (response.status_code)

        

def ndi_advisory(personID):
        print ("\nND Insights checking ... ")
        url = "https://<IP of Nexus Dashboard Insights>/login"
        payload = json.dumps({
                "username": "admin",
                "password": "<Password>"
        })
        headers = {
                'Content-Type': 'application/json'
                }
                        
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
                
        if response.status_code == 200:
                token = json.loads(response.text)["token"]
                url = "https://<IP of Nexus Dashboard Insights>/sedgeapi/v1/cisco-nir/api/api/v1/advisories/details"
                payload={}
                headers = {
                        'Authorization': 'Bearer ' + token
                        }
                response = requests.request("GET", url, headers=headers, data=payload, verify=False)
                if response.status_code == 200:
                        anomalies = json.loads(response.text)
                        num_of_anomalies = len(anomalies["entries"])
                        i = 0
                        while i < num_of_anomalies:
                                category = anomalies["entries"][i]["fabricName"]
                                anomalyReason = anomalies["entries"][i]["title"]
                                cleared = anomalies["entries"][i]["cleared"]
                                if cleared == False:
                                        send_message(category + ": " + anomalyReason, personID)
                                i = i + 1
                else:
                        print(response.status_code)
        else:
                print (response.status_code)

def ndi_advisory_chatgpt(personID):
        print ("\nND Insights checking ... ")
        url = "https://<IP of Nexus Dashboard Insights>/login"
        payload = json.dumps({
                "username": "admin",
                "password": "<Password>"
        })
        headers = {
                'Content-Type': 'application/json'
                }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        if response.status_code == 200:
                token = json.loads(response.text)["token"]
                url = "https://<IP of Nexus Dashboard Insights>/sedgeapi/v1/cisco-nir/api/api/v1/advisories/details"
                payload={}
                headers = {
                        'Authorization': 'Bearer ' + token
                        }
                response = requests.request("GET", url, headers=headers, data=payload, verify=False)
                if response.status_code == 200:
                        anomalies = json.loads(response.text)
                        num_of_anomalies = len(anomalies["entries"])
                        i = 0
                        while i < num_of_anomalies:
                                category = anomalies["entries"][i]["fabricName"]
                                anomalyReason = anomalies["entries"][i]["title"]
                                cleared = anomalies["entries"][i]["cleared"]
                                if cleared == False:
                                        chatgpt("what is the reason for this error: " + anomalyReason, personID)
                                        chatgpt("how to solve this error: " + anomalyReason, personID)
                                i = i + 1
                else:
                        print(response.status_code)
        else:
                print (response.status_code)



def send_message(answer,personID):

    url = "https://webexapis.com/v1/messages"

    payload = json.dumps({
        "toPersonId" : "personid",
        "text": "testing"
        })

    headers = {
        'Authorization': 'Bearer <Bearer Token>',
        'Content-Type': 'application/json'
        }

    payload = json.loads(payload)
    payload["text"] = answer
    payload["toPersonId"] = personID
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

if __name__ == '__main__':
    app.run(port=5002)

