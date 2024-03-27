import socket
import errno
import sys

# Definiraj glavne parametre
HEADER_LENGTH = 10
IP = socket.gethostname() # localhost
PORT = 1234

def main():
    # Stvaranje socket objekta
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    while True:
        try:
            # Primanje odgovora od poslužitelja
            command_header = client_socket.recv(HEADER_LENGTH)
            command_length = int(command_header.decode("utf-8"))
            command = client_socket.recv(command_length).decode("utf-8")

            global message, encoded_message, command_tag

            message, encoded_message, command_tag = ("", "", "")

            new_globals = {}

            exec(command, new_globals)

            globals().update(new_globals)
            
            # Slanje poruke poslužitelju
            if message:
                command_tag = command_tag.encode("utf-8")
                message_header = f"{len(encoded_message):<{HEADER_LENGTH}}".encode("utf-8")
                client_socket.sendall(command_tag + message_header + encoded_message)

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
            continue

        except Exception as e:
            print('General error', str(e))
            sys.exit()
            

if __name__ == "__main__":
    main()