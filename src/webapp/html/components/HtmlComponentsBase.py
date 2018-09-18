#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HtmlComponentsBase.py is part of Barleymap web app.
# Copyright (C) 2017 Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import sys

from barleymapcore.m2p_exception import m2pException

class HtmlComponentsBase(object):
    
    @staticmethod
    def _load_query_area_retrieve(legend, action = "retrieve", name = "query"):
        output = []
        
        output.append("""
                <!-- QUERY AREA -->
                <fieldset style="border:none">
                    <legend>{1}</legend>
                    <textarea rows="1" cols="50" id="{0}_{2}" name="{2}"
                    autofocus="autofocus"></textarea>
                    """.format(action, legend, name))
        output.append("""
                </fieldset>
        """)
        
        return "".join(output)
    
    @staticmethod
    def _load_output_area(input_multiple, input_sort, send_email, email_to, action):
        output = []
        
        ## <!-- <fieldset style="border:solid thin;width:350px;height:170px;"> -->
        output.append("""
                <fieldset style="border:solid thin;width:350px;height:180px">
                <legend>Output options:</legend>
                    <table style="width:100%;text-align:center;">
                    <tr>
                    """)
        
        ########## MULTIPLE
        
        output.append("""
                        <!-- FILTER MULTIPLE CHECK BOX -->
                        <td style="width:50%;">
                            <label for = "multiple">Show markers with multiple mappings: </label>
                            <input type="checkbox" id="multiple" name="multiple" value="1"
            """)
            
        if input_multiple == "1": output.append(" checked/>")
        else: output.append(" />")
        
        output.append("""
                        </td>
                      </tr>
                      <tr><td><hr/></td></tr>
                      <tr>
                      """)
        
        ############ SORT
        output.append("""
                        <!-- SORTING FIELD -->
                        <td style="width:50%;">
                            <label for = "sort">Sort by: </label>
                            <input type="radio" name="sort" id="sort_cm" value="cm" 
                    """)
        
        if input_sort == "" or input_sort == "cm": output.append(" checked/>")
        else: output.append(" />")
        
        output.append("""
                            <label for ="sort_cm">cM</label>
                            <input type="radio" name="sort" id="sort_bp" value="bp"
                    """)
        if input_sort == "bp": output.append(" checked/>")
        else: output.append(" />")
        
        output.append("""
                            <label for ="sort_bp">bp</label>
                         </td>
                    </tr>
                    <tr><td><hr/></td></tr>
                    <tr><td style="width:50%;">
                    """)
        
        ############## email
        output.append("""
                    <fieldset style="border:none;text-align:center;">
                        <label for="send_email">Send by e-mail</label>
                        <input id="input_send_email" type="checkbox" name="send_email" value="1"
                    """)
        
        if send_email == "1": output.append(" checked/>")
        else: output.append(" />")
        
        if send_email == "1" and email_to: output.append('<input type="email" name="email_to" autocomplete="on" value="'+str(email_to)+'"/>')
        else: output.append('<input type="email" name="email_to" autocomplete="on" value=""/>')
        
        output.append("""
                        <br/><span id="email_text" class="explain_text">Results will be sent to the speficied address.</span>
                        </fieldset>
                        </td></tr></table>
                        """)
        
        return "".join(output)
    
    @staticmethod
    def _load_data(input_data, config_data, input_name):
        output = []
        
        #output.append('<select name="{0}" id="{0}" multiple>'.format(str(input_name)))
        output.append('<select name="{0}" id="{0}">'.format(str(input_name)))
        
        if not input_data:
            input_data = []
        elif input_data == "":
            input_data = []
        elif isinstance(input_data, basestring): # If only one dataset provided, best if embeb it in a list
            input_data = [input_data]
        #else: input_data is already a list
        
        #(data_names, data_ids) = load_data(conf_file, verbose = ResourcesMng.get_verbose())
        
        for configured_data in config_data:
            conf_id = configured_data[0]
            conf_name = configured_data[1]
            output.append('           <option value="{0}"'.format(conf_id))
            if conf_id in input_data or len(input_data)==0:
                output.append('selected')
            
            output.append('>{0}</option>'.format(conf_name))
        
        output.append("</select>")
        
        return "".join(output)

## END
