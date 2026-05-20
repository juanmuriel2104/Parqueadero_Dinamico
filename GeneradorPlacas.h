#ifndef GENERADORPLACAS_H
#define GENERADORPLACAS_H

#include <string>
#include <functional>
#include "Parqueadero.h"

class GeneradorPlacas {
private:
    Parqueadero& parqueadero;

    // Callback que se llama cada vez que se registra un evento
    // Parámetros: placa, hora, celda asignada (-1 si lleno o liberada), acción ("ENTRADA"/"SALIDA"/"LLENO")
    std::function<void(std::string, std::string, int, std::string)> onEvento;

    std::string generarPlacaAleatoria();
    std::string obtenerHoraActual();

public:
    GeneradorPlacas(Parqueadero& parqueadero,
                    std::function<void(std::string, std::string, int, std::string)> callback);

    // Procesa una placa: decide si es entrada o salida y notifica
    void procesarPlaca(const std::string& placa);

    // Genera y procesa una placa aleatoria (llamar desde el loop principal)
    void tick();
};

#endif
