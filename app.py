#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPalette 
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtCore
from datetime import datetime
from langid.langid import set_languages
import sys
import json
import langid

 
set_languages(langs=['ru', 'en'])

  
class Window(QWidget):

    def __init__(self): 
        super().__init__() 
        
        self.setWindowTitle("Geometry") 
        self.setGeometry(100, 60, 500, 300)
        
        self.in_str = ''
        self.flag_stop_while = 0
        self.flag_crammer_mode = 0
        self.check_crammer_mode_key = ''
        self.check_crammer_mode_value = ''
         
        self.lbl = QLabel(self)
        self.qle = QLineEdit(self)
        self.btn = QPushButton('crammer', self)
        self.qle.setStyleSheet("background:gray;")
        
        self.qle.textChanged[str].connect(self.search)
        self.btn.clicked.connect(self.crammer_mode)
        
        qp = QPalette()
        qp.setColor(QPalette.ButtonText, Qt.black)
        qp.setColor(QPalette.Window, Qt.darkGray)
        qp.setColor(QPalette.Button, Qt.darkGray)
        self.setPalette(qp)
        
        self.vb = QVBoxLayout(self)
        self.vb.addWidget(self.lbl)
        self.vb.addWidget(self.qle)
        self.vb.addWidget(self.btn)
        
        self.di_ten = {}
        self.di_forty= {}
        self.count = 0
        
        with open("data.json") as data:
            self.di_ten = json.load(data)
           
        if len(self.di_ten) == 10:
            self.crammer_mode(self)
            
            
    def crammer_mode(self, text):
    
       self.flag_crammer_mode = 1
       
       for key in self.di_ten:
           
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
    
        en_list = []
        ru_list = []
        in_list = text.split(' ')
        
        if not text:

            self.lbl.setText('NONE')
            return None
            
        
        for word in in_list:
        
            ch, coal = langid.classify(word)
        
            if ch == 'en' and word !='' and word != ' ':
        
                en_list.append(word)
        
            elif ch == 'ru':
        
                ru_list.append(word)
                
        if len(en_list) > 1 or '-' in text:
            
            str_en = ' '.join(str(e) for e in en_list)
            str_ru = ' '.join(str(e) for e in ru_list)
            self.di_ten[str_en]:[] = str_ru, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        
        else:
        
            str_en = ''.join(en_list)
            str_en.strip(' ')
            str_ru = ', '.join(str(e) for e in ru_list)
            self.di_ten[str_en]:[] = str_ru, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        
        if len(self.di_ten) == 10:
            self.crammer_mode(self)
    
        
    def search(self, text):
        
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
            
        if self.flag_crammer_mode == 0 and e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            
            self.write(self.in_str)
            with open("data.json", "w") as data:
                json.dump(self.di_ten, data, ensure_ascii=False, indent=2)
                       
        elif e.key() == Qt.Key_Escape:
            
            sys.exit(App.exec_())
        
        else:
        
            pass                        
                                
    
    def closeEvent(self, event):
        
        with open("data.json", "w") as data:
            
            json.dump(self.di_ten, data, ensure_ascii=False, indent=2)
            
if __name__ == "__main__":        
 
    App = QApplication(sys.argv)    
    window = Window()
    window.show() 
    sys.exit(App.exec_())
  
