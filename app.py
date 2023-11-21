import subprocess
import entrance_login_verification
import uuid

class data:
    def __init__(self,email,password,token,collection):
        self.email = email
        self.password = password
        self.token = token
        self.collection = collection




class app:
    def __init__(self):
        self.data = ""


    def menu_1(self):
        print("Bienvenido a la face_recognition")
        print("1.Ingresar")
        print("2.Cerrar Programa")
        opt = int(input("ingrese una opcion: "))
        if opt == 1:
            self.ingresar()
        elif opt == 2:
            return opt

    def menu_2(self):
        print("1.Iniciar Programa")
        print("2.Registrar un nuevo usuario")
        print("3.Cerrar Sesion")
        opt = int(input("Ingrese una opcion: "))
        
        if opt == 1:
            subprocess.run(['python3','infrarrojo_camera_connection.py'])
            self.menu_2()
        elif opt == 2:
            print("Registro")
            correo_user = input("Ingresar correo de la institucion: ")
            codigo_user = input("Ingresar codigo de la institucion: ")
            print("Preparado para tomar la foto, mira direcctamente a la camara")
            jaja = input("Preparado?: ")
            subprocess.run(['python3','upload_face_camera.py','--email',correo_user,'--code',codigo_user,'--collection',self.data.collection])
            self.menu_2()
        elif opt == 3:
            entrance_login_verification.set_default_values()
            self.menu_1()

    def ingresar(self):
        correo = input("Ingrese su correo: ")
        password = input("Ingrese password: ")
        token = input("Ingrese token: ")
        uuid = input("uuid : ")
        #generar un uuid y manejarlo desde lambda
        entrance_login_verification.login_admin(correo,password,token,uuid)
        access_n_collection = entrance_login_verification.update_accepted_wait_entrance(uuid)  
        collection = ""
        if access_n_collection[0] == True:
            collection = access_n_collection[1]
            self.data = data(correo,password,token,collection)
            self.menu_2()
        else:
            print("Usted no esta registrado")
            self.menu_1()



    def system(self):
            opt = self.menu_1()
    

    
instance = app()
instance.system()
