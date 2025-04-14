import json
import socket
import threading
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Starts a UDP server for Django."

    def handle(self, *args, **kwargs):
        UDP_IP = "0.0.0.0"  # Listen on all available interfaces
        UDP_PORT = 5005      # Change this as needed

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        
        self.stdout.write(self.style.SUCCESS(f"UDP Server listening on {UDP_IP}:{UDP_PORT}"))

        CompleteData = ''
        while True:
            data, addr = sock.recvfrom(1024)  # Receive up to 1024 bytes
            CompleteData += data.decode()


            dataInJson = json.loads('"'+CompleteData+'"')
            self.stdout.write(f"Received from {addr}: {dataInJson}")  # Print received message
