#-*-coding:utf8;-*-
#qpy:2
#qpy:kivy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from mbedRPC import *
import androidhelper

class CommandScreen(GridLayout):
    def __init__(self, **kwargs):
        super(CommandScreen, self).__init__(**kwargs)
        self.cols = 2
        self.row = 2
        self.row_force_default=True
        self.row_default_height=200
        
        self.add_widget(Label(text='Device IP'))
        self.m_text_device_ip = TextInput(multiline=False,text="192.168.18.121")
        self.add_widget(self.m_text_device_ip)
        
        self.m_button_init = Button(text="Init")
        self.m_button_init.bind(on_press=self.mbedInit)
        self.add_widget(self.m_button_init)
        
        self.m_button_GetTemp = Button(text="Get Temp")
        self.m_button_GetTemp.bind(on_press=self.GetTemp)
        self.add_widget(self.m_button_GetTemp)
        
        self.btn_onLed1 = Button(text="Turn On",background_color=(1,0,0,1))
        self.btn_onLed1.bind(on_press=self.TurnOnLed1)
        self.add_widget(self.btn_onLed1)
        
        self.btn_offLed1 = Button(text="Turn Off",background_color=(1,0,0,1))
        self.btn_offLed1.bind(on_press=self.TurnOffLed1)
        self.add_widget(self.btn_offLed1)
        
        self.btn_onLed2 = Button(text="Turn On",background_color=(0,1,0,1))
        self.btn_onLed2.bind(on_press=self.TurnOnLed2)
        self.add_widget(self.btn_onLed2)
        
        self.btn_offLed2 = Button(text="Turn Off",background_color=(0,1,0,1))
        self.btn_offLed2.bind(on_press=self.TurnOffLed2)
        self.add_widget(self.btn_offLed2)

        self.btn_onLed3 = Button(text="Turn On",background_color=(0,0,1,1))
        self.btn_onLed3.bind(on_press=self.TurnOnLed3)
        self.add_widget(self.btn_onLed3)
        
        self.btn_offLed3 = Button(text="Turn Off",background_color=(0,0,1,1))
        self.btn_offLed3.bind(on_press=self.TurnOffLed3)
        self.add_widget(self.btn_offLed3)

        self.btn_getLedStatus = Button(text="LED Status")
        self.btn_getLedStatus.bind(on_press=self.GetLedStatus)
        self.add_widget(self.btn_getLedStatus)
        
        self.btn_getA0Status = Button(text="Get A0 Status")
        self.btn_getA0Status.bind(on_press=self.GetA0Status)
        self.add_widget(self.btn_getA0Status)
        

    def mbedInit(self,event):
        self.droid = androidhelper.Android()
        
        self.mbed = HTTPRPC(self.m_text_device_ip.text)
        self.led1 = DigitalOut(self.mbed,"led1")
        self.led2 = DigitalOut(self.mbed,"led2")
        self.led3 = DigitalOut(self.mbed,"led3")
        self.temp_humidity = RPCFunction(self.mbed,"Temp_and_Humidity_Finder")

        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text='Init Complete'))
        button_close = Button(text='Close me!')
        box.add_widget(button_close)

        popup = Popup(title='message', content=box,
                      size_hint=(None,None),size=(400,400), auto_dismiss=False)

        button_close.bind(on_press=popup.dismiss)
        popup.open()
        
        
    def GetTemp(self,event):
        resp = self.temp_humidity.run("")
        self.droid.ttsSpeak(resp)

    def TurnOnLed1(self,event):
        self.led1.write(1)
        
    def TurnOffLed1(self,event):
        self.led1.write(0)
        
    def TurnOnLed2(self,event):
        self.led2.write(1)
        
    def TurnOffLed2(self,event):
        self.led2.write(0)

    def TurnOnLed3(self,event):
        self.led3.write(1)
        
    def TurnOffLed3(self,event):
        self.led3.write(0)
         
    def GetLedStatus(self,event):
        if( self.led1.read()[0] == '1' ): self.droid.ttsSpeak("Turn on red.")
        if( self.led2.read()[0] == '1' ): self.droid.ttsSpeak("Turn on green.")
        if( self.led3.read()[0] == '1' ): self.droid.ttsSpeak("Turn on blue.")
        
    def GetA0Status(self,event):
        print ''

class MyApp(App):
    def build(self):
        return CommandScreen()        

if __name__ == '__main__':
    MyApp().run()