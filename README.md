Toxy by incrediBit

Toxy is a simple and powerful Python script designed to automate the installation and configuration of Tor and ProxyChains on Debian-based Linux systems. This tool streamlines the process of setting up a transparent proxy for anonymizing your network traffic, making it easy to run applications securely through the Tor network.
✨ Features

    Automated Cleanup: The script intelligently removes any previous Tor installations and configurations to ensure a clean setup.

    Official Tor Repository: It adds the official Tor Project repository to your system, guaranteeing you have the latest and most secure version of Tor.

    Seamless Integration: It automatically configures ProxyChains to use Tor's SOCKS5 proxy, removing the need for manual configuration.

    Clear Instructions: After installation, the script provides a detailed guide on how to manage the Tor service and how to use ProxyChains to route your applications.

💻 How to Run Toxy

Prerequisites: This script is designed for Debian-based Linux distributions (like Kali, Ubuntu, etc.). It must be run with administrative (root) privileges.

    Save the script: Save the script to a file named toxy.py on your machine.

    Make it executable: In your terminal, navigate to the directory where you saved the file and run the following command:

    chmod +x toxy.py

    Run the script with sudo:

    sudo ./toxy.py

The script will prompt you to press Enter to begin the installation and configuration process.
🚀 Usage after Installation

Once Toxy has finished, you can manage the Tor service and run applications through the network using these simple commands.
Managing the Tor Service

Use systemctl to control the Tor service.

    Start Tor: sudo systemctl start tor

    Stop Tor: sudo systemctl stop tor

    Restart Tor (to get a new IP): sudo systemctl restart tor

    Check Status: sudo systemctl status tor

Running Applications with ProxyChains

To route any application's traffic through Tor, simply prepend the command with proxychains4.

    Run Firefox through Tor: proxychains4 firefox-esr

    Check your public IP address: proxychains4 curl ipinfo.io

🤝 Contributing

Feel free to open an issue or submit a pull request if you have any suggestions or improvements.
