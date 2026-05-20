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
 
    # ── Conexión ──────────────────────────────
    def _conectar(self):
        def intentar():
            ok = self.cliente.conectar()
            if ok:
                self.lbl_conexion.config(text="🟢 Conectado al servidor C++", fg="#a6e3a1")
                self._actualizar_estado()
            else:
                self.lbl_conexion.config(text="🔴 Sin conexión — ¿está corriendo el servidor?", fg="#f38ba8")
        threading.Thread(target=intentar, daemon=True).start()
 
    # ── Actualizar grilla ─────────────────────
    def _actualizar_estado(self):
        if not self.cliente.conectado:
            return
 
        respuesta = self.cliente.enviar("ESTADO")
        lineas = respuesta.strip().split("\n")
 
        libres = 0
        for linea in lineas:
            partes = linea.split("|")
            if len(partes) < 3:
                continue
            _, id_str, estado = partes[0], partes[1], partes[2]
            idx = int(id_str)
 
            if estado == "LIBRE":
                self.estado_celdas[idx] = {"ocupada": False, "placa": "", "hora": ""}
                libres += 1
            elif estado == "OCUPADA" and len(partes) >= 5:
                self.estado_celdas[idx] = {"ocupada": True, "placa": partes[3], "hora": partes[4]}
 
        self._refrescar_grilla()
        ocupadas = 10 - libres
        self.lbl_resumen.config(text=f"Libres: {libres} / 10   |   Ocupadas: {ocupadas} / 10")
 
    def _refrescar_grilla(self):
        for i, w in enumerate(self.celdas_widgets):
            celda = self.estado_celdas[i]
            if celda["ocupada"]:
                w["frame"].config(bg="#3d2a2a")
                w["num"].config(bg="#3d2a2a")
                w["estado"].config(text="OCUPADA", fg="#f38ba8", bg="#3d2a2a")
                w["placa"].config(text=celda["placa"], bg="#3d2a2a")
                w["hora"].config(text=celda["hora"], bg="#3d2a2a")
            else:
                w["frame"].config(bg="#2a3d2a")
                w["num"].config(bg="#2a3d2a")
                w["estado"].config(text="LIBRE", fg="#a6e3a1", bg="#2a3d2a")
                w["placa"].config(text="", bg="#2a3d2a")
                w["hora"].config(text="", bg="#2a3d2a")
 
    # ── Ventana Entrada ───────────────────────
    def _abrir_entrada(self):
        if not self.cliente.conectado:
            messagebox.showerror("Sin conexión", "No hay conexión con el servidor.")
            return
 
        # Celdas libres disponibles
        celdas_libres = [i for i, c in self.estado_celdas.items() if not c["ocupada"]]
        if not celdas_libres:
            messagebox.showwarning("Parqueadero lleno", "No hay celdas disponibles.")
            return
 
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Entrada")
        ventana.configure(bg="#1e1e2e")
        ventana.resizable(False, False)
        ventana.grab_set()
 
        tk.Label(ventana, text="Registrar Entrada de Vehículo",
                 font=("Helvetica", 14, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=(20, 15))
 
        # Placa
        tk.Label(ventana, text="Placa del vehículo:",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack()
 
        entry_placa = tk.Entry(ventana, font=("Helvetica", 13),
                               width=15, justify="center",
                               bg="#313244", fg="#cdd6f4",
                               insertbackground="#cdd6f4", bd=0)
        entry_placa.pack(pady=(5, 15), ipady=6)
        entry_placa.focus()
 
        # Celda
        tk.Label(ventana, text="Seleccionar celda libre:",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack()
 
        celda_var = tk.IntVar(value=celdas_libres[0])
        frame_celdas = tk.Frame(ventana, bg="#1e1e2e")
        frame_celdas.pack(pady=(5, 20))
 
        for idx, c in enumerate(celdas_libres):
            tk.Radiobutton(
                frame_celdas,
                text=f"Celda {c}",
                variable=celda_var,
                value=c,
                font=("Helvetica", 10),
                bg="#1e1e2e", fg="#a6e3a1",
                selectcolor="#313244",
                activebackground="#1e1e2e"
            ).grid(row=idx // 5, column=idx % 5, padx=8, pady=4)
 
        def confirmar():
            placa = entry_placa.get().strip().upper()
            celda = celda_var.get()
 
            if not placa:
                messagebox.showwarning("Campo vacío", "Ingresa la placa.", parent=ventana)
                return
 
            respuesta = self.cliente.enviar(f"ENTRADA|{placa}|{celda}")
            partes = respuesta.split("|")
 
            if partes[0] == "OK":
                hora = partes[2] if len(partes) > 2 else ""
                messagebox.showinfo("Entrada registrada",
                                    f"✅ {placa} ingresó a celda {celda}\nHora: {hora}",
                                    parent=ventana)
                ventana.destroy()
                self._actualizar_estado()
            else:
                error = partes[1] if len(partes) > 1 else "desconocido"
                messagebox.showerror("Error", f"No se pudo registrar: {error}", parent=ventana)
 
        tk.Button(
            ventana, text="✅  Confirmar Entrada",
            font=("Helvetica", 12, "bold"),
            bg="#a6e3a1", fg="#1e1e2e",
            width=22, height=2, bd=0,
            cursor="hand2",
            command=confirmar
        ).pack(pady=(0, 20))
 
    # ── Ventana Salida ────────────────────────
    def _abrir_salida(self):
        if not self.cliente.conectado:
            messagebox.showerror("Sin conexión", "No hay conexión con el servidor.")
            return
 
        placas_dentro = [
            (i, c["placa"], c["hora"])
            for i, c in self.estado_celdas.items()
            if c["ocupada"]
        ]
 
        if not placas_dentro:
            messagebox.showinfo("Parqueadero vacío", "No hay vehículos en el parqueadero.")
            return
 
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Salida")
        ventana.configure(bg="#1e1e2e")
        ventana.resizable(False, False)
        ventana.grab_set()
 
        tk.Label(ventana, text="Registrar Salida de Vehículo",
                 font=("Helvetica", 14, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=(20, 15))
 
        tk.Label(ventana, text="Selecciona el vehículo que sale:",
                 font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#a6adc8").pack()
 
        placa_var = tk.StringVar(value=placas_dentro[0][1])
        frame_placas = tk.Frame(ventana, bg="#1e1e2e")
        frame_placas.pack(pady=(10, 20), padx=20)
 
        for celda_id, placa, hora in placas_dentro:
            tk.Radiobutton(
                frame_placas,
                text=f"Celda {celda_id}  —  {placa}  (desde {hora})",
                variable=placa_var,
                value=placa,
                font=("Helvetica", 11),
                bg="#1e1e2e", fg="#f38ba8",
                selectcolor="#313244",
                activebackground="#1e1e2e",
                anchor="w"
            ).pack(fill="x", pady=3)
 
        def confirmar():
            placa = placa_var.get()
            respuesta = self.cliente.enviar(f"SALIDA|{placa}")
            partes = respuesta.split("|")
 
            if partes[0] == "OK":
                messagebox.showinfo("Salida registrada",
                                    f"✅ {placa} ha salido del parqueadero.",
                                    parent=ventana)
                ventana.destroy()
                self._actualizar_estado()
            else:
                error = partes[1] if len(partes) > 1 else "desconocido"
                messagebox.showerror("Error", f"No se pudo registrar: {error}", parent=ventana)
 
        tk.Button(
            ventana, text="🚪  Confirmar Salida",
            font=("Helvetica", 12, "bold"),
            bg="#f38ba8", fg="#1e1e2e",
            width=22, height=2, bd=0,
            cursor="hand2",
            command=confirmar
        ).pack(pady=(0, 20))
 
 
# ─────────────────────────────────────────────
# Arranque
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
