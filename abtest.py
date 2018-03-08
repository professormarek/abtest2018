#!/usr/bin/python
#import required libraries
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import random

probability_of_a = 0.80

htmla = """
<!DOCTYPE html>
<html>
    <head>
        <title>My Test Site</title>
    </head>
    <body>
        Click to save the kittens...
        <form action="/" method="post" >
            <button type='submit' name = 'my_button' value= 'Version_A_Clicked' >
                OK
            </button>
        </form>
    </body>
</html>"""

htmlb = """
<!DOCTYPE html>
<html>
    <head>
        <title>My Test Site</title>
    </head>
    <body>
        Click to save the puppies...
        <form action="/" method="post" >
            <button type='submit' name = 'my_button' value= 'Version_B_Clicked' >
                OK
            </button>
        </form>
    </body>
</html>"""

thanks = """
<!DOCTYPE html>
<html>
    <head>
        <title>My Test Site</title>
    </head>
    <body>
        Thanks for your bitcoins mwa ha ha
        <p>
        <a href="/"> go back </a>
    </body>
</html>"""

#use a file to store the log
logfile = open('abtest.log', 'w')

print "running AB test server"

#we're going to reuse the built in python
#web server called BaseHTTPRequestHandler
#we will represent the web server as a
#software "object" that reprsents the server
#as a "thing" we can interact with

#we will extend the functionality of the
#BaseHTTPRequestHandler in order to implement
#our desired behaviour which is displaying
#the A or B version of the page, randomly

#the BaseHTTPRequestHandler has a do_GET method
#to handle HTTP GET requests
#and has a do_POST method which handles POST requests
#we will override both with our cusotmized behaviour

#let's define our custom web server class
#we inherit or reuse the BaseHTTPRequestHandler class
class myABhandler(BaseHTTPRequestHandler):
	#create a handler for GET requests
	#we override the existing do_GET method in BaseHTTPRequestHandler
	def do_GET(self):
		print "do_GET was called: ", self.path
		#beginning of a "correct" http response
		#compose a proper HTTP response using the framework
		self.send_response(200) #OK / success
		self.send_header('Content-type', 'text/html')
		self.end_headers() #these three lines form the 

		#adding code to check if the browser is trying to download an icon. Basically stop if the browser
		#is requesting anything besides the default "/" or a .html file
		#this avoids counting spurious icon requests!
		if(self.path != "/" and not self.path.endswith(".html")):
			return #end early!

		#show version "a" with freqency - probability_of_a 
		if random.random() < probability_of_a:
			#show version A
			#wfile is the part of the handler that refers
			#to data going out (written) to the browser
			print "serving version A"
			logfile.write("serving version A\n")
			self.wfile.write(htmla)
		else:
			#show version B
			print "serving version B"
			logfile.write("serving version B\n")
			self.wfile.write(htmlb)

		
		return

	#create a handler for POST requests
	def do_POST(self):
		print "do_POST was called"
		#interpret the data coming from the web browser
		#represent the HTML form that was submitted
		form = cgi.FieldStorage(fp=self.rfile,
			headers=self.headers, 
			environ={'REQUEST_METHOD':'POST', 
			'CONTENT_TYPE':self.headers['Content-Type']
			}
		)
		#iterate through the data returned by the post reply
		#returned in the form of a dictionary (dict)
		for field in form.keys():
			field_item = form[field]
			#print "DEBUG: ", field_item
			if(field_item.name == "my_button"):
				if(field_item.value == "Version_A_Clicked"):
					print "version A was clicked"
					logfile.write("version A was clicked\n")

				else:
					print "version B was clicked"
					logfile.write("version B was clicked\n")



		self.send_response(200) #OK / success
		self.send_header('Content-type', 'text/html')
		self.end_headers() #these three lines form the 
		self.wfile.write(thanks)

		return


#down here, we atually invoke and use the 
#myABhandler class
print "starting AB server"

#recall that try-except lets python execute code
#which might "throw an execption" when something
#goes wrong
try:
	#create the web server and specify a handler
	#class for handling requests
	server = HTTPServer(('', 8080), myABhandler)
	print "starting http server on: ", server.socket.getsockname()
	server.serve_forever()

#KeyboardInterrupt is the exception that is thrown when
#the user presses ctrl+c
except KeyboardInterrupt:
	print "user pressed ctrl+c, shutting down web server"
	server.socket.close() #closes the socket..

#make sure you close any open files...
logfile.close()
print "program completed successfully"






