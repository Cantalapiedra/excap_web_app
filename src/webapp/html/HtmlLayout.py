#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HtmlLayout.py is part of Barleymap web app.
# Copyright (C) 2017  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import sys

from components.HtmlComponentsRetrieve import HtmlComponentsRetrieve

from HtmlLayoutBarleymap import HtmlLayoutBarleymap

class HtmlLayout(object):
    _base_url = None
    
    def __init__(self, base_url):
        self._base_url = base_url
    
    ## Basic layout methods
    ##
    def html_head(self):
        output = []
        output.append(HtmlLayoutBarleymap.head(self._base_url))
        output.append(HtmlLayoutBarleymap.js_scripts(self._base_url))
        
        return "".join(output)  
    
    def html_head_maps(self):
        output = []
        output.append(HtmlLayoutBarleymap.head(self._base_url))
        output.append(HtmlLayoutBarleymap.js_scripts_maps(self._base_url, self._app_google_analytics_id))
        
        return "".join(output)
    
    def header(self):
        return HtmlLayoutBarleymap.title_header(self._base_url)
    
    def html_container(self, contents = []):
        return '<div id="container" style="margin:10px;">'+"".join(contents)+'</div> <!-- container -->'
    
    def footer(self):
        return HtmlLayoutBarleymap.footer()
    
    def html_end(self):
        return """
        </body>
        </html>
        """
    
    ## Methods which add content to the previous layout
    ##
    def main_text(self, citation):
        
        return HtmlLayoutBarleymap.main_text(citation, self._base_url, PREFIX_UI_CTRLS_ALIGN, PREFIX_UI_CTRLS_FIND,
                                             PREFIX_UI_CTRLS_LOCATE)
    
    def menu(self):
        
        output = []
        output.append('<div id="menu">')
        output.append(HtmlLayoutBarleymap.text_menu(self._base_url, show_last_changes = False))
        output.append('</div>')
        
        return "".join(output)
    
    ## Methods for specific contents
    ##
    def retrieve_components(self):
        
        retrieve_components = HtmlComponentsRetrieve.retrieve(self._base_url)
        
        return retrieve_components

## END