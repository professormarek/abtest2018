#!/usr/bin/python
#import required libraries
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import random

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
		print "do_GET was called"
		#beginning of a "correct" http response
		#compose a proper HTTP response using the framework
		self.send_response(200) #OK / success
		self.send_header('Content-type', 'text/html')
		self.end_headers() #these three lines form the 

		#wfile is the part of the handler that refers
		#to data going out (written) to the browser
		self.wfile.write('Hello world')
		return

	#create a handler for POST requests
	def do_POST(self):
		print "do_POST was called"


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



print "program completed successfully"






