#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HtmlComponentsFind.py is part of Barleymap web app.
# Copyright (C) 2017 Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import sys

from HtmlComponentsBase import HtmlComponentsBase

class HtmlComponentsRetrieve(object):
    
    ######################### FIND FORM HTML COMPONENTS
    ###################################################
    @staticmethod
    def retrieve(base_url):
        output = []
        
        list_of_sets = []
        dict_of_sets = {}
        for line in open("sets_conf_file", "r"):
            line_data = line.strip().split()
            set_id = line_data[0]
            set_name = line_data[1]
            if set_id in dict_of_sets:
                continue
            else:
                dict_of_sets[set_id] = {}
                list_of_sets.append((set_id, set_name))
            #set_path = line_data[2]
        
        ####### INPUT QUERY TEXT AREA
        output.append("""
        <section id="content">
            <form name="input_retrieve" action="{0}" method="post" enctype="multipart/form-data">
            """.format(base_url+"/retrieve/run"))
        
        output.append("<br/>")
        output.append("<table><tr>")
        
        output.append('<td>')
        output.append('<tr>')
        output.append("""  
                <td><fieldset style="border:none;">
                    <legend>Contig/chr or gene identifier</legend>
                    <textarea rows="1" cols="30" id="retrieve_query" name="query"
                    autofocus="autofocus">contig_10000</textarea>
                </fieldset></td>
        """)
        #output.append('</tr>')
        output.append("""
                        <td style="width:50%;">
                            
                            <input type="radio" name="type_query" id="type_contig" value="contig" checked/>
                            
                            <label for ="type_contig">Contig/chr</label>
                            <input type="radio" name="type_query" id="type_gene" value="gene" />
                            <label for ="type_gene">Gene</label>
                         </td>
                    <!--</tr>-->
                    """)
                    
                    
        output.append('</tr>')
        output.append('<tr>')
        output.append('<td>')
        output.append("""
                <fieldset style="border:none;">
                    <legend>Start pos</legend>
                    <textarea rows="1" cols="16" id="retrieve_start" name="start"
                    autofocus="autofocus"></textarea>
                </fieldset>
        """)
        
        output.append("""
                <fieldset style="border:none;">
                    <legend>End pos</legend>
                    <textarea rows="1" cols="16" id="retrieve_end" name="end"
                    autofocus="autofocus"></textarea>
                </fieldset>
        """)
        output.append('</td>')
        output.append('<td>')
        # drop down for excap files
        output.append("""
                    <fieldset id="find_fieldset" style="border:solid thin;">
                    <legend style="text-align:left;">Choose dataset:</legend>
                    """)
        
        output.append(HtmlComponentsBase._load_data("ibsc2012",
                                                    list_of_sets,
                                                    "sets"))
        
        output.append("""              
                    </fieldset>
        """)
        output.append("</td>")
        output.append('</tr>')
        output.append("</td>")
        
        output.append('<td>')
        output.append("""
                <fieldset style="border:none;">
                    <legend>Max. miss</legend>
                    <textarea rows="1" cols="5" id="maxmiss" name="maxmiss"
                    autofocus="autofocus">1.0</textarea>
                </fieldset>
        """)
        output.append("""
                <fieldset style="border:none;">
                    <legend>Max. hets</legend>
                    <textarea rows="1" cols="5" id="maxhets" name="maxhets"
                    autofocus="autofocus">1.0</textarea>
                </fieldset>
        """)
        output.append("""
                <fieldset style="border:none;">
                    <legend>MAF</legend>
                    <textarea rows="1" cols="5" id="maf" name="maf"
                    autofocus="autofocus">0.0</textarea>
                </fieldset>
        """)
        output.append("</td>")
        
        output.append("""
                <td id="submit_button_td">
                    <button class="boton" id="submit_button" name="action" type="submit" value="retrieve">
                        <img src="{0}" onmouseover="hover_{1}(this);" onmouseout="unhover_{1}(this);"/>
                    </button>
                </td>
                </tr></table>
            </form>
        </section><hr/> <!-- content -->
        """.format(base_url+"/img/ui_buttons_find.png", "find"))
        
        output.append("""
        <script>
            // Functions to change image with mouse over and out
            function hover_{0}(element) {{
                element.setAttribute('src', '{2}');
            }}
            function unhover_{0}(element) {{
                element.setAttribute('src', '{1}');
            }}
        </script>
        """.format("find", base_url+"/img/ui_buttons_find_mini.png", base_url+"/img/ui_buttons_find_mini_hover.png"))
        
        return "".join(output)
        
        output.append("<br/>")
        output.append("<table><tr><td>")
        output.append(HtmlComponentsBase._load_output_area(find_form.get_multiple(),
                                         find_form.get_sort(),
                                         find_form.get_send_email(),
                                         find_form.get_email_to(),
                                         PREFIX_UI_CTRLS_FIND))
        output.append("</td><td>")
        output.append(HtmlComponentsBase._load_genes_area(find_form.get_show_markers(),
                                        find_form.get_show_genes(),
                                        find_form.get_show_anchored(),
                                        find_form.get_show_main(),
                                        find_form.get_show_how(),
                                        find_form.get_extend(),
                                        find_form.get_extend_cm(),
                                        find_form.get_extend_bp(),
                                        PREFIX_UI_CTRLS_FIND))
        output.append("</td></tr></table>")
        output.append("<br/>")
        
        output.append("""
                <table><tr>
                <td>
                    <fieldset id="find_fieldset" style="border:solid thin;">
                    <legend style="text-align:left;">Choose map:</legend>
                    """)
        
        #### MAPS
        output.append(HtmlComponentsBase._load_data(find_form.get_maps(),
                                                    maps_config.get_maps_tuples(),
                                                    "maps"))
        
        output.append("""
                      
                    </fieldset>
                </td><td id="submit_button_td">
                    <button class="boton" id="submit_button" name="action" type="submit" value="Retrieve">
                        <img src="{0}" onmouseover="hover_{1}(this);" onmouseout="unhover_{1}(this);"/>
                    </button>
                </td>
                </tr></table>
            </form>
        </section><hr/> <!-- content -->
        """.format(base_url+"/img/ui_buttons_find.png", "find"))
        
        output.append("""
        <script>
            // Functions to change image with mouse over and out
            function hover_{0}(element) {{
                element.setAttribute('src', '{2}');
            }}
            function unhover_{0}(element) {{
                element.setAttribute('src', '{1}');
            }}
        </script>
        """.format("find", base_url+"/img/ui_buttons_find_mini.png", base_url+"/img/ui_buttons_find_mini_hover.png"))
        
        return "".join(output)

## END