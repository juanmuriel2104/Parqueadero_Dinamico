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
    // Formato colombiano: ABC-123
    // Pool pequeño de letras para aumentar probabilidad de repetición (simula salidas)
    const std::string letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const std::string digitos = "0123456789";
