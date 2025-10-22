#include <cstdlib>  
#include <string>   

#define PYTHON_PATH "C:/Users/eskfr/anaconda3/envs/apienv/python.exe"
#define SCRIPT "-m source.osebx.py"

int main() {
    
    std::string command = std::string(PYTHON_PATH) + " " + SCRIPT;
    system(command.c_str());

    return 0;
}
