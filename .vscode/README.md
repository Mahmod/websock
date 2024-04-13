# Simple Chat Application

This repository contains the source code for a simple chat application implemented in both Python and C++. It includes a WebSocket server written in each language and a single web-based client that can connect to either server.

## Directory Structure

```plaintext
/
├── python/
│   └── server.py          # Python WebSocket server
├── cpp/
│   ├── chat_server.cpp    # C++ WebSocket server
│   └── include/           # Include directory for external headers
│       └── nlohmann/      # JSON library for C++
└── client/
    └── index.html         # Web client for the chat application
```

## Prerequisites

### For Python Server
- Python 3.x
- `websockets` library

### For C++ Server
- C++11 compiler (e.g., g++)
- Boost Libraries
- WebSocket++ library
- nlohmann/json library

## Installation

### Python Server

1. **Install Python 3.x** (if not installed): [Python Installation Guide](https://www.python.org/downloads/)
2. **Install Dependencies**:
   ```bash
   pip install websockets
   ```

### C++ Server

1. **Install C++ Build Tools**: Ensure `g++` and `CMake` are installed.
2. **Install Boost Libraries**:
   ```bash
   sudo apt-get install libboost-all-dev
   ```
3. **Install WebSocket++**:
   ```bash
   git clone https://github.com/zaphoyd/websocketpp.git
   ```
4. **Install nlohmann/json**:
   ```bash
   sudo apt-get install nlohmann-json3-dev
   ```

## Building and Running the Servers

### Python Server

To run the Python server, navigate to the `python` directory and execute the following command:

```bash
python server.py
```

This will start the WebSocket server on `localhost:8765`.

### C++ Server

To build and run the C++ server, navigate to the `cpp` directory and execute the following commands:

1. **Compile the Server**:
   ```bash
   g++ -std=c++11 chat_server.cpp -o chat_server -I ./websocketpp -I ./include -lboost_system -lpthread
   ```
2. **Run the Server**:
   ```bash
   ./chat_server
   ```

This will compile and start the WebSocket server on `localhost:8765`.

## Using the Client

Open the `client/index.html` file in any modern web browser to connect to the running WebSocket server. Ensure that either the Python or C++ server is running before opening the client.

1. **Enter a username** in the provided input field.
2. **Type a message** and click `Send` to broadcast it to all connected clients.
3. Received messages from other clients will be displayed in real time.

## Notes

- The C++ server requires proper setup of WebSocket++ and Boost, including ensuring that paths in the compilation command are correct.
- Both servers listen on the same port (`8765`), so ensure that only one server is running at a time when using the client.

---