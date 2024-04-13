import asyncio
import websockets
import json

clients = {}  # Maps connections to user details
rooms = {}  # Maps room names to members and messages

async def register_client(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
            username = data['username']
            room = data['room']
            clients[websocket] = {'username': username, 'room': room}

            # Initialize room if new, otherwise add client to room
            if room not in rooms:
                rooms[room] = {'members': set(), 'messages': []}
            rooms[room]['members'].add(websocket)

            # Send existing messages in the room to the new user
            for msg in rooms[room]['messages']:
                await websocket.send(msg)

            # Notify room of new user
            join_message = f"{username} has joined the chat!"
            await broadcast(room, join_message)

            # Handle subsequent messages
            await handle_messages(websocket, room)
    finally:
        # Cleanup on disconnect
        await unregister_client(websocket)

async def handle_messages(websocket, room):
    async for message in websocket:
        data = json.loads(message)
        formatted_message = f"{clients[websocket]['username']}: {data['message']}"
        # Save message to room history
        rooms[room]['messages'].append(formatted_message)
        await broadcast(room, formatted_message)

async def broadcast(room, message):
    for client in rooms[room]['members']:
        await client.send(message)

async def unregister_client(websocket):
    room = clients[websocket]['room']
    username = clients[websocket]['username']
    rooms[room]['members'].remove(websocket)
    if not rooms[room]['members']:  # Optionally clear history when room is empty
        del rooms[room]
    else:
        leave_message = f"{username} has left the chat."
        await broadcast(room, leave_message)
    del clients[websocket]

###start_server = websockets.serve(register_client, "localhost", 8765)

async def main():
    async with websockets.serve(register_client, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
