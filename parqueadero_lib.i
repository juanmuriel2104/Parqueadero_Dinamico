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
