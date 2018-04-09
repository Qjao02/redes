
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-

import socket
import os 
import datetime as dt
import threading as th
import sys

    
def requestMessage (con,cliente,extensionDict,shareFolder):
    
    print ("aguardando mensagem") 
    mensagem = con.recv(1048576).decode('utf-8')

    msg = mensagem.split("\n")
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
            break

    try:
        filepath = request['operation'].split()[1]
    except:
        filepath='servConfig/400.html'
        
    if filepath == '/':
        nameFile = request['operation'].split()

        file = open(shareFolder + '/Index.html','rb')

        fileByte = file.read()

        respostaString = '\nHTTP/1.1 200 Ok \r\n'

        resposta = {
            "Location" : "http://localhost:7000/",
            'date' : str(dt.datetime.now()),
            'Server' : 'jaoserver',
            'Content-Type' : 'text/html',
            'Content-Lenght' : str(len(fileByte))

        }
        for key,valor in resposta.items():
            respostaString = respostaString + key+': '+ valor + '\r\n'

        respostaString = respostaString + '\r\n'
        con.send( respostaString.encode('utf-8') + fileByte )

    else:
            
        if os.path.isfile(shareFolder + filepath) :
            file = open(shareFolder + filepath,'rb')
            respostaString = '\nHTTP/1.1 200 ok! \r\n'
            fileByte = file.read()
            index = filepath.rfind('.')
            keyExtension = filepath[index:]
            
        elif os.path.isdir(shareFolder + filepath):
            
            files = os.listdir(shareFolder + filepath)
            createListHtml(filepath,files,shareFolder)
            
            keyExtension = '.isdir'
            
            file = open(shareFolder+'/temp/listDir.html','rb')
            fileByte = file.read()
            respostaString = '\nHTTP/1.1 200 ok! \n'
            
            
        else:
            file = open('servConfig/404.html','rb')
            respostaString = '\nHTTP/1.1 404 Not Found! \r\n'
            fileByte = file.read()
            keyExtension = '.html'

        resposta = {
            "Location" : "http://localhost:7000/",
            'date' : str(dt.datetime.now()),
            'Server' : 'jaoserver',
            'Content-Type' : extensionDict[keyExtension],
            'Content-Length' : str(len(fileByte))

        }

        for key,valor in resposta.items():
            respostaString = respostaString + key+': '+ valor + '\r\n'
        
        respostaString = respostaString + '\r\n'
        file.close()
        con.sendall( respostaString.encode('utf-8') + fileByte )
    con.close()

def createListHtml(filePath,files,shareFolder):
    file = open(shareFolder + '/temp/listDir.html','w')
    file.write('<html>')
    file.write('<head><title>listDir</title></head>')
    file.write('<body>')
    file.write('<h1>MUTHERFUCKER PAGES</H1>')
    for fileName in files:
        file.write('<a href="' + filePath + '/'+fileName+'">'+fileName+'</a><br>')
    
    file.write('</body>')
    file.write('</html>')
    file.close()
    
request = {}
host = '10.0.0.248' 
port = int(sys.argv[1])
print(str(port))

shareFolder = sys.argv[2]
loadextensions = open('servConfig/extension.txt','r')
extensionDict = {}

for line in loadextensions:
    keyValue = line.split('\t')
    index = keyValue[1].find('\r\n')
    extensionDict[keyValue[0]] = keyValue[1][:index]
    
loadextensions.close()
addr = (host, port) 
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(addr) 
serv_socket.listen(10) 

#variaveis declaradas
file = ''
fileByte = ''
cons = set()
cont = 0
while True:    
    con, cliente = serv_socket.accept() 
    print ('conectado')
    cons.add(con)
    th.Thread(target=requestMessage,args=(con, cliente, extensionDict,shareFolder)).start()
    


# In[ ]:
