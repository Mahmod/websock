#include <websocketpp/config/asio_no_tls.hpp>
#include <websocketpp/server.hpp>

#include <functional> // Ensure this header is included for std::bind and std::placeholders
#include <iostream>
#include <set>
#include <nlohmann/json.hpp>  // Include this for JSON handling

typedef websocketpp::server<websocketpp::config::asio> server;

// Create a server endpoint
server print_server;

// Define a set to hold connections
std::set<websocketpp::connection_hdl, std::owner_less<websocketpp::connection_hdl>> connections;

void on_message(websocketpp::connection_hdl hdl, server::message_ptr msg) {
    // Parse message as JSON
    auto json_msg = nlohmann::json::parse(msg->get_payload());
    std::string username = json_msg["username"];
    std::string message = json_msg["message"];
    std::cout << "Received message: " << message << " from " << username << std::endl;

    // Broadcast message
    for (auto it : connections) {
        if (it.lock() != hdl.lock()) {  // Don't send the message back to the sender
            print_server.send(it, msg->get_payload(), msg->get_opcode());
        }
    }
}

void on_open(websocketpp::connection_hdl hdl) {
    std::cout << "New connection established" << std::endl;
    connections.insert(hdl);
}

void on_close(websocketpp::connection_hdl hdl) {
    std::cout << "Connection closed" << std::endl;
    connections.erase(hdl);
}

int main() {
    // Set logging settings
    print_server.set_access_channels(websocketpp::log::alevel::all);
    print_server.clear_access_channels(websocketpp::log::alevel::frame_payload);

    // Initialize ASIO
    print_server.init_asio();

    // Correct the namespace for placeholders in the bind function
    print_server.set_message_handler(std::bind(&on_message, std::placeholders::_1, std::placeholders::_2));
    print_server.set_open_handler(std::bind(&on_open, std::placeholders::_1));
    print_server.set_close_handler(std::bind(&on_close, std::placeholders::_1));

    // Listen on port 8765
    print_server.listen(8765);

    // Start the server accept loop
    print_server.start_accept();

    // Start the ASIO io_service run loop
    try {
        print_server.run();
    } catch (const std::exception & e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }
}
