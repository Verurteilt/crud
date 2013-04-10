from hashlib import md5
from hashlib import sha1
import time
import lepl.apps.rfc3696
from errors import MyException
import redis


class CRUD ():
        def __init__(self):
                ## Initialize redis
                self.crud = redis.Redis("localhost", db="crud", password="kaliman14")
                self.plain = redis.Redis("localhost", db="password", password="kaliman14")

        def create(self, user, password, email):
                self.user_create = user
                self.password_create = password
                self.email = email
                self.email_validator = lepl.apps.rfc3696.Email()
                self.keys = self.crud.keys('*')
                self.emails = {}
                self.email_existe = False
                self.error = "Ya existe un usuario con ese nombre o email"
                if self.user_create != "" and self.password_create != "" and self.email_validator(self.email) is True:
                    self.md5 = md5(self.password_create).hexdigest()
                    self.sha1 = sha1(self.password_create).hexdigest()
                    self.password_encriptada = self.md5 + self.sha1
                    for add_email in self.keys:
                        self.emails[add_email] = self.crud.hget(add_email, 'email')
                    for comp_email in self.emails.values():
                        if self.email == comp_email:
                            self.email_existe = True
                    if self.crud.hexists(self.user_create, 'name') is True or self.email_existe is True:
                        raise MyException("Error! Ya existe un usuario asi!")
                    else:
                        try:
                            self.crud.hset(self.user_create, 'name', self.user_create)
                            self.crud.hset(self.user_create, 'password_encriptada', self.password_encriptada)
                            self.crud.hset(self.user_create, 'email', self.email)
                            self.crud.hset(self.user_create, 'created_at', time.strftime('%Y-%m-%d %H:%M'))
                            self.crud.hset(self.user_create, 'updated_at', time.strftime('%Y-%m-%d %H:%M'))
                            self.plain.hset(self.user_create, 'name_plain', self.user_create)
                            self.plain.hset(self.user_create, 'password', self.password_create)
                            print("Successful")
                        except AttributeError:
                            self.crud.hdel(self.user_create, 'name', self.user_create)
                            self.crud.hdel(self.user_create, 'password_encriptada', self.password_encriptada)
                            self.crud.hdel(self.user_create, 'email', self.email)
                            self.crud.hdel(self.user_create, 'created_at', time.strftime('%Y-%m-%d %H:%M'))
                            self.crud.hdel(self.user_create, 'updated_at', time.strftime('%Y-%m-%d %H:%M'))
                            self.plain.hdel(self.user_create, 'name_plain', self.user_create)
                            self.plain.hdel(self.user_create, 'password', self.password_create)
                            raise AttributeError
                else:
                    raise MyException("Error EmptyString")

        def update(self, user, password="", email=""):
            self.user = user
            self.password_update = password
            self.email_update = email
            self.password_update_md5 = md5(self.password_update).hexdigest()
            self.password_update_sha1 = sha1(self.password_update).hexdigest()
            if self.user != "" and self.crud.hget(self.user, 'name') is not None:
                if self.password_update != "":
                    self.crud.hset(self.user, 'password_encriptada', self.password_update_md5+self.password_update_sha1)
                    self.plain.hset(self.user, 'password', self.password_update)
                    self.crud.hset(self.user, 'updated_at', time.strftime('%Y-%m-%d %H:%M'))
                else:
                    pass
                if self.email_update != "":
                    self.crud.hset(self.user, 'email', self.email_update)
                else:
                    pass
            else:
                raise MyException("Error that user does not exit")

        def read(self, user=""):
            self.keys_read = self.crud.keys('*')
            self.keys_readed = {}
            for x in self.keys_read:
                self.keys_readed['name_'+self.crud.hget(x, 'name')] = self.crud.hget(x, 'name')
            return self.keys_readed

        def read_only(self, user=""):
            self.user_only = user
            if self.user_only != "" and self.user_only.isdigit() is False:
                self.name_only = self.crud.hget(self.user_only, 'name')
                self.email_only = self.crud.hget(self.user_only, 'email')
                self.created_at_only = self.crud.hget(self.user_only, 'created_at')
                self.updated_at_only = self.crud.hget(self.user_only, 'updated_at')
                self.lista = list()
                self.lista.append(self.name_only)
                self.lista.append(self.email_only)
                self.lista.append(self.created_at_only)
                self.lista.append(self.updated_at_only)

            else:
                raise MyException("Error EmptyString or User is a Digit")
            return self.lista

        def delete(self, user=""):
            self.user_del = user
            if self.user_del != "" and self.crud.hget(self.user_del, 'name') is not None:
                self.crud.delete(self.user_del)
            else:
                raise MyException("That user does not exist!")

        def login(self, user="", password=""):
            self.user_log = user
            self.password_log = password
            if (self.user_log and self.password_log) != "" and self.crud.hget(self.user_log, 'name') is not None:
                self.password_status = md5(self.password_log).hexdigest() + sha1(self.password_log).hexdigest()
                if self.password_status == self.crud.hget(self.user_log, 'password_encriptada'):
                    return True
                else:
                    raise MyException("Wrong password!")
            else:
                raise MyException("That users does not exist!")
