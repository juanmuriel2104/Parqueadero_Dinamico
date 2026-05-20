#ifndef PARQUEADERO_H
#define PARQUEADERO_H

#include <string>
#include <map>
#include <vector>

struct Celda {
    int id;
    bool ocupada;
    std::string placa;
    std::string horaEntrada;
};

class Parqueadero {
private:
    int totalCeldas;
    std::vector<Celda> celdas;
    std::map<std::string, int> placaACelda; // placa -> id de celda

public:
    Parqueadero(int totalCeldas = 10);

    // Retorna el id de celda asignada, o -1 si el parqueadero está lleno (asigna la primera libre)
    int registrarPlaca(const std::string& placa, const std::string& hora);

    // Registra la placa en una celda específica elegida por el operario. Retorna -1 si está ocupada
    int registrarPlacaEnCelda(const std::string& placa, const std::string& hora, int idCelda);

    // Retorna true si la placa existía y se liberó
    bool liberarPlaca(const std::string& placa);

    // Retorna true si la placa ya está en el parqueadero
    bool placaExiste(const std::string& placa) const;

    // Estado completo de todas las celdas
    std::vector<Celda> getEstado() const;

    int getCeldasLibres() const;
    int getTotalCeldas() const;
};

#endif
