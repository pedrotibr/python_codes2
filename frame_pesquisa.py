#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:22:31 2018

@author: pmesquital
"""


import sys

import os


import wx
import MySQLdb

import frame_cadastro

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, A4, portrait

import calendario


 
def create(parent):
    return Frame2(parent)
 
class Frame2(wx.Frame):
    def __init__(self, prnt):
        
        wx.Frame.__init__(self,id=-1, parent=prnt, title='Consulta',style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        
        self.panel = wx.Panel(self, id=-1)

        
        self.choices=['']
        
        
        self.lbl_data=wx.StaticText(self.panel, pos=(10,40), label='Data:', size=(50,70))
        self.edit_data=wx.TextCtrl(self.panel, pos=(100,30), size=(100,25))
        
        self.edit_data.Bind(wx.EVT_LEFT_UP, self.frame_calendario)
        
 
        self.lbl_alterar_data=wx.StaticText(self.panel, pos=(220,30), label='Nova data agendamento(s):', size=(110,40))
        self.edit_nova_data=wx.TextCtrl(self.panel, pos=(340,30), size=(100,25))
        self.edit_nova_data.Bind(wx.EVT_LEFT_UP, self.frame_calendario2)
        
        
    
        self.lbl_agendamentos=wx.StaticText(self.panel, pos=(10,80), label='Agenda:', size=(50,30))
        
        
        
        self.btn_pesquisar = wx.Button(self.panel, pos=(100,400), label='Pesquisar', size=(100,30))
        
        self.btn_editar = wx.Button(self.panel, pos=(210,400), label='Editar', size=(90,30))
        
        self.btn_ok = wx.Button(self.panel, pos=(450,30), label='Ok', size=(40,25))
        self.btn_ok.SetFocus()
        
        self.btn_imprimir = wx.Button(self.panel, pos=(310,400), label='imprimir', size=(100,30))
        
    
        self.listctrl1 = wx.ListCtrl(self.panel, pos=(100,70),size=(510,300), style = wx.LC_REPORT) 
        self.listctrl1.InsertColumn(0, 'Column1', wx.LIST_FORMAT_LEFT, 100) 
        self.listctrl1.InsertColumn(1, 'Column2', wx.LIST_FORMAT_LEFT, 100) 
        self.listctrl1.InsertColumn(2, 'Column3', wx.LIST_FORMAT_LEFT, 100) 
        self.listctrl1.InsertColumn(3, 'Column4', wx.LIST_FORMAT_LEFT, 100) 
 
        
        self.btn_pesquisar.Bind(wx.EVT_BUTTON, self.Onconsultar)
        
        self.btn_editar.Bind(wx.EVT_BUTTON, self.frame_cadastro)
        
       
        
        self.a1=""

       
        self.SetSize((700,500))

        self.Center()
        
        self.btn_pesquisar.Bind(wx.EVT_SET_FOCUS, self.set_date)
        
        self.edit_data.Bind(wx.EVT_KEY_DOWN, self.onKeyPress) 
        
        self.btn_ok.Bind(wx.EVT_BUTTON, self.OnSelected)
       
        
        self.btn_imprimir.Bind(wx.EVT_BUTTON, self.seleciona_tipo_impressao)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("./logo.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        
        self.calendario = None
        

    def seleciona_tipo_impressao(self,e):
        
        dialog = wx.MessageDialog(self,("Selecione o tipo de impressão:"),("Confirma"),
                                      wx.YES_NO | wx.ICON_QUESTION)
        
        dialog.SetYesNoLabels("&Paisagem", "&Retrato")
        
        confirma = dialog.ShowModal() == wx.ID_YES
        dialog.Destroy()
        
        if confirma:
            tipo = ("landscape")
            self.Onprint(self,tipo)
            
        if not confirma:
            tipo = ("portrait")
            self.Onprint(self,tipo)
        
 
    def OnSelected(self, evt):


        db=MySQLdb.connect(host="localhost",port=3306,user="user",passwd="password",db="database")
        cursor1 = db.cursor()
        
        nova_data=self.edit_nova_data.GetValue()

        dialog = wx.MessageDialog(self,("Confirmar alterar data dos registros selecionados?"),("Confirma"),
                                      wx.YES_NO | wx.ICON_QUESTION)
        confirma = dialog.ShowModal() == wx.ID_YES
        dialog.Destroy()
        
        if confirma:
                   

            item = self.listctrl1.GetFirstSelected() 

            print("item: "+str(item))
        
            self.confirma=1

            while item != -1:
                data = self.listctrl1.GetItem(item)
           
                sessoes = str(data.Text)
                
                data = self.listctrl1.GetItem(item, 0) 
            
                nome=str(data.Text)
                
                data = self.listctrl1.GetItem(item, 1) 
            
                data_=str(data.Text)
                
                data = self.listctrl1.GetItem(item, 2) 
             
                data_=str(data.Text)
                
                data = self.listctrl1.GetItem(item, 3) 
          
                heaa=str(data.Text)

             
        
                cursor1.execute('UPDATE TABLE1 SET data_agendamento = "'+nova_data+'" WHERE sessoes = %s and data_agendamento = %s and heaa = %s',[sessoes, data_, heaa])
                db.commit()
   
                item = self.listctrl1.GetNextSelected(item)
     

            self.Onconsultar_nova_data()
            
    def frame_calendario(self, event):
           
        if not self.calendario:    
            self.calendario = calendario.create(self)
            
      
        self.calendario.Bind(wx.EVT_CLOSE,self.set_date)
        
        self.calendario.Show(True)
   
        event.Skip      

     
    def set_date(self,e):

            
        x=str(self.calendario.data())
  
        self.edit_data.SetValue(x)

        self.calendario.Destroy()  
        
               
        
        
    def frame_calendario2(self, event):
           
        if not self.calendario:    
            self.calendario = calendario.create(self)
            
        
        self.calendario.Bind(wx.EVT_CLOSE,self.set_date2)
        
        self.calendario.Show(True)
   
        event.Skip      

     
    
    def set_date2(self,e):

            
        x=str(self.calendario.data())
  
  
        self.edit_nova_data.SetValue(x) 

        self.calendario.Destroy()
        
  
     
    def frame_calendario_btn_ok(self, event):
    
        self.btn_ok.SetFocus()     
    
        if not (self.calendario):
            
            self.calendario = calendario.create(self)
            
            
        self.calendario.Show(True)
              
        
        event.Skip  
      

      
    def get_mes(self, x):
    
        if x == "Jan":
            mes=("  janeiro")
            mes_int=1
        
        if x == "Feb":
            mes=(" fevereiro")
            mes_int=2
        
        if x == "Mar":
            mes=("  março")
            mes_int=3
        
        if x == "Apr":
            mes=("   abril")
            mes_int=4
        
        if x == "May":
            mes=("   maio")
            mes_int=5
        
        if x == "Jun":
            mes=("   junho")
            mes_int=6
        
        if x == "Jul":
            mes=("   julho")
            mes_int=7
        
        if x == "Aug":
            mes=("  agosto")
            mes_int=8
        
        if x == "Sep":
            mes=("setembro")
            print("setembro mês atual")
            mes_int=9
        
        if x == "Oct":
            mes=(" outubro")
            mes_int=10
        
        if x == "Nov":
            mes=("novembro")
            mes_int=11
        
        if x == "Dec":
            mes=("dezembro")
            mes_int=12
    
        print(mes_int)
        
        return (mes_int)
            
        
      
    def OnClose(self, event):
      
        self.Destroy() 
  
        
    def frame_cadastro(self, event):
      
        
        item = self.listctrl1.GetFirstSelected()
  
        self.confirma=1

        while item != -1:
            
            data = self.listctrl1.GetItem(item)
        
            sessoes = str(data.Text)
            
            data = self.listctrl1.GetItem(item, 1) 
          
            nome=str(data.Text)
            
            data = self.listctrl1.GetItem(item, 2) 
           
            data_=str(data.Text)
            
            data = self.listctrl1.GetItem(item, 3) 
            
            heaa=str(data.Text)
     
 
            item = self.listctrl1.GetNextSelected(item)
        
    
        self.Framew1 = frame_cadastro.create(self)
        
        self.Framew1.Show()
   
        self.Framew1.find_user_heaa(heaa)
        
        self.Framew1.combobox_qtd.Enable(False)
        
        self.Framew1.Onedit(self.Framew1)
        
        self.btn_ok.SetFocus()

    def onKeyPress(self, event):

        keycode = event.GetKeyCode()
        
        print (keycode)
                              
        if keycode == 13 :
     
            self.Onconsultar(self)
            
        
        event.Skip()
        
        
    def Onconsultar(self,e):
        
        db=MySQLdb.connect(host="localhost",port=3306,user="user",passwd="password",db="database")
        cursor = db.cursor()
        cursor2 = db.cursor()
  
        self.listctrl1.DeleteAllItems()        
        
        data = (self.edit_data.GetValue())
        
        numrows=cursor2.execute('select * from database.TABLE1 where data_agendamento like "%'+data+'%"')
        
        row=cursor2.fetchone()
        
        print (row)
                
        self.lista=[]
   
        
        for num in range (0, numrows):     
           
            heaa = (str(row[4]))
            
            crm = (str(row[3]))
            
            numrows=cursor.execute('select * from database.TABLE2 where HEAA like "%'+heaa+'%"')
            row2=cursor.fetchone()

            print(row2)
           
            
            self.listctrl1.InsertItem(num, row[0])
       
            
            self.listctrl1.SetItem(num, 0, (str(row[2])))
            self.listctrl1.SetItem(num, 1, (str(row2[1])))
            self.listctrl1.SetItem(num, 2, (str(row[1])))
            self.listctrl1.SetItem(num, 3, (str(row[4])))

            row=cursor2.fetchone()



    def Onconsultar_nova_data(self):

        db=MySQLdb.connect(host="localhost",port=3306,user="user",passwd="password",db="database")
        cursor = db.cursor()
        cursor2 = db.cursor()
        
        self.listctrl1.DeleteAllItems()
                
        data = (self.edit_nova_data.GetValue())
        
        numrows=cursor2.execute('select * from database.TABLE1 where data_agendamento like "%'+data+'%"')
        
        row=cursor2.fetchone()
        
        print (row)
                
        self.lista=[]

        
        for num in range (0, numrows):   
           
            heaa = (str(row[4]))
            
            crm = (str(row[3]))
            
            numrows=cursor.execute('select * from database.TABLE2 where HEAA = %s',[heaa])
            row2=cursor.fetchone()
            
            
            
            numrows=cursor.execute('select * from database.TABLE3 where CRM = %s',[crm])
            row3=cursor.fetchone()
            
    
            self.listctrl1.InsertStringItem(num, row[0])
          
            
            self.listctrl1.SetStringItem(num, 0, (str(row[2])))
            self.listctrl1.SetStringItem(num, 1, (str(row2[1])))
            self.listctrl1.SetStringItem(num, 2, (str(row[1])))
            self.listctrl1.SetStringItem(num, 3, (str(row[4])))
          
         
            row=cursor2.fetchone()
           
            
     
    def Onedit(self, e):
       self.editmat.SetFocus()
       

    def tabulacao_portrait(self,canvas):
        from reportlab.lib.units import inch
        from reportlab.lib.colors import pink, black, red, blue, green
        c = canvas

        c.setStrokeColor(black)
        c.setFont("Times-Roman", 10)

        y=680
        
        
        for n in range(30):
        
             
             c.rect(10,y,60,20)
             
             y=y-20
             
             if y <= 10:
                 break
             
        y=680
        
        for n in range(30):
        
             
             c.rect(70,y,160,20)
             
             y=y-20
             
             if y <= 10:
                 break
             
        y=680       
         
        for n in range(30):
        
             
             c.rect(230,y,70,20)
             
             y=y-20
             
             if y <= 10:
                 break
             
                
                
        y=680      
         
        for n in range(30):
        
             
             c.rect(300,y,50,20)
             
             y=y-20
             
             if y <= 10:
                 break  
 
        y=680      
         
        for n in range(30):
        
             
             c.rect(350,y,100,20)
             
             y=y-20
             
             if y <= 10:
                 break     
             
                
        y=680       
         
        for n in range(30):
        
             
             c.rect(450,y,120,20)
             
             y=y-20
             
             if y <= 10:
                 break           
                

    def tabulacao_landscape(self,canvas):
        
        
        from reportlab.lib.units import inch
        from reportlab.lib.colors import pink, black, red, blue, green
        c = canvas

        c.setStrokeColor(black)
        c.setFont("Times-Roman", 10)
     

        y=445
        
        for n in range(35):
        
             
             c.rect(10,y,60,20)
  
             y=y-20
             
             if y <= 10:
                 break
             
        y=445
        
        for n in range(35):
        
             
             c.rect(70,y,260,20)
 
             y=y-20
             
             if y <= 10:
                break
            
        y=445       
         
        for n in range(35):
        
             
             c.rect(330,y,80,20)

             y=y-20
             
             if y <= 10:
                 break

        y=445        
        
        for n in range(35):
       
             
             c.rect(410,y,60,20)
    
             y=y-20
             
             if y <= 10:
                 break  
 
        y=445       
         
        for n in range(35):
        
             
             c.rect(470,y,120,20)
    
             y=y-20
             
             if y <= 10:
                 break     
    
        y=445       
         
        for n in range(35):
        
             
             c.rect(590,y,220,20)
             
             y=y-20
             
             if y <= 10:
                 break           
        
        
    
    def Onprint(self, e,tipo):
       

        self.confirma=1

        
        orientacao = tipo+"(A4)"
        
   
        c = canvas.Canvas("/tmp/arquivo.pdf")

        print(orientacao)    
    
                   
        
        if orientacao == "portrait(A4)":
            
            
            c.setPageSize(portrait(A4))
   
            self.tabulacao_portrait(c)
      
            c.setFontSize(16)
            c.drawString(510,790,("Registro"))
            
            c.setFontSize(16)
            c.drawString(510,780,("impressão"))
            
       
            
       
        if orientacao == "landscape(A4)":  
      
            
            c.setPageSize(landscape(A4))

            
            c.setFontSize(16)
            c.drawString(700,550,("Registro de"))
            c.setFontSize(16)
            c.drawString(702,535,("impressão"))
         


        c.showPage()

        c.save()
        
        os.system("evince /tmp/arquivo.pdf&") 
        

    def Ondelete(self, e):
       
            db=MySQLdb.connect(host="localhost",port=3306,user="user",passwd="password",db="database")
            cursor = db.cursor()
    
            dialog = wx.MessageDialog(self,("Você quer realmente deletar esse registro?"),("Confirma exclusão"),
                                      wx.YES_NO | wx.ICON_QUESTION)
            remove = dialog.ShowModal() == wx.ID_YES
            dialog.Destroy()

            if remove:
                    num = str(self.editcod.GetValue())
               
                    cursor.execute("delete from TABLE4 where id_codigo= %s",[num])
                    db.commit()

                    self.Onant(0)

            e.Skip()    
        
        
                
        
     
