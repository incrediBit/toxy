#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import tempfile
import time

# --- Helper function to run shell commands ---
def run_cmd(command, check=True):
    """
    Runs a shell command, prints it, and checks for errors.
    If 'check' is True and the command fails, the script will exit.
    """
    print(f"\n-> Running: {command}")
    result = subprocess.run(command, shell=True, check=False)
    if check and result.returncode != 0:
        print(f"[ERROR] Command failed with exit code {result.returncode}: {command}")
        sys.exit(1)
    return result

# --- Step 1: Cleanup any existing Tor or Tor Browser installations ---
def cleanup_existing_install():
    """
    Removes any previously installed Tor packages and repository files
    to ensure a clean installation.
    """
    print("\n[Step 1] Cleaning up old Tor and Tor Browser installations...")
    # Remove Tor and torbrowser-launcher packages
    run_cmd("apt purge -y tor torbrowser-launcher", check=False)

    # Remove the Tor Project apt source list file
    tor_list_file = "/etc/apt/sources.list.d/torproject.list"
    if os.path.exists(tor_list_file):
        print(f"Removing old repository file: {tor_list_file}")
        os.remove(tor_list_file)

    # Remove the GPG key
    gpg_key_file = "/usr/share/keyrings/tor-archive-keyring.gpg"
    if os.path.exists(gpg_key_file):
        print(f"Removing old GPG key: {gpg_key_file}")
        os.remove(gpg_key_file)

    # Clean up any leftover dependencies
    run_cmd("apt autoremove -y")
    run_cmd("apt update")
    print("Cleanup complete.")

# --- Step 2: Install Tor and ProxyChains ---
def install_tor_and_proxychains():
    """
    Adds the Tor Project repository and installs both Tor and ProxyChains.
    """
    print("\n[Step 2] Installing Tor and ProxyChains...")

    print("-> Downloading and adding Tor GPG key...")
    # The command to get the key and dearmor it
    key_cmd = (
        "wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | "
        "gpg --dearmor | tee /usr/share/keyrings/tor-archive-keyring.gpg >/dev/null"
    )
    run_cmd(key_cmd)
    run_cmd("chmod 644 /usr/share/keyrings/tor-archive-keyring.gpg")

    print("-> Adding Tor repository for Debian 12 (bookworm)...")
    repo_line = "deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bookworm main"
    with open("/etc/apt/sources.list.d/torproject.list", "w") as f:
        f.write(repo_line + "\n")

    print("-> Updating package list and installing Tor and ProxyChains...")
    run_cmd("apt update")
    # We remove firefox-esr from this line since we're no longer running it
    run_cmd("apt install -y tor proxychains4")

    print("Tor and ProxyChains installation complete.")

# --- Step 3: Configure ProxyChains to use Tor's SOCKS5 proxy ---
def configure_proxychains():
    """
    Edits the proxychains.conf file to ensure it points to Tor's SOCKS5 proxy.
    It first backs up the original file and then modifies the new one.
    """
    print("\n[Step 3] Configuring ProxyChains...")
    config_file = "/etc/proxychains4.conf"
    if not os.path.exists(config_file):
        print(f"[ERROR] ProxyChains configuration file not found at {config_file}")
        sys.exit(1)

    backup_file = f"{config_file}.bak"
    print(f"-> Backing up original config to {backup_file}")
    shutil.copyfile(config_file, backup_file)

    with open(config_file, "r") as f:
        lines = f.readlines()

    with open(config_file, "w") as f:
        found_proxy_list = False
        for line in lines:
            # Comment out all other proxy definitions
            if line.strip().startswith("socks") or line.strip().startswith("http"):
                f.write(f"# {line}")
            # Add our Tor SOCKS5 proxy to the end
            elif "[ProxyList]" in line:
                f.write(line)
                found_proxy_list = True
            else:
                f.write(line)

        # If the [ProxyList] section was found, add our entry
        if found_proxy_list:
            print("-> Adding Tor SOCKS5 proxy to the configuration.")
            f.write("socks5 127.0.0.1 9050\n")
        else:
            print("[WARNING] Could not find '[ProxyList]' section in config file. Adding to the end.")
            f.write("\n[ProxyList]\n")
            f.write("socks5 127.0.0.1 9050\n")

    print("ProxyChains configuration complete.")

# --- Step 4: Start Tor and provide final instructions ---
def start_tor_and_provide_instructions():
    """
    Starts and enables the Tor system service and then prints final instructions
    for the user instead of launching a browser.
    """
    print("\n[Step 4] Starting Tor service and finalizing setup...")
    run_cmd("systemctl enable --now tor")

    print("-> Waiting 10 seconds for Tor to connect to the network...")
    # It's a good idea to wait a bit for Tor to connect
    time.sleep(10)
    print("\n✅ All done! Tor and ProxyChains are installed and ready to use.")

    print("""
### How to Manage Tor Services
You can control the Tor service using 'systemctl'. These commands require administrative privileges.

- **Start Tor:**
  sudo systemctl start tor
- **Stop Tor:**
  sudo systemctl stop tor
- **Restart Tor (to get a new IP):**
  sudo systemctl restart tor
- **Check Tor's status:**
  sudo systemctl status tor

### How to Run Applications with ProxyChains
To run an application through the Tor network, simply use `proxychains` before the command.

- **Example: Run Firefox through Tor**
  proxychains firefox-esr
- **Example: Check your IP address**
  proxychains curl ipinfo.io
    """)

# --- Main execution block ---
def main():
    """
    Main function to run the entire installation and execution process.
    """
    print("=== Toxy by incrediBit ===")

    # New section to outline the steps
    print("\nThis script will perform the following steps:")
    print("1. Clean up any existing Tor installations to ensure a fresh start.")
    print("2. Install the latest Tor and ProxyChains packages.")
    print("3. Configure ProxyChains to route traffic through the Tor network.")
    print("4. Start and enable the Tor service, and provide usage instructions.")

    # Prompt the user to continue
    print("\nPress Enter to begin the process...")
    input()

    # Check if running as root
    if os.geteuid() != 0:
        print("[ERROR] This script must be run as root. Please use 'sudo'.")
        sys.exit(1)

    cleanup_existing_install()
    install_tor_and_proxychains()
    configure_proxychains()
    start_tor_and_provide_instructions()

    print("\nScript finished.")
    print("Thanks for using Toxy!")
    print("@incrediBit")


if __name__ == "__main__":
    main()
