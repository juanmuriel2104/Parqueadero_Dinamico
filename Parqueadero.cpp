#include "Parqueadero.h"
#include <stdexcept>
 
Parqueadero::Parqueadero(int totalCeldas) : totalCeldas(totalCeldas) {
    for (int i = 0; i < totalCeldas; i++) {
        celdas.push_back({i, false, "", ""});
    }
}

int Parqueadero::registrarPlaca(const std::string& placa, const std::string& hora) {
    // Buscar la primera celda libre
    for (auto& celda : celdas) {
        if (!celda.ocupada) {
            celda.ocupada    = true;
            celda.placa      = placa;
            celda.horaEntrada = hora;
            placaACelda[placa] = celda.id;
            return celda.id;
        }
    }
    return -1; // Parqueadero lleno
}
