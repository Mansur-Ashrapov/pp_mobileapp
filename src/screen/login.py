
from kivy.uix.screenmanager import Screen 


class LoginScreen(Screen):
    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        # TODO: Login api
        if username == 'user' and password == 'pass':
            self.manager.current = "home_screen"
        else:
            self.ids.login_status.text = "Неверные данные"


