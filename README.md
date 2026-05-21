# Parqueadero_Dinamico


Proyectode **Estructura de Datos** — ITM
Juan Diego Muriel Bedoya

---

## Descripción

Sistema de gestión de parqueadero en tiempo real compuesto por dos componentes que se comunican mediante sockets TCP:

- **Servidor C++**: gestiona las celdas del parqueadero y expone una API por socket TCP.
- **Visualizador Python**: interfaz gráfica (tkinter) que se conecta al servidor y permite registrar entradas y salidas de vehículos.

La comunicación entre C++ y Python también se realiza mediante una **librería dinámica** generada con **SWIG**, que expone la clase `Parqueadero` directamente a Python.

---

## Arquitectura

```
┌─────────────────────────┐     Socket TCP      ┌──────────────────────────┐
│   Servidor C++          │ ──────────────────► │   Visualizador Python    │
│                         │                     │                          │
│  • Parqueadero (10 cel) │                     │  • GUI tkinter           │
│  • GeneradorPlacas      │                     │  • ClienteSocket         │
│  • Socket TCP :5000     │                     │  • Registrar entrada     │
│                         │                     │  • Registrar salida      │
└─────────────────────────┘                     └──────────────────────────┘
         ▲
         │ expone vía SWIG
┌────────┴────────┐
│  _parqueadero_  │
│  lib.so / .pyd  │
└─────────────────┘
```

---

## Estructura del proyecto

```
Parqueadero_Dinamico/
├── Parqueadero.h           # Clase que gestiona las celdas
├── Parqueadero.cpp
├── GeneradorPlacas.h       # Generador de placas aleatorias
├── GeneradorPlacas.cpp
├── main.cpp                # Servidor TCP (Windows - Winsock)
├── main_linux.cpp          # Servidor TCP (Linux - POSIX)
├── parqueadero_lib.i       # Interfaz SWIG
├── visualizador.py         # Visualizador GUI en Python
└── README.md
```

---

## Protocolo de comunicación (socket TCP)

| Python envía | C++ responde |
|---|---|
| `ENTRADA\|ABC-123\|3` | `OK\|ABC-123\|10:35:42\|3` |
| `SALIDA\|ABC-123` | `OK\|ABC-123` |
| `ESTADO` | `CELDA\|0\|LIBRE`, `CELDA\|1\|OCUPADA\|XYZ-999\|10:30:00`, ... |

**Errores posibles:**
- `ERROR|PLACA_YA_EXISTE`
- `ERROR|CELDA_OCUPADA`
- `ERROR|PLACA_NO_EXISTE`
- `ERROR|FORMATO_INCORRECTO`

---

## Requisitos

### Linux (GitHub Codespaces)
- g++ con soporte C++17
- SWIG 4.2.0+
- Python 3.12+

### Windows
- MinGW-w64 16.x (x86_64)
- SWIG 4.4.1
- Python 3.14

---

## compilación y ejecución

### Linux / GitHub Codespaces
