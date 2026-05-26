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

## Compilación y ejecución

## Paso 1 — Instalar Git

1. Entra a **https://git-scm.com/download/win**
2. Descarga el instalador y ábrelo
3. Deja todas las opciones por defecto y haz clic en **Next** hasta terminar
4. Abre una terminal CMD (tecla Windows → escribe `cmd` → Enter) y verifica:

```
git --version
```

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

---

## Paso 3 — Instalar MinGW-w64 (compilador C++)

1. Entra a **https://github.com/niXman/mingw-builds-binaries/releases**
2. En la sección **Assets** del release más reciente, descarga el archivo que diga:
   ```
   x86_64-...-release-win32-seh-msvcrt-rt_v12-rev0.7z
   ```
3. Descomprime el archivo `.7z`
   **https://www.7-zip.org/**
4. Dentro del archivo descomprimido encontrarás una carpeta llamada `mingw64`
5. Mueve esa carpeta a la raíz del disco: `C:\mingw64`
6. Agrega MinGW al PATH de Windows:
   - **"Variables de entorno"**
   - **"Editar las variables de entorno del sistema"**
   - **"Variables de entorno..."**
   - **"Variables del sistema"** **"Path"**
   - Clic en **"Nuevo"** → escribir exactamente: `C:\mingw64\bin`
   - Clic en **Aceptar** en todas las ventanas
7. Cierra el CMD. Verifica:

```
g++ --version
```
---

## Paso 4 — Instalar SWIG

1. Entra a **https://www.swig.org/download.html**
2. Descarga el archivo **swigwin** (el `.zip` de Windows)
3. Descomprime el `.zip`
4. Mueve esa carpeta a `C:\swigwin`
5. Dentro de `C:\swigwin` abre la carpeta que se creó (ej. `swigwin-4.4.1`) y verifica
   que hay un archivo llamado `swig.exe`
6. Agrega SWIG al PATH igual que MinGW:
   - Variables de entorno → Path → Nuevo
   - Escribe la ruta exacta donde está `swig.exe`
   - Clic en **Aceptar** en todas las ventanas
7. Cierra el CMD y abre uno nuevo. Verifica:

```
swig -version
```
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

---

## Paso 6 — Compilar el servidor C++

Dentro de la carpeta del proyecto:

```
g++ -std=c++17 -o servidor.exe main.cpp Parqueadero.cpp -lws2_32
```

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

> El número `314` al final de `-lpython314` corresponde a la versión de Python.
> Si el Python es 3.12, usa `-lpython312`. Si es 3.11, usa `-lpython311`.
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

### Terminal 2 — Abrir el visualizador Python

Abre un nuevo CMD y ejecuta:

```
cd C:\Parqueadero_Dinamico
python visualizador.py
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
