import socket
from connection import *

### Protocolo SMTP Enviar emails ###

def send_message(fromHost, toHost, mailFrom, mailTo, subject, msg):
  """
  Recibe str:
    fromHost (host de origen)
    toHost(host destino)
    mailFrom (mail remitente)
    mailTo(mail destino)
    subject(Asunto)
    msg (Cuerpo del mensaje)

  mailTo es un str que puede traer multiples destinatarios separados por coma
  Se genera un array a partir de str 'mailTo'.

  Envia mensaje a multiples destinatarios usando comandos de protocolo SMPT
  retorna array de responses
  """
  defFromHost(fromHost)
  defToHost(toHost)

  responses = []
  recipients = mailTo.split(",")
  i = 0

  #Setea ip en caso de traer nombre de host
  ip1 = socket.gethostbyname(fromHost)
  ip2 = socket.gethostbyname(toHost)

  #Se crea la conexion al host destino con ip y puerto
  con = socket.socket(IPV4, TCP)
  con.connect((ip2, PORT_SMTP))
  response = con.recv(1024).decode()
  responses.append(response)
  print(response)

  #Comando helo para establecer conexion con el servidor enviando host origen
  command = "HELO {}\n".format(ip1)
  con.send(command.encode())
  response = con.recv(1024).decode()
  responses.append(response)
  print(response)

  #Envia dirección de correo remitente
  command = "MAIL FROM: {}\n".format(mailFrom)
  con.send(command.encode())
  response = con.recv(1024).decode()
  responses.append(response)
  print(response)

  #Se envían lass n direcciones de correo destinatarios
  while(i < len(recipients)):
    command = "RCPT TO: {}\n".format(recipients[i])
    con.send(command.encode())
    response = con.recv(1024).decode()
    responses.append(response)
    print(response)
    i += 1

  #Se empieza a escribir el mensaje con el comando DATA
  command = "DATA\n"
  con.send(command.encode())

  command = "\n"
  con.send(command.encode())

  command = "Subject: {}\n\n".format(subject)
  con.send(command.encode())

  command = "From: {}\n".format(mailFrom)
  con.send(command.encode())

  while(i < len(recipients)):
    command = "To: {}\n".format(recipients[i])
    con.send(command.encode())
    i += 1

  command = "\n"
  con.send(command.encode())

  command = "{}\n".format(msg)
  con.send(command.encode())

  #Fin del mensaje
  endmsg = '\r\n.\r\n'
  con.send(endmsg.encode())
  response = con.recv(1024).decode()
  responses.append(response)
  print(response)

  #Fin de la sesión
  quit = "quit \n"
  con.send(quit.encode())
  response = con.recv(1024).decode()
  responses.append(response)
  print(response)

  return responses

