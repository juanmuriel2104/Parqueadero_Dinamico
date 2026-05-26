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

# 🛠️ Guía de instalación y ejecución en Windows

Esta guía explica cómo instalar todas las herramientas necesarias y correr el sistema
de parqueadero en cualquier PC con Windows desde cero.

---

## 📋 Requisitos

| Herramienta | Versión mínima | Para qué sirve |
|---|---|---|
| Git | cualquier versión | Clonar el repositorio |
| Python | 3.10+ | Correr el visualizador |
| MinGW-w64 | 64 bits | Compilar el servidor C++ |
| SWIG | 4.x | Generar la librería dinámica |

---

## Paso 1 — Instalar Git

1. Entra a **https://git-scm.com/download/win**
2. Descarga el instalador y ábrelo
3. Deja todas las opciones por defecto y haz clic en **Next** hasta terminar
4. Abre una terminal CMD (tecla Windows → escribe `cmd` → Enter) y verifica:

```
git --version
```

Debe salir algo como `git version 2.x.x`

---

## Paso 2 — Instalar Python

1. Entra a **https://www.python.org/downloads/**
2. Descarga el instalador haciendo clic en el botón amarillo **"Download Python 3.x.x"**
3. Abre el instalador
4. ⚠️ **MUY IMPORTANTE** — antes de hacer clic en "Install Now", marca la casilla
   **"Add Python to PATH"** en la parte inferior del instalador
5. Haz clic en **"Install Now"**
6. Cierra el CMD y abre uno nuevo. Verifica:

```
python --version
```

Debe salir algo como `Python 3.x.x`

---

## Paso 3 — Instalar MinGW-w64 (compilador C++)

1. Entra a **https://github.com/niXman/mingw-builds-binaries/releases**
2. En la sección **Assets** del release más reciente, descarga el archivo que diga:
   ```
   x86_64-...-release-win32-seh-msvcrt-rt_v12-rev0.7z
   ```
3. Descomprime el archivo `.7z` — si no tienes descompresor, instala **7-Zip** desde
   **https://www.7-zip.org/**
4. Dentro del archivo descomprimido encontrarás una carpeta llamada `mingw64`
5. Mueve esa carpeta a la raíz del disco: `C:\mingw64`
6. Agrega MinGW al PATH de Windows:
   - Tecla Windows → escribe **"Variables de entorno"**
   - Clic en **"Editar las variables de entorno del sistema"**
   - Clic en **"Variables de entorno..."**
   - En la sección **"Variables del sistema"** busca **"Path"** → doble clic
   - Clic en **"Nuevo"** → escribe exactamente: `C:\mingw64\bin`
   - Clic en **Aceptar** en todas las ventanas
7. Cierra el CMD y abre uno nuevo. Verifica:

```
g++ --version
```

Debe decir `x86_64` en la primera línea. Ejemplo: `g++ (x86_64-...) 16.x.x`

---

## Paso 4 — Instalar SWIG

1. Entra a **https://www.swig.org/download.html**
2. Descarga el archivo **swigwin** (el `.zip` de Windows), por ejemplo `swigwin-4.x.x.zip`
3. Descomprime el `.zip` — te queda una carpeta como `swigwin-4.x.x`
4. Mueve esa carpeta a `C:\swigwin`
5. Dentro de `C:\swigwin` abre la carpeta que se creó (ej. `swigwin-4.4.1`) y verifica
   que hay un archivo llamado `swig.exe`
6. Agrega SWIG al PATH igual que MinGW:
   - Variables de entorno → Path → Nuevo
   - Escribe la ruta exacta donde está `swig.exe`, por ejemplo: `C:\swigwin\swigwin-4.4.1`
   - Clic en **Aceptar** en todas las ventanas
7. Cierra el CMD y abre uno nuevo. Verifica:

```
swig -version
```

Debe salir `SWIG Version 4.x.x`

---

## Paso 5 — Clonar el repositorio

Abre el CMD y ejecuta:

