from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import Mount
import os
import socket


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
def generate_User():
    try:
        Mounted_Drives=Mount.get_mounted_drives()
        Users=[]
        for i in range(len(Mounted_Drives)):
            Users.append({"usr":f"User{i}","Password":"12345","Drive":Mounted_Drives[i]})
        return Users
    except Exception as e:
        print(str(e))

def setUser(UsersDict):
    for User in Users_Dict:
        if os.path.exists(User["Drive"]) :
                authorizer.add_user(username=User["usr"], password=User["Password"], homedir=User["Drive"],perm='elradfmwM')
                print(f'credential for Directory {User["Drive"]} \n \t Username: {User["usr"]} and Password: {User["Password"]}')
                print("-------------------------------------------")
        else:
                print(f'Directory {User["Drive"]} does not exist')

Users_Dict=generate_User()
local_ip=get_local_ip()
port=3000
authorizer = DummyAuthorizer()


setUser(Users_Dict)

#authorizer.add_anonymous("d:\\")

handler = FTPHandler
handler.authorizer = authorizer
handler.passive_ports=range(60001, 60101)
server = FTPServer((local_ip, port), handler)

print(f"Server : ftp://{local_ip}:{port}")


server.serve_forever()
   