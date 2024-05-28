from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import Mount
import os
import socket
import threading

# copied from the internet. This function helps to find the IP address assigned by the router.
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# This function will generate a User as dictionary format for FTP credentials.
def generate_User():
    try:
        Mounted_Drives = Mount.get_mounted_drives()
        Users = []
        for i in range(len(Mounted_Drives)):
            Users.append({"usr": f"User{i}", "Password": "12345", "Drive": Mounted_Drives[i]})
        return Users
    except Exception as e:
        print(str(e))

# This function will ensure the path exists or not and add the user to the authorizer of the FTP library.
def setUser(UsersDict):
    for User in UsersDict:
        if os.path.exists(User["Drive"]):
            authorizer.add_user(username=User["usr"], password=User["Password"], homedir=User["Drive"], perm='elradfmwM')
            print(f'Credentials for Directory {User["Drive"]} \n\t Username: {User["usr"]} and Password: {User["Password"]}')
            print("-------------------------------------------")
        else:
            print(f'Directory {User["Drive"]} does not exist')

Users_Dict = generate_User()
local_ip = get_local_ip()
port = 3000
authorizer = DummyAuthorizer()

setUser(Users_Dict)

# Configure FTP handler with existing data.
handler = FTPHandler
handler.authorizer = authorizer
handler.passive_ports = range(60001, 60101)
server = FTPServer((local_ip, port), handler)

print(f"Server: ftp://{local_ip}:{port}")

# Function to stop the server
def stop_server():
    print("Shutting down the server...")
    server.close_all()

# Thread to handle stopping the server with 's' key press
def monitor_keyboard():
    while True:
        key = input()
        if key == 's':
            stop_server()
            break

# Start the keyboard monitoring thread
keyboard_thread = threading.Thread(target=monitor_keyboard)
keyboard_thread.start()

# Start the FTP server in the main thread
server.serve_forever()

# Wait for the keyboard thread to complete
keyboard_thread.join()