```
cd C:\
git clone https://github.com/juanmuriel2104/Parqueadero_Dinamico.git
cd Parqueadero_Dinamico
```

Verifica que están todos los archivos:

```
dir
```

Debes ver: `Parqueadero.h`, `Parqueadero.cpp`, `main.cpp`, `main_linux.cpp`,
`parqueadero_lib.i`, `visualizador.py`, `README.md`

---

## Paso 6 — Compilar el servidor C++

Dentro de la carpeta del proyecto:

```
g++ -std=c++17 -o servidor.exe main.cpp Parqueadero.cpp -lws2_32
```

Si no hay mensajes de error, el archivo `servidor.exe` fue creado correctamente.

---

## Paso 7 — Compilar la librería SWIG

Primero verifica la ruta donde está instalado Python en este PC:

```
python -c "import sys; print(sys.prefix)"
```

Copia la ruta que te muestra (ejemplo: `C:\Users\usuario\AppData\Local\Programs\Python\Python314`)
y úsala en el siguiente comando reemplazando `TU_RUTA_PYTHON`:

```
swig -c++ -python parqueadero_lib.i
```

```
g++ -std=c++17 -shared -o _parqueadero_lib.pyd parqueadero_lib_wrap.cxx Parqueadero.cpp -I"TU_RUTA_PYTHON\include" -L"TU_RUTA_PYTHON\libs" -lpython314
```

> ⚠️ El número `314` al final de `-lpython314` corresponde a la versión de Python.
> Si tu Python es 3.12, usa `-lpython312`. Si es 3.11, usa `-lpython311`.
> Puedes verificarlo con `python --version`.

Si no hay mensajes de error, el archivo `_parqueadero_lib.pyd` fue creado correctamente.

---

## Paso 8 — Ejecutar el sistema

Necesitas **dos ventanas CMD abiertas al mismo tiempo**.

### Terminal 1 — Arrancar el servidor C++

```
cd C:\Parqueadero_Dinamico
servidor.exe
```

Debes ver:
```
=== Servidor Parqueadero ===
Escuchando en puerto 5000...
Esperando conexion del visualizador Python...
```

⚠️ No cierres esta ventana — el servidor debe seguir corriendo.

### Terminal 2 — Abrir el visualizador Python

Abre un nuevo CMD y ejecuta:

```
cd C:\Parqueadero_Dinamico
python visualizador.py
```

Se abre la ventana gráfica del parqueadero con las 10 celdas.

---

## ✅ Verificación final

En la interfaz gráfica debes poder:

- Ver las 10 celdas en verde (libres)
- Hacer clic en **"Registrar Entrada"**, ingresar una placa y seleccionar una celda
- Ver esa celda cambiar a rojo con la placa y la hora
- Hacer clic en **"Registrar Salida"**, seleccionar la placa y ver la celda volver a verde
- En la Terminal 1 (servidor) ver los mensajes de cada operación en tiempo real

---

## ❗ Solución a problemas comunes

**`g++` no se reconoce como comando**
→ Cierra el CMD y abre uno nuevo. Si persiste, verifica que `C:\mingw64\bin` está en el PATH.

**`swig` no se reconoce como comando**
→ Verifica que la ruta en el PATH apunta exactamente a la carpeta donde está `swig.exe`,
no a la carpeta padre.

**`python` no se reconoce como comando**
→ Verifica que instalaste Python marcando la casilla "Add Python to PATH".
Puedes reinstalar Python y esta vez marcar esa casilla.

**Error al compilar SWIG: `python3xx.lib not found`**
→ Verifica la versión exacta de Python con `python --version` y ajusta el número
en `-lpython3xx` del comando de compilación.

**El visualizador dice "Sin conexión"**
→ Verifica que el servidor está corriendo en la Terminal 1 antes de abrir el visualizador.

**Puerto 5000 en uso**
→ Cierra cualquier otra aplicación que use ese puerto, o reinicia el PC.
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
