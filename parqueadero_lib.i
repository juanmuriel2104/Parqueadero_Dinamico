%module parqueadero_lib

%{
#include "Parqueadero.h"
%}

// Exponer el struct Celda
struct Celda {
    int id;
    bool ocupada;
    std::string placa;
    std::string horaEntrada;
};

// Exponer la clase Parqueadero
class Parqueadero {
public:
    Parqueadero(int totalCeldas = 10);
    int registrarPlaca(const std::string& placa, const std::string& hora);
    int registrarPlacaEnCelda(const std::string& placa, const std::string& hora, int idCelda);
    bool liberarPlaca(const std::string& placa);
    bool placaExiste(const std::string& placa) const;
    int getCeldasLibres() const;
    int getTotalCeldas() const;
};
