import zmq
import json
import os


def Main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5555")
    Request(socket)


def Request(socket):
    print('Please input your desired selection:')
    peticion = int(input('1.Upload   2.Download = '))
    if peticion == 1:
        Subir(socket)
    elif peticion == 2:
        Descargar(socket)
    else:
        print('Incorrect input, please enter a valid number.')


def Subir(socket):
    # upload
    fileBytes = ''
    fileName = b'holaMundo.txt'
    if os.path.isfile(fileName.decode('utf-8')):
        file_stats = os.stat(fileName.decode('utf-8'))
        print(f'File Size in Bytes is {file_stats.st_size}')
        fileSize = file_stats.st_size
        # Guardamos en una variable el archivo ubicado en la posicion 1 de m en modo read binary
        file = open(fileName.decode('utf-8'), 'rb')
        fileBytes = file.read(fileSize)
        # print(fileBytes)
    else:
        print('Error. The file requested to upload doesnt exist')
        fileBytes = b'error'
    m = [b'upload', fileName, fileBytes]
    socket.send_multipart(m)
    # mR = message received
    mR = socket.recv()
    print('{}'.format(mR.decode('utf-8')))


def Descargar(socket):
    # download
    fileName = b'gato.jpg'
    m = [b'download', fileName]
    socket.send_multipart(m)
    # mR = message received
    mR = socket.recv()
    if mR == b'Error. File requested is not available for download':
        print(mR)
    else:
        # save the file: open it in write bytes mode
        file = open(fileName.decode('utf-8'), 'wb')
        file.write(mR)
        file.close()
        print('file {} has been received successfully'.format(m[1].decode('utf-8')))


if __name__ == "__main__":
    while True:
        Main()
