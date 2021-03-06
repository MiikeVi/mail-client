from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog
import sys
import pop
import smtp

### UI CLASSES ###

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
        self.button_login.clicked.connect(self.showMenu)
        self.menu = {}

    def showMenu(self):
        'Set campos user, password y genera instancia de clase Menu'

        user = self.input_user.text()
        password = self.input_password.text()
        if self.checkAuth(user, password):
            self.createDialog()
            return 
        self.menu = Menu(user, password)
        self.menu.show()
        self.close()
    
    #Validación campos user y pass de login
    def checkAuth(self, user, password):
        'Validar campos user y password llenos'

        return user == "" or password == ""   
    
    #Crear Dialog
    def createDialog(self):
        'Genera instancia de clase Dialog seteando label  de error'

        self.dialog = Dialog()
        self.dialog.label_response.setPlainText("Debe ingresar usuario y contraseña")
        self.dialog.show()

class Menu(QtWidgets.QMainWindow):
    def __init__(self, user, password):
        super().__init__()
        uic.loadUi("ui/menu.ui", self)
        self.mailbox = {}
        self.send = Send()

        #Eventos buttons
        self.button_new_mail.clicked.connect(self.showSend)
        self.button_check_mailbox.clicked.connect(lambda:self.showMailbox(user, password))
        self.button_exit.clicked.connect(self.exit)
        
    def showMailbox(self, user, password):
        'Genera instancia de Mailbox y hace visible la ventana'

        self.mailbox = MailBox(user, password)
        self.mailbox.show()

    def showSend(self):
        'Hace visible objeto(ventana) Send'

        self.send.show()
    
    def exit(self):
        'Terminar ejecución del programa'

        sys.exit(app.exec_())

class Send(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/send.ui", self)
        self.dialog = {}
        self.button_send.clicked.connect(self.send_mail)

    def send_mail(self):
        'Setea campos necesarios para usar funcion send_message y crea un cuadro de dialogo con la response'

        fromHost = self.input_from_host.text()
        toHost = self.input_to_host.text()
        from_ = self.input_from.text()
        to = self.input_to.text()
        subject = self.input_subject.text()
        msg = self.input_msg.toPlainText()

        #Chequear campos necesarios
        if self.checkFields(fromHost, toHost, from_, to, subject, msg):
            self.createDialog()
            return

        #Array send, guarda data de correos
        send = smtp.send_message(fromHost, toHost, from_, to, subject, msg)
        dialogMessage = ""
        self.dialog = Dialog()

        #Generando texto del dialog
        for i in range(len(send)):
            dialogMessage = dialogMessage + "\n" + send[i]
        
        #Seteamos texto y mostramos dialog
        self.dialog.label_response.setPlainText(dialogMessage)
        self.dialog.show()
    
    def checkFields(self, origin, destination, from_, to, subject, msg):
        'Comprueba que campos esenciales no sean nulos'

        return self == "" or origin == "" or destination == "" or from_ == "" or to == "" or subject == "" or msg == ""
    
    def createDialog(self):
        'Generar dialogo de error'

        self.dialog = Dialog()
        self.dialog.label_response.setPlainText("Debe rellenar todos los campos")
        self.dialog.show()

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/dialog.ui", self)
        self.button_accept.clicked.connect(self.onClickOk)

    def onClickOk(self):
        'Cerrar ventana de dialogo'

        self.close()

class MailBox(QtWidgets.QMainWindow):
    def __init__(self, user, password):
        super().__init__()
        uic.loadUi("ui/mailbox.ui", self)

        #Eventos buttons
        self.button_sync.clicked.connect(lambda:self.onClickButtonCheck(user, password))
        self.button_delete_mail.clicked.connect(lambda:self.deleteMessages(user, password))
        self.button_read_mail.clicked.connect(lambda:self.viewMessage(user, password))

    def onClickButtonCheck(self, user, password):
        host = self.input_to_host.text()
        self.syncList(user, password, host)
        
    def syncList(self, user, password, host):
        'Lista mails seteando la response en label list de ui'

        print(host, "from synclist")
        response = pop.list_mails(user, password, host)
        self.label_list.setPlainText(response)
    
 
    def deleteMessages(self, user, password):
        'Setea host, id, eliminar n correos y setea las responses como mensaje de dialogo ui'
        
        host = self.input_to_host.text()
        id = self.input_id_mail.text()
        response = pop.delete_mail(user, password, id, host)

        dialogMessage = ""
        self.dialog = Dialog()

        for i in range(len(response)):
            dialogMessage = dialogMessage + "\n" + response[i]
        
        self.dialog.label_response.setPlainText(dialogMessage)
        self.dialog.show()

    def viewMessage(self, user, password):
        'Set host, id y lista de mensajes en la ui'

        host = self.input_to_host.text()
        id = self.input_id_mail.text()
        response = pop.get_mails(user, password, id, host)
        message = ""
        
        for i in range(len(response)):
            message = message + "\n" + response[i]

        self.label_list.setPlainText(message)

app = QtWidgets.QApplication(sys.argv)
win = Login()
win.show()
app.exec_()
