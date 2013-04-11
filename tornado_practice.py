import tornado.web
import CRUD
global x
x = CRUD.CRUD()

#To generate the cookie use this
#import base64
#import uuid
#print base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


class INDEX(tornado.web.RequestHandler):
        def get_current_user(self):
            return self.get_secure_cookie("user")

        def get(self):
            users = x.read()
            logeado = False
            if len(users) is 0:
                users = None
            if self.current_user:
                logeado = True
            self.render('templates/index.html', users=users, logeado = logeado, ul = self.current_user)


class CREATE(tornado.web.RequestHandler):

    def get_current_user(self):
                return self.get_secure_cookie("user")

    def get(self):
        if self.current_user:
            return self.redirect("/")
        self.render('templates/create.html')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        email = self.get_argument("email")
        try:
            x.create(username, password, email)
            self.write("Muy bien, creado :D <a href='/'>Inicio</a>")
        except:
            raise Exception(x.create(username, password, email))


class UPDATE(tornado.web.RequestHandler):
    def get_current_user(self):
            return self.get_secure_cookie("user")

    def get(self, username):
        username = username
        if self.current_user == username:
                pass
        else:
            self.redirect("/")
        self.render('templates/update.html', username=username)

    def post(self, *args):
        password = self.get_argument("password")
        email = self.get_argument("email")
        try:
            x.update(self.current_user, password, email)
            self.write("Muy bien, actualizado :D <a href='/'>Inicio</a>")
        except:
            raise Exception(x.update(username, password, email))


class READONLY(tornado.web.RequestHandler):
    def get(self, user_name):
        self.user = x.read_only(user=user_name)
        self.name = self.user[0]
        self.email = self.user[1]
        self.created_at = self.user[2]
        self.updated_at = self.user[3]
        if self.user[0] is None:
            self.vacio = True
        else:
            self.vacio = False
        self.render("templates/perfil.html", name=self.name, email=self.email, creado=self.created_at, actualizado=self.updated_at, vacio=self.vacio)


class DELETE(tornado.web.RequestHandler):
    def get_current_user(self):
            return self.get_secure_cookie("user")

    def get(self, username):
        try:
            username = username
            if self.current_user == username:
                x.delete(username)
                self.write("Usuario Borrado!")
                self.clear_cookie("user")
            else:
                self.redirect("/")
        except:
            raise Exception(x.delete(username))


class LOGIN(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        if self.current_user:
            self.redirect("/read_only/"+self.current_user)
        self.render("templates/login.html")

    def post(self):
        if x.login(self.get_argument("username"), self.get_argument("password")):
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect("/read_only/"+self.current_user)

        else:
            raise Exception(x.login(self.get_argument("username"), self.get_argument("password")))

class LOGOUT(tornado.web.RequestHandler):
    def get_current_user(self):
            return self.get_secure_cookie("user")

    def get(self):
        if self.current_user:
            self.write("Logout listo puedes volver a logearte aqui <a href='/login'>Login</a>")
            return self.clear_cookie("user")
        else:
            self.redirect("/login")


application = tornado.web.Application([
        (r"/", INDEX),
        (r"/create", CREATE),
        (r"/update/([A-z0-9]+)", UPDATE),
        (r"/read_only/([A-z0-9]+)", READONLY),
        (r"/delete/([A-z0-9]+)", DELETE),
        (r"/login", LOGIN),
        (r"/logout", LOGOUT), ],
        debug=True, cookie_secret="CqmtCmLvSkSDJ+UnDPW7Wj0fj2IKzUobpY/SFXec7Yg=")

if __name__ == '__main__':
        PORT = 8000
        try:
            application.listen(PORT)
        except:
            PORT += 110
            application.listen(PORT)
        print "Running in localhost on PORT:"+str(PORT)
        tornado.ioloop.IOLoop.instance().start()
