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
