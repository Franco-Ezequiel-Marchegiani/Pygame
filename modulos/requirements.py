import os
def install_requirements():
    # Ejecuta este comando de python, que hace que instale las dependencias y librerías
    # Necesarias para que el proyecto se ejecute correctamente
    if os.name in ['nt', 'dos']: #Windows
        comando = 'python '
    else: #Mac o Linux
        comando = 'python3 '
    comando += '-m pip install -r requirements.txt'
    os.system(comando)

if __name__ == '__main__':
    install_requirements()

    from main import pythonisa
    
    pythonisa()