import asyncio
import websockets
import json

connected = set()

async def chat_server(websocket, path):
    # Register websocket connection
    connected.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Received message: {data['message']} from {data['username']}")
            # Broadcast message to all connected websockets
            for conn in connected:
                if conn != websocket:
                    await conn.send(json.dumps(data))
    finally:
        # Unregister websocket connection
        connected.remove(websocket)

async def main():
    async with websockets.serve(chat_server, "localhost", 8765):
        print("Chat server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
