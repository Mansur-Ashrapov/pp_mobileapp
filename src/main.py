import kivy
from kivymd.app import MDApp
from kivy.lang import Builder

from screen import (
    LoginScreen,
    HomeScreen,
    CameraScreen
)

kivy.require('2.0.0')


class MyApp(MDApp):
    def build(self):
        self.root = Builder.load_file("main.kv")
        self.root.add_widget(LoginScreen(name="login_screen"))
        self.root.add_widget(HomeScreen(name="home_screen"))
        self.root.add_widget(CameraScreen(name="camera_screen"))
        
        self.root.current = "camera_screen"

        return self.root

if __name__ == "__main__":
    MyApp().run()