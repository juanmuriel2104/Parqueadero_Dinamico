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
# ─────────────────────────────────────────────
# Ventana principal
# ─────────────────────────────────────────────
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Parqueadero")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
 
        self.cliente = ClienteSocket()
        self.celdas_widgets = []  # botones de cada celda
        self.estado_celdas = {}   # id -> {"ocupada": bool, "placa": str, "hora": str}
 
        self._construir_ui()
        self._conectar()
 
    # ── UI ────────────────────────────────────
    def _construir_ui(self):
        # Título
        tk.Label(
            self.root, text="🅿 Sistema de Parqueadero",
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        ).pack(pady=(20, 5))
 
        # Estado de conexión
        self.lbl_conexion = tk.Label(
            self.root, text="⚪ Conectando...",
            font=("Helvetica", 10),
            bg="#1e1e2e", fg="#a6adc8"
        )
        self.lbl_conexion.pack(pady=(0, 15))
 
        # Grilla de celdas (2 filas x 5 columnas)
        frame_grilla = tk.Frame(self.root, bg="#1e1e2e")
        frame_grilla.pack(padx=20, pady=10)
 
        for i in range(10):
            fila = i // 5
            col  = i % 5
 
            frame_celda = tk.Frame(
                frame_grilla,
                bg="#313244",
                bd=0,
                relief="flat",
                width=140,
                height=100
            )
            frame_celda.grid(row=fila, column=col, padx=6, pady=6)
            frame_celda.pack_propagate(False)
 
            lbl_num = tk.Label(
                frame_celda,
                text=f"Celda {i}",
                font=("Helvetica", 9, "bold"),
                bg="#313244", fg="#a6adc8"
            )
            lbl_num.pack(pady=(8, 0))
 
            lbl_estado = tk.Label(
                frame_celda,
                text="LIBRE",
                font=("Helvetica", 11, "bold"),
                bg="#313244", fg="#a6e3a1"
            )
            lbl_estado.pack()
 
            lbl_placa = tk.Label(
                frame_celda,
                text="",
                font=("Helvetica", 9),
                bg="#313244", fg="#cdd6f4"
            )
            lbl_placa.pack()
 
            lbl_hora = tk.Label(
                frame_celda,
                text="",
                font=("Helvetica", 8),
                bg="#313244", fg="#a6adc8"
            )
            lbl_hora.pack()
 
            self.celdas_widgets.append({
                "frame": frame_celda,
                "estado": lbl_estado,
                "placa": lbl_placa,
                "hora": lbl_hora,
                "num": lbl_num
            })
 
            # Estado inicial
            self.estado_celdas[i] = {"ocupada": False, "placa": "", "hora": ""}
 
        # Panel de botones
        frame_botones = tk.Frame(self.root, bg="#1e1e2e")
        frame_botones.pack(pady=20)
 
        btn_entrada = tk.Button(
            frame_botones,
            text="🚗  Registrar Entrada",
            font=("Helvetica", 12, "bold"),
            bg="#a6e3a1", fg="#1e1e2e",
            activebackground="#94d2a0",
            width=20, height=2,
            bd=0, cursor="hand2",
            command=self._abrir_entrada
        )
        btn_entrada.grid(row=0, column=0, padx=15)
 
        btn_salida = tk.Button(
            frame_botones,
            text="🚪  Registrar Salida",
            font=("Helvetica", 12, "bold"),
            bg="#f38ba8", fg="#1e1e2e",
            activebackground="#e07a96",
            width=20, height=2,
            bd=0, cursor="hand2",
            command=self._abrir_salida
        )
        btn_salida.grid(row=0, column=1, padx=15)
 
        btn_actualizar = tk.Button(
            frame_botones,
            text="🔄  Actualizar",
            font=("Helvetica", 10),
            bg="#313244", fg="#cdd6f4",
            activebackground="#45475a",
            width=12, height=2,
            bd=0, cursor="hand2",
            command=self._actualizar_estado
        )
        btn_actualizar.grid(row=0, column=2, padx=15)
 
        # Contador libres/ocupadas
        self.lbl_resumen = tk.Label(
            self.root,
            text="Libres: 10 / 10",
            font=("Helvetica", 11),
            bg="#1e1e2e", fg="#a6adc8"
        )
        self.lbl_resumen.pack(pady=(0, 20))
 
