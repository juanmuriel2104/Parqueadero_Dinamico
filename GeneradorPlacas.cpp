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
