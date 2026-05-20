#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <ctime>
#include <iomanip>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include "Parqueadero.h"

#define PUERTO 5000
#define BUFFER_SIZE 1024

std::string obtenerHora() {
    std::time_t t = std::time(nullptr);
    std::tm* tm_local = std::localtime(&t);
    std::ostringstream oss;
    oss << std::setfill('0')
        << std::setw(2) << tm_local->tm_hour << ":"
        << std::setw(2) << tm_local->tm_min  << ":"
        << std::setw(2) << tm_local->tm_sec;
    return oss.str();
}

std::vector<std::string> split(const std::string& s, char delim) {
    std::vector<std::string> tokens;
    std::stringstream ss(s);
    std::string token;
    while (std::getline(ss, token, delim)) tokens.push_back(token);
    return tokens;
}
 
std::string procesarMensaje(const std::string& mensaje, Parqueadero& parqueadero) {
    std::vector<std::string> partes = split(mensaje, '|');
    if (partes.empty()) return "ERROR|MENSAJE_VACIO";
    std::string comando = partes[0];
 
    if (comando == "ENTRADA") {
        if (partes.size() < 3) return "ERROR|FORMATO_INCORRECTO";
        std::string placa = partes[1];
        int celda = std::stoi(partes[2]);
        std::string hora = obtenerHora();
        if (parqueadero.placaExiste(placa)) return "ERROR|PLACA_YA_EXISTE";
        int celdaAsignada = parqueadero.registrarPlacaEnCelda(placa, hora, celda);
        if (celdaAsignada == -1) return "ERROR|CELDA_OCUPADA";
        return "OK|" + placa + "|" + hora + "|" + std::to_string(celdaAsignada);
    }
    if (comando == "SALIDA") {
        if (partes.size() < 2) return "ERROR|FORMATO_INCORRECTO";
        std::string placa = partes[1];
        if (!parqueadero.placaExiste(placa)) return "ERROR|PLACA_NO_EXISTE";
        parqueadero.liberarPlaca(placa);
        return "OK|" + placa;
    }
    if (comando == "ESTADO") {
        std::string respuesta = "";
        for (const auto& c : parqueadero.getEstado()) {
            if (c.ocupada)
                respuesta += "CELDA|" + std::to_string(c.id) + "|OCUPADA|" + c.placa + "|" + c.horaEntrada + "\n";
            else
                respuesta += "CELDA|" + std::to_string(c.id) + "|LIBRE\n";
        }
        return respuesta.empty() ? "ESTADO_VACIO\n" : respuesta;
    }
    return "ERROR|COMANDO_DESCONOCIDO";
}
 
int main() {
    Parqueadero parqueadero(10);
    int serverFd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(serverFd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
 
    sockaddr_in addr{};
    addr.sin_family      = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port        = htons(PUERTO);
 
    bind(serverFd, (sockaddr*)&addr, sizeof(addr));
    listen(serverFd, 1);
 
    std::cout << "=== Servidor Parqueadero (Linux) ===\n";
    std::cout << "Escuchando en puerto " << PUERTO << "...\n\n";
 
    while (true) {
        int clientFd = accept(serverFd, nullptr, nullptr);
        if (clientFd < 0) continue;
        std::cout << "[Conexion recibida]\n";
 
        char buffer[BUFFER_SIZE];
        while (true) {
            memset(buffer, 0, BUFFER_SIZE);
            int bytes = recv(clientFd, buffer, BUFFER_SIZE - 1, 0);
            if (bytes <= 0) { std::cout << "[Cliente desconectado]\n\n"; break; }
 
            std::string mensaje(buffer);
            while (!mensaje.empty() && (mensaje.back() == '\n' || mensaje.back() == '\r'))
                mensaje.pop_back();
 
            std::cout << "[Recibido]: " << mensaje << "\n";
            std::string respuesta = procesarMensaje(mensaje, parqueadero);
            std::cout << "[Enviado]:  " << respuesta << "\n";
            respuesta += "\n";
            send(clientFd, respuesta.c_str(), respuesta.size(), 0);
        }
        close(clientFd);
    }
    close(serverFd);
    return 0;
}
