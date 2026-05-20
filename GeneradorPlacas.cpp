#include "GeneradorPlacas.h"
#include <cstdlib>
#include <ctime>
#include <sstream>
#include <iomanip>

GeneradorPlacas::GeneradorPlacas(Parqueadero& parqueadero,
                                 std::function<void(std::string, std::string, int, std::string)> callback)
    : parqueadero(parqueadero), onEvento(callback) {
    std::srand(static_cast<unsigned>(std::time(nullptr)));
}
 
std::string GeneradorPlacas::generarPlacaAleatoria() {
    // Formato: ABC-123
    // Pool pequeño de letras para aumentar probabilidad de repetición (simula salidas)
    const std::string letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const std::string digitos = "0123456789";

    // Usamos un pool reducido para que haya repeticiones y se simulen salidas
    const int POOL_LETRAS = 8;
    const int POOL_DIGITOS = 5;
 
    std::string placa = "";
    placa += letras[std::rand() % POOL_LETRAS];
    placa += letras[std::rand() % POOL_LETRAS];
    placa += letras[std::rand() % POOL_LETRAS];
    placa += "-";
    placa += digitos[std::rand() % POOL_DIGITOS];
    placa += digitos[std::rand() % POOL_DIGITOS];
    placa += digitos[std::rand() % POOL_DIGITOS];
 
    return placa;
}

std::string GeneradorPlacas::obtenerHoraActual() {
    std::time_t t = std::time(nullptr);
    std::tm* tm_local = std::localtime(&t);
    std::ostringstream oss;
    oss << std::setfill('0')
        << std::setw(2) << tm_local->tm_hour << ":"
        << std::setw(2) << tm_local->tm_min  << ":"
        << std::setw(2) << tm_local->tm_sec;
    return oss.str();
}
 
void GeneradorPlacas::procesarPlaca(const std::string& placa) {
    std::string hora = obtenerHoraActual();
 
    if (parqueadero.placaExiste(placa)) {
        // La placa ya está → es una salida
        parqueadero.liberarPlaca(placa);
        onEvento(placa, hora, -1, "SALIDA");
    } else {
        // Es una entrada
        int celda = parqueadero.registrarPlaca(placa, hora);
        if (celda == -1) {
            onEvento(placa, hora, -1, "LLENO");
        } else {
            onEvento(placa, hora, celda, "ENTRADA");
        }
    }
}
 
void GeneradorPlacas::tick() {
    std::string placa = generarPlacaAleatoria();
    procesarPlaca(placa);
}
