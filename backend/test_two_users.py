import websocket
import json


conversation_uuid = "ee46ffbe-ee77-4bc7-9ec2-f9bd9c569ec0"

joyal_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg3MjMwMTQ5LCJpYXQiOjE3ODcyMjk4NDksImp0aSI6ImZiNGQ5OTVkOTE0NzRjZjFiZjY5MTlmNDY2OGI4NDE5IiwidXNlcl9pZCI6IjQifQ.TByTTpgQbJmkS2PventFon8okR9Lb-TuoDFT3gJTb64"
meghana_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg3MjMwMTA1LCJpYXQiOjE3ODcyMjk4MDUsImp0aSI6ImZiM2U3NGM1NWQ3ZjQ1ODZiNzlkZmZjMDFjNmVkMDE0IiwidXNlcl9pZCI6IjkifQ.8lHwUKIwqPEOmeWoUU8Aw_kvx89r5M7NgF9IojFy-1w"


joyal_url = (
    f"ws://127.0.0.1:8000/ws/chats/"
    f"{conversation_uuid}/"
    f"?token={joyal_token}"
)

meghana_url = (
    f"ws://127.0.0.1:8000/ws/chats/"
    f"{conversation_uuid}/"
    f"?token={meghana_token}"
)


joyal_ws = websocket.create_connection(joyal_url)

print("Joyal connected!")


meghana_ws = websocket.create_connection(meghana_url)

print("Meghana connected!")


joyal_ws.send(json.dumps({
    "content": "Hello Meghana!"
}))


message = meghana_ws.recv()

print("Meghana received:")
print(message)


joyal_ws.close()
meghana_ws.close()