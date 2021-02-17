#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPalette 
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtCore
from datetime import datetime
from langid.langid import set_languages                        # to determine the input language 
import sys
import json
import langid                                                  # to determine the input language 

 
set_languages(langs=['ru', 'en'])                              # list of defined languages 

  
class Window(QWidget):

    def __init__(self): 
        super().__init__() 
        
        self.setWindowTitle("Geometry")                        # window creation 
        self.setGeometry(100, 60, 500, 300)
        
        self.in_str = ''                                       # string for storing input data
        self.flag_stop_while = 0                               # XXX algorithm under development XXX
        self.flag_crammer_mode = 0                             # flag for handling input
        self.check_crammer_mode_key = ''                       # XXX algorithm under development XXX
        self.check_crammer_mode_value = ''                     # XXX algorithm under development XXX
         
        self.lbl = QLabel(self)                                # field for displaying text 
        self.qle = QLineEdit(self)                             # field to enter text 
        self.btn = QPushButton('crammer', self)                # crammer mode button 
        self.qle.setStyleSheet("background:gray;")
        
        self.qle.textChanged[str].connect(self.search)         # when changing in the text input field, call the search function       
        self.btn.clicked.connect(self.crammer_mode)            # when clicking on the button, we call the crammer_mode function 
        
        qp = QPalette()
        qp.setColor(QPalette.ButtonText, Qt.black)
        qp.setColor(QPalette.Window, Qt.darkGray)
        qp.setColor(QPalette.Button, Qt.darkGray)
        self.setPalette(qp)
        
        self.vb = QVBoxLayout(self)
        self.vb.addWidget(self.lbl)
        self.vb.addWidget(self.qle)
        self.vb.addWidget(self.btn)
        
        self.di_ten = {}                                       # dictionary for writing 10 values   
        self.di_forty= {}                                      # dictionary for writing 40 values ( not yet implemented )
        self.count = 0
        
        with open("data.json") as data:                        # open json file
            self.di_ten = json.load(data)                      # save the content to the dictionary 
           
        if len(self.di_ten) == 10:                             # if there are 10 values in the dictionary, 
            self.crammer_mode(self)                            #  start the cramming mode
            
            
    def crammer_mode(self, text):
     '''
     XXX algorithm under development XXX         
     '''
    
       self.flag_crammer_mode = 1                              # flag for handling input 
       
       for key in self.di_ten:                                 # this is nonsense, it doesn't work  XXX algorithm under development XXX
           
           self.list_value = [element.strip(", ") for element in self.di_ten[key][0].split(",")]
           start_len_value = len(self.list_value)
           len_value = 0
           print('len - ', start_len_value)
           print('list_value - ', self.list_value)
           self.check_crammer_mode = key
           out_str = 'examine:   ' + key + '   ----------------------------   ' + str(len_value) + '/' + str(start_len_value)
           self.lbl.setText(out_str)
          # while self.flag_stop_while == 0:
           #    pass
       
       self.flag_crammer_mode = 0
        
    def write(self, text):
     '''
     writes input to a dictionary 
     '''
    
        en_list = []                                            # create a list to handle English input 
        ru_list = []                                            # create a list for processing Russian input  
        in_list = text.split(' ')                               # list for input string 
        
        if not text:                                            

            self.lbl.setText('NONE')                           
            return None
            
        
        for word in in_list:                                    # we iterate over the entered words
        
            ch, coal = langid.classify(word)                    # ch stores the language of the word 
        
            if ch == 'en' and word !='' and word != ' ':        # if the word is in english
        
                en_list.append(word)                            # add to the list for English words 
        
            elif ch == 'ru':                                    # if the word is in Russian 
        
                ru_list.append(word)                            # add to the list for Russian words
                
        if len(en_list) > 1 or '-' in text:                     # if in English not one word, but a phrase or a complex word with a hyphen 
            
            str_en = ' '.join(str(e) for e in en_list)
            str_ru = ' '.join(str(e) for e in ru_list)
            self.di_ten[str_en]:[] = str_ru, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())    # date added to the list of dictionary values 
                                                                                                for possible further sorting 

        
        else:                                                   
        
            str_en = ''.join(en_list)
            str_en.strip(' ')
            str_ru = ', '.join(str(e) for e in ru_list)
            self.di_ten[str_en]:[] = str_ru, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        
        if len(self.di_ten) == 10:                              
            self.crammer_mode(self)
    
        
    def search(self, text):
     '''
     looks for the input string in the 
     dictionary keys when the crammer mode 
     is on, or in values when it is off 
     '''
        
        self.in_str = text
        
        if self.flag_crammer_mode == 0:

            if self.di_ten.get(text):
        
                self.lbl.setText(text + ' : ' + self.di_ten[text][0])

            else:
        
                self.lbl.setText('NONE')          
        
        else:

            if text in self.list_value:
                print('yahooo')
                self.flag_stop_while = 1                
    
    def keyPressEvent(self, e):
     '''
     keyboard press event handler 
     '''
            
        if self.flag_crammer_mode == 0 and e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:   # if the pressed key is one of the enterters 
                                                                                                    and the crammer mode is not active 
            
            self.write(self.in_str)                                                               # write the entered values into the dictionary 
            with open("data.json", "w") as data:                                                  # the dictionary is written to a file 
                json.dump(self.di_ten, data, ensure_ascii=False, indent=2)
                       
        elif e.key() == Qt.Key_Escape:
            
            sys.exit(App.exec_())
        
        else:               # to be able to add hotkeys 
        
            pass                        
                                
    
    def closeEvent(self, event):
     '''
     when the program is closed, the dictionary is saved to a file 
     '''
        
        with open("data.json", "w") as data:
            
            json.dump(self.di_ten, data, ensure_ascii=False, indent=2)
            
if __name__ == "__main__":        
 
    App = QApplication(sys.argv)    
    window = Window()
    window.show() 
    sys.exit(App.exec_())                                     # when you press escape the window is closed 
  
