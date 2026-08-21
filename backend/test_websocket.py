import websocket
import json


conversation_uuid = "2bcdfe10-ba6a-460f-ae7d-2fed2065c901"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg3MTk4MTUxLCJpYXQiOjE3ODcxOTc4NTEsImp0aSI6IjYxZjljOTA5NjczMTRlY2RiMThjMWFlN2YyNGU1NWJhIiwidXNlcl9pZCI6IjQifQ.beodOBQqP7VA7XYbE-9_Gfi3crRF7PMtm2tzrGE-1x8"


url = (
    f"ws://127.0.0.1:8000/ws/chats/"
    f"{conversation_uuid}/"
    f"?token={access_token}"
)


ws = websocket.create_connection(url)

print("WebSocket connected!")

ws.send(json.dumps({
    "content": "Hello from WebSocket!"
}))

response = ws.recv()

print("Server response:")
print(response)

ws.close()