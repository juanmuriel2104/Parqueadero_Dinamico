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
- Parqueadero.h           # Clase que gestiona las celdas
- Parqueadero.cpp
- GeneradorPlacas.h       # Generador de placas aleatorias
- GeneradorPlacas.cpp
- main.cpp                # Servidor TCP (Windows - Winsock)
- main_linux.cpp          # Servidor TCP (Linux - POSIX)
- parqueadero_lib.i       # Interfaz SWIG
- visualizador.py         # Visualizador GUI en Python
- README.md
```


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

```bash
# 1. Compilar servidor
g++ -std=c++17 -o servidor main_linux.cpp Parqueadero.cpp GeneradorPlacas.cpp

# 2. Compilar librería SWIG
swig -c++ -python parqueadero_lib.i
g++ -std=c++17 -shared -fPIC -o _parqueadero_lib.so \
    parqueadero_lib_wrap.cxx Parqueadero.cpp GeneradorPlacas.cpp \
    $(python3-config --includes) $(python3-config --ldflags)

# 3. Correr el sistema (dos terminales)
./servidor                  # Terminal 1
python3 visualizador.py     # Terminal 2
```


### Windows

```bat
:: 1. Compilar servidor
g++ -std=c++17 -o servidor.exe main.cpp Parqueadero.cpp GeneradorPlacas.cpp -lws2_32

:: 2. Compilar librería SWIG
swig -c++ -python parqueadero_lib.i
g++ -std=c++17 -shared -o _parqueadero_lib.pyd parqueadero_lib_wrap.cxx ^
    Parqueadero.cpp GeneradorPlacas.cpp ^
    -I"C:\Users\...\Python314\include" ^
    -L"C:\Users\...\Python314\libs" -lpython314

:: 3. Correr el sistema (dos terminales)
servidor.exe                :: Terminal 1
python visualizador.py      :: Terminal 2
```

---

## Uso del visualizador

1. Inicia el servidor C++ primero
2. Ejecuta el visualizador Python
3. La grilla muestra las 10 celdas del parqueadero:
   - **Verde** = celda libre
   - **Rojo** = celda ocupada (muestra placa y hora de entrada)
4. **Registrar Entrada**: ingresa la placa y selecciona una celda libre
5. **Registrar Salida**: selecciona la placa del vehículo que sale
6. **Actualizar**: refresca el estado consultando al servidor

---

## Ramas Git

| Rama | Contenido |
|---|---|
| `main` | Código estable e integrado |
| `fase1` | Clases base C++ (Parqueadero, GeneradorPlacas) |
| `fase2` | Servidor socket TCP |
| `fase3` | Librería dinámica SWIG |
| `fase4` | Visualizador GUI Python |
