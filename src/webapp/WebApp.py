#!/usr/bin/env python
# -*- coding: utf-8 -*-

# WebApp.py is part of excap web app.
# Copyright (C) 2018  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import sys, traceback
import cherrypy

from html.HtmlLayout import HtmlLayout

from FormsFactory import FormsFactory

########## MAIL SERVER
# check file in /home/excap/email/

class Root():
    
    MOUNT_POINT = None
    
    VERBOSE = False
    
    def __init__(self, MOUNT_POINT, VERBOSE):
        self.MOUNT_POINT = MOUNT_POINT
        self.VERBOSE = VERBOSE
        return
    
    def _get_html_layout(self):
        
        return HtmlLayout(self.MOUNT_POINT)
    
    @cherrypy.expose
    def index(self):
        try:
            sys.stderr.write("excap web app: request to /index\n")
            
            html_layout = self._get_html_layout()
            
            retrieve_component = html_layout.retrieve_components()
            
            
            contents = [html_layout.menu(),
                        retrieve_component]
            
            output = "".join([html_layout.html_head(),
                             html_layout.header(),
                             html_layout.html_container(contents),
                             html_layout.footer(),
                             html_layout.html_end()])
        
        except Exception, e:
            sys.stderr.write(str(e)+"\n")
            traceback.print_exc(file=sys.stderr)
            output = "There was a server error. Please, contact with excap web application adminitrators."
        
        return output
    
## END