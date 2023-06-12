# -*- coding: latin-1 -*-

import socket
import hashlib

class Leecher:
    def __init__(self, tracker_address, tracker_port):
        self.tracker_address = tracker_address
        self.tracker_port = tracker_port

    #Conexion con el tracker
    def connect_to_tracker(self):
        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.connect((self.tracker_address, self.tracker_port))
        return tracker_socket
    
    #Obteniendo el archivo del seeder
    def request_file(self, file_name):
        tracker_socket = self.connect_to_tracker()
        tracker_socket.send(f"GETSEEDER {file_name}".encode())
        seeder_address = tracker_socket.recv(1024).decode()
        tracker_socket.close()

        if seeder_address:
            self.download_file(file_name, seeder_address)
        else:
            print(f"No se encontro seeder para el archivo: {file_name}")

    #Se descarga el archivo y verificamos que el archivo sea el mismo que el original 
    def download_file(self, file_name, seeder_address):
        seeder_address_parts = seeder_address.split(":")
        seeder_ip = seeder_address_parts[0]
        seeder_port = int(seeder_address_parts[1])

        file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_socket.connect((seeder_ip, seeder_port))

        with open(file_name, 'wb') as file:
            while True:
                data = file_socket.recv(1024)
                if not data:
                    break
                file.write(data)

        file_socket.close()
        print(f"Archivo descargado: {file_name}")

        self.verify_file(file_name)

    def verify_file(self, file_name):
        leecher_hash = hashlib.sha256()
        with open(file_name, 'rb') as leecher_file:
            data = leecher_file.read(1024)
            while data:
                leecher_hash.update(data)
                data = leecher_file.read(1024)

        seeder_hash = hashlib.sha256()
        with open(file_name, 'rb') as seeder_file:
            data = seeder_file.read(1024)
            while data:
                seeder_hash.update(data)
                data = seeder_file.read(1024)

        if leecher_hash.hexdigest() == seeder_hash.hexdigest():
            print("El archivo se descargo y verifico correctamente.")
        else:
            print("La verificacion del archivo ha fallado.")

    def start(self):
        file_name = "archivo1.jpg"  # Nombre del archivo a descargar
        self.request_file(file_name)

if __name__ == "__main__":
    tracker_address = "localhost"
    tracker_port = 5000
    leecher = Leecher(tracker_address, tracker_port)
    leecher.start()

