import zmq
import json
# Lo importamos para obtener el tamano del archivo que vamos a subir
# de esta forma no tenemos una restriccion por el tamano del archivo
import os


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://25.66.234.80:5555")

# download
# m = [b'download', b'gat.jpg']

# upload
fileBytes = ''
m = [b'upload', b'gato.jpg', fileBytes]


# Estamos verificando el contenido de la peticion
if m[0] == b'upload':

    if os.path.isfile(m[1].decode('utf-8')):

        file_stats = os.stat(m[1])

        print(f'File Size in Bytes is {file_stats.st_size}')

        fileSize = file_stats.st_size

        # Guardamos en una variable el archivo ubicado en la posicion 1 de m en modo read binary
        file = open(m[1], 'rb')
        fileBytes = file.read(fileSize)
        # print(fileBytes)
    else:
        print('Error. The file requested to upload doesnt exist')
        fileBytes = b'error'

m = [b'upload', b'gato.jpg', fileBytes]

socket.send_multipart(m)
# mR = message received
mR = socket.recv()
# m= m.decode('utf-8')

if m[0] == b'download':
    # save the file: open it in write bytes mode
    # m['fileName']
    file = open('hola1', 'wb')
    file.write(mR)
    file.close()
    if mR == b'Error el archivo deseado no se encuentra disponible para descarga':
        print(mR)
    else:
        print('file {} has been received successfully'.format(m[1]))
else:
    # Print the message: Error or success
    print(mR)
