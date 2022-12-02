# Importamos las librerias necesarias
from git import Repo  # En primer lugar importamos nuestro repo remoto
import re  # importamos expresiones regulares
import sys  # importamos sys para controlar la salida
import signal  # importamos signal para controlar la salida
import pandas as pd # para transformar a df el dccionario final

def handler_signal(signal, frame):  # Funcion para regular la salida
    # En caso de salida mostraremos dicho mensaj epor pantalla
    print("\n\n Ha comenzado la salida ordenada y controlada del programa")
    sys.exit(1)


# Ctrl + C Boton que debemos pulsar para interrumpir ejecucion
signal.signal(signal.SIGINT, handler_signal)
# A continuacion tenemos nuestro url del repo
REPO_DIR = 'skale/skale-manager'
# vamos a definir una serie de palabras importantes, para obtener informacion necesaria
PAlABRAS_CLAVE = ['password', 'credentials',
                  'username', 'key', 'user', 'secret_word', "private"]


def extract(repo_dir):  # Funcion para la extraccion de datos
    repo = Repo(repo_dir)  # con el repositorio remoto creamos el local
    dir(repo)
    # Hacemos un itter de commmits
    commits = list(repo.iter_commits('develop'))
    return commits  # una vez sacamos los commits los guardamos y se lo pasaremos a transform


def transform(commits):  # A continuación transformaremos los datos

    dicci = dict()  # Iniciamos un diccionario
    for i in commits:  # hacemos un bucle para recoorer los commitss
        for palabra in PAlABRAS_CLAVE:  # bucamos si las distintas palabras pertenecen a palabras clave
            if re.search(palabra, i.message, re.IGNORECASE):
                valor = i.message  #  buestro valor asociado a dicha clave sera el mmesage
                clave = i.hexsha  # nuestra llave del diccionario va a ser i.hesha
                # rellenamos el diccionario con key como llave y data como valor
                dicci[clave] = valor

    return dicci  # una vez complletamdo el diccionario lo devolveremos


def load(diccionario): # por ultimo le realizamops el load , devolveremos dataframe
    df = pd.DataFrame([[key, diccionario[key]]
                      for key in diccionario.keys()], columns=['Commit', 'Ocurrencia'])
    return df 


if __name__ == '__main__':
    # Nos creamos un main para lanzarlo 
    commits = extract(REPO_DIR)
    diccionario = transform(commits)
    df = load(diccionario)
    df.to_json("commit-leaks.json", indent = 1)
