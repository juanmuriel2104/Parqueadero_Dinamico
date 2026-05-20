#include "Parqueadero.h"
#include <stdexcept>
 
Parqueadero::Parqueadero(int totalCeldas) : totalCeldas(totalCeldas) {
    for (int i = 0; i < totalCeldas; i++) {
        celdas.push_back({i, false, "", ""});
    }
}
