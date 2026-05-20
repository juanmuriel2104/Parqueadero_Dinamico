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
 
    // Retorna el id de celda asignada, o -1 si el parqueadero está lleno
    int registrarPlaca(const std::string& placa, const std::string& hora);
 
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
