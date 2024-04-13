import asyncio
import websockets
import json

clients = {}  # Dictionary to track connections
rooms = {}  # Dictionary to manage rooms and their members

async def register_client(websocket, path):
    # Wait for the client to send their username and desired room
    try:
        async for message in websocket:
            data = json.loads(message)
            username = data['username']
            room = data['room']
            clients[websocket] = {'username': username, 'room': room}

            # Add client to the specified room
            if room in rooms:
                rooms[room].add(websocket)
            else:
                rooms[room] = {websocket}

            # Notify room of new user
            await broadcast(room, f"{username} has joined the chat!")

            # Handle subsequent messages
            await handle_messages(websocket, room)
    finally:
        # Cleanup on disconnect
        await unregister_client(websocket)

async def handle_messages(websocket, room):
    async for message in websocket:
        data = json.loads(message)
        await broadcast(room, f"{clients[websocket]['username']}: {data['message']}")

async def broadcast(room, message):
    for client in rooms[room]:
        await client.send(message)

async def unregister_client(websocket):
    room = clients[websocket]['room']
    username = clients[websocket]['username']
    rooms[room].remove(websocket)
    if not rooms[room]:  # Delete room if empty
        del rooms[room]
    del clients[websocket]
    await broadcast(room, f"{username} has left the chat.")

###start_server = websockets.serve(register_client, "localhost", 8765)

async def main():
    async with websockets.serve(register_client, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
