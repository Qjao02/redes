# Client and Server Python

Those codes are just a simple implementation of Client and Server using Socket API for python, where TCP made the connection, and GET requisitions make the communication between those applications

## Server

Server is responsable for attempt de GET requisitions, and follow with some response. First Server receives a menssage of some cliente (it can be a browser), and get the request GET from client, currently the answer from server can be, a file (text, zip or jpg for example) or the 404 error.

Run Server:
    
    python Servidor.py PORT SHAREDFOLDERNAME
    

    
## Client

Client are just capable of get some url and make a requistion GET for some Server, it will recives a binary, get the response reader and write the binary in a new file or decode in case of texts (HTML for example).

Run Client
    
    python Cliente.py
    
    
Example of requistion
   
    localhost:PORT/index.html
    
    
## Dependencies
  
  Client and Server needs those follows python Librarys:
*  Python 3
*  API Sockets
*  OS
*  SYS
 
