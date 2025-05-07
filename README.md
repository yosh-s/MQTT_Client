# MQTT Client GUI

A modern, user-friendly MQTT client application built with Python, Tkinter, and Paho MQTT. This application allows users to connect to an MQTT broker, subscribe to topics, publish messages, and view real-time message logs with a sleek, dark-themed graphical interface.

![MQTT Client GUI Screenshot](https://github.com/yosh-s/MQTT_Client/blob/main/asset/screenshot.png)

## Features

- **Connect to MQTT Brokers**: Easily connect to any MQTT broker with configurable broker address, port, and topic.
- **Subscribe and Publish**: Subscribe to MQTT topics to receive messages and publish messages to specified topics.
- **Real-Time Logging**: View timestamped logs of connection status, incoming messages, and published messages.
- **Dark Theme UI**: Modern, visually appealing interface with a dark theme and customizable colors.
- **Thread-Safe MQTT Handling**: Uses threading to ensure smooth operation without freezing the GUI.
- **Error Handling**: Robust error handling for connection issues, invalid inputs, and unexpected disconnections.
- **Cross-Platform**: Runs on Windows, macOS, and Linux with Python installed.

## Installation

### Prerequisites
- Python 3.6 or higher
- Required Python packages:
  - `paho-mqtt`
  - `tkinter` (usually included with Python; install `python3-tk` on Linux if needed)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yosh-s/MQTT_Client.git
   cd MQTT_Client
   ```

2. Install dependencies:
   ```bash
   pip install paho-mqtt
   ```

3. Run the application:
   ```bash
   python MQTT_Client.py
   ```
### Windows Executable
For Windows users, you can download the standalone executable:
<p align="left">
  <a href="https://github.com/yosh-s/MQTT_Client/raw/refs/heads/main/MQTT_Client.exe">
    <img src="https://github.com/yosh-s/MQTT_Client/blob/main/asset/download.png" alt="Download MQTT_Client.exe" width="160"/>
  </a>
</p>



  
## Usage

1. **Launch the Application**:
   - Run the script to open the GUI.

2. **Configure Connection**:
   - Enter the MQTT broker address (e.g., `test.mosquitto.org`).
   - Specify the port (default: `1883`).
   - Enter a topic to subscribe to (e.g., `temp`).
   - Click **Connect** to establish a connection.

3. **Publish Messages**:
   - Enter a topic and message in the "Publish Message" section.
   - Click **Publish** to send the message.

4. **View Logs**:
   - The "Message Log" displays timestamped events, including connections, disconnections, and messages.

5. **Disconnect**:
   - Click **Disconnect** to close the MQTT connection.

## Configuration

The application uses the following default settings:
- **Broker**: `test.mosquitto.org`
- **Port**: `1883`
- **Topic**: `temp`

These can be modified in the GUI or by editing the `DEFAULT_BROKER`, `DEFAULT_PORT`, and `DEFAULT_TOPIC` variables in the source code.


## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure your code follows PEP 8 guidelines and includes appropriate comments.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Paho MQTT](https://www.eclipse.org/paho/) for the MQTT client library.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework.
- Inspired by the need for a simple, modern MQTT client GUI.

## Contact

For questions or feedback, open an issue on GitHub or contact [yosh-s](https://github.com/yosh-s).

---

Happy MQTT messaging! 🚀
