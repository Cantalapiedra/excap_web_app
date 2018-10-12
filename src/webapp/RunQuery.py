#!/usr/bin/env python
# -*- coding: utf-8 -*-

# RunQuery.py is part of excap web app.
# Copyright (C) 2018  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import sys, traceback
import cherrypy

from Excap import Excap
from FormsFactory import FormsFactory
from html.HtmlLayout import HtmlLayout


EMAIL_CONF = "EMAIL_CONF"
APP_NAME = "APP_NAME"
#N_THREADS = "N_THREADS"
#MAX_QUERIES = "MAX_QUERIES"

class Root():
    
    MOUNT_POINT = None
    PATHS_CONFIG = None
    
    VERBOSE = False
    
    def __init__(self, MOUNT_POINT, VERBOSE):
        self.MOUNT_POINT = MOUNT_POINT
        self.VERBOSE = VERBOSE
    
    def _get_html_layout(self, bmap_settings):
        return HtmlLayout(self.MOUNT_POINT)#, bmap_settings[APP_GOOGLE_ANALYTICS_ID])
    
    # For example, T3 or GrainGenes links
    # Maybe, this could be implemented as REST API in the future
    @cherrypy.expose
    def run(self, action, query, sets, start, end,
            maxmiss, maxhets, maf, type_query):
        
        # curl "http://161.111.227.14/excap/retrieve/run?action=retrieve&query=contig_67536&start=-1&end=-1&sets=ibsc2012&maxmiss=1&maxhets=1&maf=0&type_query=contig"
        
        sys.stderr.write("server.py: GET request to /retrieve/index\n")
        sys.stderr.write(action+"\n")
        sys.stderr.write(str(query)+"\n")
        sys.stderr.write(str(start)+"\n")
        sys.stderr.write(str(end)+"\n")
        sys.stderr.write(str(sets)+"\n")
        sys.stderr.write(str(maxmiss)+"\n")
        sys.stderr.write(str(maxhets)+"\n")
        sys.stderr.write(str(maf)+"\n")
        sys.stderr.write(str(type_query)+"\n")
        
        try:
            excap_settings = cherrypy.request.app.config['excapsettings']
            
            if not start: start = 0
            if not end: end = 0
            if not maxmiss: maxmiss = 1.0
            if not maxhets: maxhets = 1.0
            if not maf: maf = 0.0
            
            form = FormsFactory.get_retrieve_form_new(query, sets, long(start), long(end),
                                                      float(maxmiss), float(maxhets), float(maf),
                                                      type_query)
            
            form.set_action(action)
            form.set_session(cherrypy.session)
            
            app_name = excap_settings[APP_NAME]
            
            excap = Excap(app_name, self.VERBOSE)
            
            results = excap.retrieve(form)
            
            output = "click on the image to download your results >>> "
            output += str(results)
            
            #email_conf = excap_settings[EMAIL_CONF]
            #
            #excap.email(form, csv_files, email_conf)
            
        except Exception, e:
            sys.stderr.write(str(e)+"\n")
            traceback.print_exc(file=sys.stderr)
            output = "There was a server error. Please, contact with barleymap web application adminitrators."
        
        return output
    
## END
