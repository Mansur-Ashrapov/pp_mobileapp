from kivy.uix.screenmanager import Screen 
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2


class CameraScreen(Screen):
    def switch_buttons(self, b = False):
        self.ids.capture_button.disabled = b
        self.ids.capture_button.opacity = 1 if b is False else 0
        self.ids.repeat_button.disabled = b is False
        self.ids.repeat_button.opacity = 1 if b else 0
        self.ids.results_button.disabled = b is False
        self.ids.results_button.opacity = 1 if b else 0

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.cap = True
        self.capturing = Clock.schedule_interval(self.update_camera, 1.0 / 16.0) 
        self.switch_buttons()

    def update_camera(self, dt):
        if self.cap:
            ret, frame = self.capture.read()
            if ret:
                buf = cv2.flip(frame, 0).tobytes()
                # TODO: frame = recognize_test(frame)
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.ids.image.texture = texture

    def capture_image(self):
        self.cap = False 
        self.capturing.cancel()
        self.capture.release()
        self.switch_buttons(True)

    def repeat_process(self):
        self.cap = True
        self.capture = cv2.VideoCapture(0)
        self.capturing = Clock.schedule_interval(self.update_camera, 1.0 / 24.0) 
        self.switch_buttons()

    def send_results(self, *args):
        self.dialog.dismiss()
        # TODO: send result to api
        self.manager.current = "home_screen"

    def show_results(self):
        self.dialog = MDDialog(
            text="Ваш кадр успешно снят. Вы можете его сохранить.",
            buttons=[
                MDRaisedButton(
                    text="Закрыть",
                    on_release=self.close_dialog,
                ),
                MDRaisedButton(
                    text="Отправить",
                    on_release=self.send_results,
                )
            ]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()