from threading import Timer

# import logging
from kivy import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

# logging.Logger.manager.root = Logger
Builder.load_file('layout.kv')

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol

# Window.fullscreen = True
Window.clearcolor = (1, 1, 1, 1)


class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        self.factory.app.handle_message(data)


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


# Sensor Access Gate Layout (Design taken from .kv file)
class SAGateLayout(BoxLayout):
    pass


class TwistedServerApp(App):
    label = None
    image = None

    def build(self):
        '''layout = FloatLayout()
        self.label = Label(text="Please present your \ncard to the reader", font_size='64dp', pos_hint={'right': 1, 'top': 0.8})
        self.label.color = (0, 0, 0, 1)
        layout.add_widget(self.label)
        self.image = Image(source='Securitas_AB_logo.png', size_hint=(0.5, 0.5),
                           pos_hint={'right': 0.75, 'top': 1})
        layout.add_widget(self.image)'''
        reactor.listenTCP(8000, EchoServerFactory(self))
        self.layout = SAGateLayout()
        return self.layout

    def clear_screen(self):
        Logger.info("Clear Screen")
        self.layout.ids['img1'].source = "Securitas_AB_logo.png"
        self.layout.ids['lbl1'].text = "Please present your \ncard to the reader"
        self.layout.ids['lbl1'].color = (0, 0, 0, 1)
        return

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        msg = msg.split('|', 2)
        if len(msg) > 1:
            Logger.info(msg[0])
            if msg[0] == '0':
                Logger.info("image 0")
                self.layout.ids['img1'].source = 'spot-check.png'
                self.layout.ids['lbl1'].color = (1, 0, 0, 1)  # Red
                #Clock.schedule_once(self.clear_screen, 10)
                t = Timer(5.0, self.clear_screen)
                t.start()
            else:
                Logger.info("image other")
                self.layout.ids['img1'].source = 'green_check.png'
                self.layout.ids['lbl1'].color = (0, 1, 0, 1)  # Green
                t = Timer(15.0, self.clear_screen)
                t.start()

            self.layout.ids['lbl1'].text = f"{msg[1]}"
        else:
            print(self.layout.ids)
            self.layout.ids['lbl1'].text = f"{msg[0]}"

        return


if __name__ == '__main__':
    TwistedServerApp().run()
