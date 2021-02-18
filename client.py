import zmq
import json
# Lo importamos para obtener el tamano del archivo que vamos a subir
# de esta forma no tenemos una restriccion por el tamano del archivo
import os


# Funcion principal
def Main():
    Conexion()


# Funcion de conexion, para crear el context y organizar el socket


def Conexion():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")
    Request(socket)


def Request(socket):
    print('Cual operacion desearia realizar?')
    peticion = int(input('1. Subir 2. Descargar = '))
    # print(peticion)
    if (peticion == 1 or peticion == 2):
        # La peticion para subir arhivos se identifica con el numero 1
        if peticion == 1:
            fileBytes = ''
            infoEnviar = [b'upload', b'gato.jpg', fileBytes]
            if os.path.isfile(infoEnviar[1].decode('utf-8')):
                file_stats = os.stat(infoEnviar[1])
                print(f'File Size in Bytes is {file_stats.st_size}')
                fileSize = file_stats.st_size
                # Guardamos en una variable el archivo ubicado en
                # la posicion 1 de m en modo read binary
                file = open(infoEnviar[1], 'rb')
                fileBytes = file.read(fileSize)
                # print(fileBytes)
            else:
                print('Error. The file requested to upload doesnt exist')
                fileBytes = b'error'
        if peticion == 1:
            infoEnviar = [b'upload', b'gato.jpg', fileBytes]
            socket.send_multipart(infoEnviar)
        if peticion == 2:
            msjRecibido = [b'download', b'gato.jpg']
            socket.send_multipart(msjRecibido)
        # socket.send_multipart(infoEnviar)
        # msjRecibido = message received
        msjRecibido = socket.recv()
        # m= m.decode('utf-8')
        if peticion == 2:
            # save the file: open it in write bytes mode
            # m['fileName']
            file = open('catJoe.jpg', 'wb')
            file.write(msjRecibido)
            file.close()
            if msjRecibido == b'Error el archivo deseado no se encuentra disponible para descarga':
                print(msjRecibido)
            else:
                print('file {} has been received successfully'.format(msjRecibido[1]))

    else:
        print('La opcion que ha elegido no existe')
        print('Por favor intente nuevamente marcando 1 para subir o 2 para descargar')

        # download
        #m = [b'download', b'gato.jpg']
        # upload

    # Estamos verificando el contenido de la peticion


while True:
    Main()
