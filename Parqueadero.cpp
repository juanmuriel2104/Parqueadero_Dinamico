#include "Parqueadero.h"
#include <stdexcept>

Parqueadero::Parqueadero(int totalCeldas) : totalCeldas(totalCeldas) {
    for (int i = 0; i < totalCeldas; i++) {
        celdas.push_back({i, false, "", ""});
    }
}

int Parqueadero::registrarPlaca(const std::string& placa, const std::string& hora) {
    for (auto& celda : celdas) {
        if (!celda.ocupada) {
            celda.ocupada     = true;
            celda.placa       = placa;
            celda.horaEntrada = hora;
            placaACelda[placa] = celda.id;
            return celda.id;
        }
    }
    return -1;
}

int Parqueadero::registrarPlacaEnCelda(const std::string& placa, const std::string& hora, int idCelda) {
    if (idCelda < 0 || idCelda >= totalCeldas) return -1;
    if (celdas[idCelda].ocupada) return -1;

    celdas[idCelda].ocupada     = true;
    celdas[idCelda].placa       = placa;
    celdas[idCelda].horaEntrada = hora;
    placaACelda[placa]          = idCelda;
    return idCelda;
}

bool Parqueadero::liberarPlaca(const std::string& placa) {
    auto it = placaACelda.find(placa);
    if (it == placaACelda.end()) return false;

    int id = it->second;
    celdas[id].ocupada     = false;
    celdas[id].placa       = "";
    celdas[id].horaEntrada = "";
    placaACelda.erase(it);
    return true;
}

bool Parqueadero::placaExiste(const std::string& placa) const {
    return placaACelda.count(placa) > 0;
}

std::vector<Celda> Parqueadero::getEstado() const {
    return celdas;
}

int Parqueadero::getCeldasLibres() const {
    int libres = 0;
    for (const auto& c : celdas) {
        if (!c.ocupada) libres++;
    }
    return libres;
}

int Parqueadero::getTotalCeldas() const {
    return totalCeldas;
}
