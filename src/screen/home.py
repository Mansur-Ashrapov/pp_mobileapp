
from kivy.uix.screenmanager import Screen 


class HomeScreen(Screen):
    # TODO: get tests and classes api

    # TODO: Добавить меню выбора класса и теста

    def button1_action(self):
        print("Действие кнопки 1")

    def button2_action(self):
        print("Действие кнопки 2")

    def show_camera(self):
        self.manager.current = "camera_screen"
