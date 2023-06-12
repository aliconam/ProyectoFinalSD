# -*- coding: latin-1 -*-

import socket

class Seeder:
    
    def __init__(self, tracker_address, file_name, port):
        self.tracker_address = tracker_address
        self.file_name = file_name
        self.port = port

    #Registro en el tracker
    def register_with_tracker(self):
        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.connect(self.tracker_address)
        tracker_socket.send(f"REGISTER {self.file_name} {self.port}".encode())
        tracker_socket.close()
    
    #Envio del seeder al leecher
    def send_file(self, leecher_socket):
        with open(self.file_name, 'rb') as file:
            data = file.read(1024)
            while data:
                leecher_socket.send(data)
                data = file.read(1024)


    #Iniciamos el seeder y lo conectamos al tracker por medio del puerto 5000
    def start(self):
        self.register_with_tracker()

        seeder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        seeder_socket.bind(('localhost', self.port))
        seeder_socket.listen(1)
        print(f"El seeder se ha concectado al puerto {self.port}")

        #Verificamos que haya un leecher al cual enviar el archivo
        while True:
            leecher_socket, address = seeder_socket.accept()
            print(f"Leecher conectado: {address}")
            self.send_file(leecher_socket)
            leecher_socket.close()

if __name__ == "__main__":
    tracker_address = ('localhost', 5000)  # Direccion del tracker
    file_name = 'archivo1.jpg'  # El archivo a enviar
    port = 6000  # Puerto de comunicacion con el leecher
    seeder = Seeder(tracker_address, file_name, port)
    seeder.start()
