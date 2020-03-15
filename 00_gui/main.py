# -*- coding: utf-8 -*-
"""

Filename: main.py

Author:   Ednalyn C. De Dios
Phone:    (210) 236-2685
Email:    ednalyn.dedios@taskus.com 

Created:  March 13, 2020
Updated:  March 14, 2020

PURPOSE: conduct nlp on a one-column flat file.

PREREQUISITES: list any prerequisites or
assumptions here.

DON'T FORGET TO:
1. Hydrate.
2. Sleep.
3. Have fun!

"""

# import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty



class MyGrid(Widget):

    def __init__(self, **kwargs): 
  
        # The super() builtin 
        # returns a proxy object that 
        # allows you to refer parent class by 'super'.  
        super(MyGrid, self).__init__(**kwargs)

    def btn_close(self):
        App.get_running_app().stop()



class PathButton(Button):
    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()
        return(filedialog.askopenfilename())



class PlaylistApp(App):
    def build(self):
        return MyGrid()


if __name__ == '__main__':
    PlaylistApp().run()