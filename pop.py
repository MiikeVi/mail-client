import socket
from connection import *

### PROTOCOLO POP3 ###

def list_mails(user, passwd, host):
    """
    Recibe str: user, password y host de destino.
    Recupera los emails enviando el comando LIST.
    retorna un str.
    """
    #Set ip a partir del nombre de host 
    ip = socket.gethostbyname(host)

    #Se crea conexión socket
    con = connect(user, passwd, ip)

    command = "LIST \n"
    con.send(command.encode())
    response = con.recv(1024).decode()
    print(response)
    return response

def get_mails(user, passwd, id, host):
    """
    Recibe str: user, password, id, host
    id es una cadena separada por comas
    Crea un array de ids de correos a partir del str 'id'
    Usa el comando RETR n veces donde n = cantidad ids
    retorna array con responses
    """
    responses = []
    ids = id.split(",")
    i = 0
    ip = socket.gethostbyname(host)
    con = connect(user, passwd, ip)

    #Recorrer array de ids para obtener data de cada correo por su id
    while(i < len(ids)):
        command = "RETR {}\n".format(ids[i])
        con.send(command.encode())
        response = con.recv(1024).decode()
        print(response)
        responses.append(response)
        i += 1
    
    return responses

def delete_mail(user, passwd, id, host):
    """
    Recibe str: user, password, id, host
    id es una cadena de ids separadas por coma
    Crear array de ids a partir de 'id'
    Usa comandos DELE y QUIT n veces donde n = cantidad ids, 
    para eliminar los correos respectivos
    retorn array de responses
    """
    responses = []
    ids = id.split(",")
    i = 0
    ip = socket.gethostbyname(host)
    con = connect(user, passwd, ip)

    #Recorrer array de ids para ejecutar comando DELE y eliminar cada correo
    while(i < len(ids)):
        command = "DELE {}\n".format(ids[i])
        con.send(command.encode())
        response = con.recv(1024).decode()
        print(response)
        responses.append(response)
        i += 1

    #Termino de sesión
    command = "QUIT \n"
    con.send(command.encode())
    response = con.recv(1024).decode()
    print(response)
    responses.append(response)

    return responses

def connect(user, passwd, host):
    """
    Recibe user, password, host
    Autenticarse en servidor con los comandos USER y PASS de pop3 por medio de sockets
    retorna socket conexion
    """
    con = socket.socket(IPV4, TCP)
    con.connect((host, PORT_POP))
    response = con.recv(1024).decode()
    print(response)

    #Send nombre de usuario
    command = "USER {}\n".format(user)
    con.send(command.encode())
    response = con.recv(1024).decode()
    print(response)

    #Send contraseña
    command = "PASS {}\n".format(passwd)
    con.send(command.encode())
    response = con.recv(1024).decode()
    print(response)

    return con
