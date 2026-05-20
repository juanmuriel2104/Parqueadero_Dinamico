#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <ctime>
#include <iomanip>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include "Parqueadero.h"

#define PUERTO 5000
#define BUFFER_SIZE 1024

std::string obtenerHora() {
    std::time_t t = std::time(nullptr);
    std::tm* tm_local = std::localtime(&t);
    std::ostringstream oss;
    oss << std::setfill('0')
        << std::setw(2) << tm_local->tm_hour << ":"
        << std::setw(2) << tm_local->tm_min  << ":"
        << std::setw(2) << tm_local->tm_sec;
    return oss.str();
}
