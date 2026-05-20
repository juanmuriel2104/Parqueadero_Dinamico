#include <iostream>
#include <thread>
#include <chrono>
#include <cstdlib>
#include "Parqueadero.h"
#include "GeneradorPlacas.h"

// Imprime el estado actual del parqueadero en consola
void imprimirEstado(const Parqueadero& p) {
    std::cout << "\n====== ESTADO PARQUEADERO ======\n";
    for (const auto& celda : p.getEstado()) {
        std::cout << "  Celda " << celda.id << ": ";
        if (celda.ocupada) {
            std::cout << "[OCUPADA] " << celda.placa << " (desde " << celda.horaEntrada << ")";
        } else {
            std::cout << "[LIBRE]";
        }
        std::cout << "\n";
    }
    std::cout << "  Libres: " << p.getCeldasLibres()
              << " / " << p.getTotalCeldas() << "\n";
    std::cout << "================================\n\n";
}

int main() {
    Parqueadero parqueadero(10);

    // Callback: se ejecuta cada vez que hay un evento
    auto callback = [&](std::string placa, std::string hora, int celda, std::string accion) {
        std::cout << "[" << hora << "] ";
        if (accion == "ENTRADA") {
            std::cout << "ENTRADA  - Placa: " << placa << " -> Celda " << celda << "\n";
        } else if (accion == "SALIDA") {
            std::cout << "SALIDA   - Placa: " << placa << "\n";
        } else if (accion == "LLENO") {
            std::cout << "LLENO    - Placa: " << placa << " no pudo entrar\n";
        }
        imprimirEstado(parqueadero);
    };


    GeneradorPlacas generador(parqueadero, callback);

    std::cout << "=== Sistema de Parqueadero - Fase 1 ===\n";
    std::cout << "Generando placas... (Ctrl+C para detener)\n\n";

    // Loop principal: genera una placa cada 2 o 5 segundos (aleatorio)
    while (true) {
        generador.tick();

        int espera = (std::rand() % 2 == 0) ? 2 : 5;
        std::this_thread::sleep_for(std::chrono::seconds(espera));
    }

    return 0;
}
