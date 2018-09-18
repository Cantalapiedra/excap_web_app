#!/usr/bin/env python
# -*- coding: utf-8 -*-

# server.py is part of excap web app.
# Copyright (C) 2018  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import os, sys
import cherrypy

import webapp.WebApp as WebApp
import webapp.RunQuery as RunQuery

MOUNT_POINT = "/excap"

SERVER_CONFIG_FILE = "server.conf"
CONFIG_FILE = "excap.conf"

VERBOSE = False

## Loads server and barleymap configuration,
## loads the app into the server,
## and deploys the server
def start_standalone():
    sys.stderr.write("Starting server...\n")
    
    sys.stderr.write("Python path:\n")
    sys.stderr.write(str(sys.path)+"\n")
    
    ############## LOAD SERVER CONFIGURATION
    ########################################
    server_conf_file = os.path.join(os.path.dirname(__file__), SERVER_CONFIG_FILE)
    cherrypy.config.update(server_conf_file)
    
    sys.stderr.write("\tcherrypy configuration files loaded\n")
    
    ############### LOAD THE EXCAP APP
    #################################
    # Classes with exposed methods
    root = WebApp.Root(MOUNT_POINT, VERBOSE)
    
    root.retrieve = RunQuery.Root(MOUNT_POINT, VERBOSE)
    
    # Mount app on server, with webapp config file
    app_conf_file = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    
    app = cherrypy.tree.mount(root, script_name=MOUNT_POINT, config=app_conf_file)
    
    sys.stderr.write("\t"+MOUNT_POINT+" mounted\n")
    
    # Add barleymap configuration
    #bmap_conf_dict = _load_globals()
    #abs_path = os.path.dirname(os.path.abspath(__file__))
    
    ################ STARTING THE SERVER
    ####################################
    #if hasattr(cherrypy.engine, "signal_handler"):
    #    cherrypy.engine.signal_handler.subscribe()
    #if hasattr(cherrypy.engine, "console_control_handler"):
    #    cherrypy.engine.console_control_handler.subscribe()
    
    # or
    
    #cherrypy.engine.signals.subscribe()
    
    cherrypy.engine.start()
    
    sys.stderr.write("Server started. Accepting requests...\n")
    
    cherrypy.engine.block() ## Here the server stops to accept requests
    
    ####################################
    
    #cherrypy.quickstart(root, script_name="/"+ResourcesMng.get_app_name(), config=global_conf_dict)
    
    sys.stderr.write("Server stopped.\n")
    
    return

##########################
########################## START
if __name__ == '__main__':
    sys.stderr.write("In the beginning...\n")
    start_standalone()
    sys.stderr.write("...towards an end.\n")

## END