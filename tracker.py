import socket
import threading

class Tracker:
    def __init__(self, port):
        self.port = port
        self.files = {}

    #Registro de seeder
    def register_seeder(self, file_name, seeder_address):
        if file_name in self.files:
            self.files[file_name].append(seeder_address)
        else:
            self.files[file_name] = [seeder_address]
        print(f"Se ha regiatrado seeder para el archivo {file_name}: {seeder_address}")

    def get_seeder(self, file_name):
        if file_name in self.files:
            seeders = self.files[file_name]
            return seeders[0]  # Retorna el primer seeder registrado para simplificar
        else:
            return None

   #Verificando que la conexion del seeder sea exitosa
    def handle_client(self, client_socket, address):
        request = client_socket.recv(1024).decode()
        request_parts = request.split()

        if request_parts[0] == "REGISTER":
            file_name = request_parts[1]
            seeder_address = (address[0], int(request_parts[2]))
            self.register_seeder(file_name, seeder_address)
            client_socket.send("Se ha registrado correctamente".encode())
        elif request_parts[0] == "GETSEEDER":
            file_name = request_parts[1]
            seeder_address = self.get_seeder(file_name)
            if seeder_address:
                client_socket.send(f"{seeder_address[0]}:{seeder_address[1]}".encode())
            else:
                client_socket.send("".encode())
        else:
            client_socket.send("Solicitud invalida".encode())
        client_socket.close()

    def start(self):
        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.bind(('localhost', self.port))
        tracker_socket.listen(5)
        print(f"Tracker iniciado en el puerto {self.port}")

        while True:
            client_socket, address = tracker_socket.accept()
            print(f"Conexion con cliente: {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    port = 5000  # Puerto del tracker
    tracker = Tracker(port)
    tracker.start()
