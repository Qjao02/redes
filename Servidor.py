
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-

import socket
import os 
import datetime as dt
import threading as th

    
def requestMessage (con,cliente):
    print ("aguardando mensagem") 
    mensagem = con.recv(1024).decode('utf-8')

    msg = mensagem.split("\r\n")
    request['operation'] = msg[0]
    del(msg[0])

    print(request['operation'])

    #debug variable
    cont = 0

    for line in msg:
        cont = cont+1
        print (line)
        lineSplit = line.split(': ')
        try:
            key = lineSplit[0]
            valor = lineSplit[1]
            request[key] = valor
        except:
            print('error create dictionary on ' + str(cont) + 'line')


    filepath = request['operation'].split()[1]

    if request['operation'].split()[1]== '/':
        print('if')
        nameFile = request['operation'].split()

        print (filepath)
        file = open('content/Index.html','rb')

        fileByte = file.read()

        respostaString = '\nHTTP/1.1 200 Ok \n'

        resposta = {
            "Location" : "http://localhost:7000/",
            'date' : str(dt.datetime.now()),
            'Server' : 'jaoserver',
            'Content-Type' : 'text/html',
            'Content-Lenght' : str(len(fileByte))

        }
        for key,valor in resposta.items():
            respostaString = respostaString + key+': '+ valor + '\r\n'


        con.send( respostaString.encode('utf-8') + fileByte )

    else:
        filePath = request['operation'].split()[1]
        print('content' + filePath)
        
        if os.path.isfile('content' + filepath) :
            file = open('content'+filepath,'rb')
            respostaString = '\nHTTP/1.1 200 ok! \n'
            fileByte = file.read()
            
        elif os.path.isdir('content' + filePath):
            
            
            files = os.listdir('content' + filepath)
            createListHtml(filePath,files)
            
            
            file = open('content/temp/listDir.html','rb')
            fileByte = file.read()
            respostaString = '\nHTTP/1.1 200 ok! \n'

            
        else:
            print('arquivo nao existe')
            file = open('content/404.html','rb')
            respostaString = '\nHTTP/1.1 404 Not Found! \n'
            fileByte = file.read()


        resposta = {
            "Location" : "http://localhost:7000/",
            'date' : str(dt.datetime.now()),
            'Server' : 'jaoserver',
            'Content-Type' : 'text/html',
            'Content-Length' : str(len(fileByte))

        }

        for key,valor in resposta.items():
            respostaString = respostaString + key+': '+ valor + '\r\n'
        
        respostaString = respostaString + '\n'
        file.close()
        con.send( respostaString.encode('utf-8') + fileByte)
    con.close()

def createListHtml(filePath,files):
    file = open('content/temp/listDir.html','w')
    file.write('<html> \r\n')
    file.write('<head><title>listDir</title></head>\n')
    file.write('<body>\n')
    file.write('<h1>MUTHERFUCKER PAGES</H1>')
    for fileName in files:
        file.writelines('<a href="' + filePath + '/'+fileName+'">'+fileName+'</a><br>\n')
    
    file.writelines('</body>\n')
    file.writelines('</html>\n')
    file.close()
    
request = {}
host = 'localhost' 
port =  7000

addr = (host, port) 
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(addr) 
serv_socket.listen(10) 

#variaveis declaradas
file = ''
fileByte = ''

while True:
    
    print ('aguardando conexao') 
    
    con, cliente = serv_socket.accept() 
    print ('conectado')
    t = th.Thread(target = requestMessage, args=(con,cliente))
    t.start()
    t.join()
    
    

