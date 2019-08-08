#!/usr/bin/python

# -*- coding: utf-8 -*-

import sys #importa o modulo sys

reload(sys)

sys.setdefaultencoding('utf-8')

from gtts import gTTS # importamos o modúlo gTTS

import os

import mysql.connector #importa o modulo mysql conector

from asterisk.agi import * #entendo que aqui importa o  asterisk

agi = AGI() #agi

agi.verbose("python agi started") #vai mandar la para o console

Quantidade = agi.get_variable('QUANTIDADE') #captura a variavel

mydb = mysql.connector.connect(host="127.0.0.1",user="root",passwd="", database="produtos")

mycursor = mydb.cursor()

mycursor.execute("SELECT nome FROM produtos where codigo = %s" % Quantidade)

myresult = mycursor.fetchall()

d = [[s.encode('ascii') for s in list] for list in myresult] #transforma a  lista da consulta no banco em string

d = str(d).strip('[]') # retira os colchetes da string

mycursor.execute("SELECT valor FROM produtos where codigo = %s" % Quantidade)

myresult1 = mycursor.fetchall()

e = [tuple(str(item) for item in t) for t in myresult1] #transforma a tupla em uma lista

e = [[s.encode('ascii') for s in list] for list in e] #transforma a lista em uma string

e = str(e).strip('[]')

voz = gTTS("o preço do "+d+"eh de"+e+"reais", lang ="pt") #faz a conversão de voz em dados

voz.save("voz.mp3") #salvamos com o comando save em mp3

os.system("sox voz.mp3 -r 8000 -c1 voz.gsm") #codifica o audio

os.system("cp voz.gsm /var/lib/asterisk/sounds/en")# #salva na pasta sound
