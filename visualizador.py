import tkinter as tk
from tkinter import messagebox, simpledialog
import socket
import threading
 
# ─────────────────────────────────────────────
# Configuración de conexión
# ─────────────────────────────────────────────
HOST = "127.0.0.1"
PORT = 5000

# ─────────────────────────────────────────────
# Comunicación con el servidor C++
# ─────────────────────────────────────────────
class ClienteSocket:
    def __init__(self):
        self.sock = None
        self.conectado = False
 
    def conectar(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.conectado = True
            return True
        except Exception as e:
            self.conectado = False
            return False
 
    def enviar(self, mensaje):
        try:
            self.sock.sendall((mensaje + "\n").encode())
            respuesta = ""
            while True:
                parte = self.sock.recv(4096).decode()
                respuesta += parte
                # El servidor termina sus respuestas con \n
                if respuesta.endswith("\n"):
                    break
            return respuesta.strip()
        except Exception as e:
            self.conectado = False
            return "ERROR|CONEXION_PERDIDA"
 
    def desconectar(self):
        if self.sock:
            self.sock.close()
 
 
