#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp
import socket
import urllib


cache = {}


class miServidor (webapp.webApp):
    def parse(self, request):

        url = request.split()[1][1:].split('/')[0]
        cabeceras = request.split('\r\n', 1)[1]
        try:
            peticion = request.split()[1][1:].split('/')[1]
        except IndexError:
            peticion = None

        return (url, cabeceras, peticion)

    def process(self, parsedRequest):
        miurl = "http://" + socket.gethostname() + ":1234/" + parsedRequest[0]
        urlreal = "http://" + parsedRequest[0]

        pactual = ("<a href= '" + urlreal + "'>Pagina original.</a></br>" +
                   "<a href= '" + miurl + "'>Recargar pagina.</a></br>" +
                   "<a href= '" + miurl + "/cache'>cache</a></br>" +
                   "<a href= '" + miurl + "/HTTP-1'>HTTP-1</a></br>" +
                   "<a href= '" + miurl + "/HTTP-2'>HTTP-2</a></br>")

        try:
            x = urllib.urlopen(urlreal)

        except IOError:
            return ("400 Not Found", "<html><body><p>Pagina no encontrada" +
                                     "</p></html></body>")

        if parsedRequest[2] == "HTTP-1":

            return("200 OK", "<html><body>" + pactual +
                             "<p>-Cabeceras enviadas al navegador:</p>" +
                             "<p>No se envian cabeceras al navegador:" +
                             "<p>-Cabeceras recibidas del navegador:</p>" +
                             parsedRequest[1] + "</html></body>")

        elif parsedRequest[2] == "HTTP-2":
            cabecera = x.info()
            return ("200 OK", "<html><body>" + pactual +
                              "<p>-Cabeceras enviadas al servidor:<p>" +
                              + urlreal +
                              "<p>-Cabeceras recibidas del servidor  " +
                              + urlreal +
                              ":</p>" + str(cabecera) + "</html></body>")

        elif parsedRequest[2] == "cache":
            try:
                html = cache[urlreal]

        else:
            html = x.read()
            cache[urlreal] = html
            posicion = html.find('<body')
            posicion = html.find('>', posicion)
            html = (html[:posicion + 1] + pactual +
                    "</br></br>" + html[(posicion + 1):])

        return ("200 OK", html)

if __name__ == "__main__":
    serv = miServidor(socket.gethostname(), 1234)
