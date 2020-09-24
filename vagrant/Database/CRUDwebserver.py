from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi
import sys
import os
from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
class WebServerHandler(BaseHTTPRequestHandler):
    global session
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200,"OK")
                self.send_header("Content-Type","text/html")
                self.end_headers()
                res=session.query(Restaurant).all()
                output = ''
                output += "<html><body>"
                output += "<h1><a href='restaurants/new'> Create a new Restaurant</a>"
                for i in res:
                    output += "<h2>{}  .</h2>".format(i.id)
                    output += "<h2>{}</h2>".format(i.name)
                    output += "<h5><a href='/restaurants/{}/edit'>Edit</a><br></h5>".format(i.id)
                    output += "<h5><a href='/restaurants/{}/delete'>Delete</a><h5>".format(i.id)
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            if self.path.endswith("/menuitems"):
                self.send_response(200,"OK")
                self.send_header("Content-Type","text/html")
                self.end_headers()
                res=session.query(MenuItem).all()
                output = ''
                output += "<html><body>"
                for i in res:
                    output += "<h2>{}</h2>".format(i.name)
                    output += "<h5><a href='#'>Edit</a><br></h5>".format(i.id)
                    output += "<h5><a href='#'>Delete</a><h5>".format(i.id)
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200,"OK")
                self.send_header("Content-Type","text/html")
                self.end_headers()
                output = ''
                output += "<html><body>"
                output += "<h1>ADD A RESTAURANT</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input type='text' name='newRestaurantName'><input type='submit' value='create'></form>"
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            if self.path.endswith('/edit'):
                id_num = self.path.split('/')[2]
                print(id_num)
                self.send_response(200,"OK")
                self.send_header("Content-type","text/html")
                self.end_headers()
                output = ''
                output += "<html><body>"
                output += "<h1>WRITE THE RESTAURANT NAME</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/{}/edit'><input type='text' name='renameRestaurant'><input type='submit' value='RENAME'></form>".format(id_num)
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            if self.path.endswith('/delete'):
                id_num = self.path.split('/')[2]
                print(id_num)
                self.send_response(200,"OK")
                self.send_header("Content-type","text/html")
                self.end_headers()
                output = ''
                output += "<html><body>"
                output += "<h1>WRITE THE RESTAURANT NAME TO BE DELETED</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/{}/delete'><input type='submit' value='YES' name='Yes'><span></span><input type='submit' value='NO' name='No'></form>".format(id_num)
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print(output)
                return
            else:
                self.send_error(404,"File Not Found",self.path)
        except  IOError:
            self.send_error(404,"File Not Found",self.path)
    def do_POST(self):
        global messagecontent
        try:
            if self.path.endswith('/restaurants/new'):
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/restaurants")
                self.end_headers()
                ctype,pdict=cgi.parse_header(self.headers.get("Content-type"))
                pdict['boundary']=bytes(pdict['boundary'],'utf-8')
                if ctype == 'multipart/form-data':
                    print(pdict)
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent=fields.get("newRestaurantName")
                newRestaurant=Restaurant(name=messagecontent[0].decode('utf-8'))
                session.add(newRestaurant)
                session.commit()
                return
            if self.path.endswith('/edit'):
                id_num = self.path.split('/')[2]
                rename_hotel = session.query(Restaurant).filter_by(id=id_num).first()
                ctype,pdict=cgi.parse_header(self.headers.get('Content-type'))
                pdict['boundary']=bytes(pdict['boundary'],'utf-8')
                if ctype=="multipart/form-data":
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent=fields.get('renameRestaurant')
                rename_hotel.name=messagecontent[0].decode('utf-8')
                session.add(rename_hotel)
                session.commit()
                self.send_response(301)
                self.send_header("Content-type","text/html")
                self.send_header("Location","/restaurants")
                self.end_headers()
                return
            if self.path.endswith('/delete'):
                id_num = self.path.split('/')[2]
                rename_hotel = session.query(Restaurant).filter_by(id=id_num).first()
                ctype,pdict=cgi.parse_header(self.headers.get('Content-type'))
                pdict['boundary']=bytes(pdict['boundary'],'utf-8')
                if ctype=="multipart/form-data":
                    fields=cgi.parse_multipart(self.rfile,pdict)
                    messagecontent=fields.get('Yes')

                print(messagecontent)
                #print(messagecontent2)
                if messagecontent==None:
                    self.send_response(301)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Location", "/restaurants")
                    self.end_headers()
                    return
                elif messagecontent[0].decode('utf-8')=='YES':
                    session.delete(rename_hotel)
                    session.commit()
                self.send_response(301)
                self.send_header("Content-type","text/html")
                self.send_header("Location","/restaurants")
                self.end_headers()
                return
        except IOError:
            print(IOError)



def main():
    global server
    try:
        port=8080
        server=HTTPServer(('',port),WebServerHandler)
        print("server is running at port ",port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server Closed")
        server.socket.close()

if __name__ == '__main__':
    engine=create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind=engine
    DBsession=sessionmaker(bind=engine)
    session=DBsession()
    main()