
from kivy import Logger
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
#import logging
#logging.Logger.manager.root = Logger
#Window.fullscreen = True

from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        self.factory.app.handle_message(data)

class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    label = None

    def build(self):
        self.label = Label(text="")
        reactor.listenTCP(8000, EchoServerFactory(self))
        return self.label

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.label.text = f"{msg}"
        return


if __name__ == '__main__':
    TwistedServerApp().run()





class MyApp(App):
    denied_lbl= ''
    def build(self):
        # creating Floatlayout
        layout = FloatLayout()

        self.denied_lbl = Label(text='Denied',
                    size_hint=(0.4, 0.2),
                    pos_hint={'x': .3, 'y': .7},
                           color=(0,0,1,1))


        # adding button widget
        layout.add_widget(self.denied_lbl)

        '''layout = GridLayout(cols=2)
        layout.add_widget(Button(text='Hello 1'))
        layout.add_widget(Button(text='World 1'))
        layout.add_widget(Button(text='Hello 2'))
        layout.add_widget(Button(text='World 2'))'''

        return layout

    def update(self, *args):
        print('hgfhgf')
        self.denied_lbl.text = 'hello'

if __name__ == '__main__':
    TwistedServerApp().run()
