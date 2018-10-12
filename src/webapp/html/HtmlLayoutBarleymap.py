#!/usr/bin/env python
# -*- coding: utf-8 -*-

# HtmlLayoutBarleymap.py is part of Barleymap web app.
# Copyright (C) 2017  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

class HtmlLayoutBarleymap(object):
    
    @staticmethod
    def output_html_img_button(action, url, img_url, width = "3%", height = "3%", img_url_hover = None):
        output = []
        if url and img_url:
            output.append("""<a href="{1}">
                          <img style="width:{2};height:{3}; border:0;"
                          onmouseover="hover_{0}(this);" onmouseout="unhover_{0}(this);"
                          src="{4}"/>
                          </a>""".format(action, url, width, height, img_url))
            
            if img_url_hover:
                # Functions to change maps image (zoom or full maps)
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
                """.format(action, img_url, img_url_hover))
        else:
            Exception("HtmlLayoutBarleymap: No URL or img_url provided for img button.")
        
        return "".join(output)
    
    @staticmethod
    def main_text(citation, base_url, PREFIX_UI_CTRLS_ALIGN, PREFIX_UI_CTRLS_FIND, PREFIX_UI_CTRLS_LOCATE):
        output = []
        #output.append('<br/>')
        output.append('<div id="main_buttons" style="margin:0px;">')
        output.append('<table id="main_buttons_table" center><tr>')
        output.append('<td style="text-align:center;">')
        output.append(HtmlLayoutBarleymap.output_html_img_button(PREFIX_UI_CTRLS_FIND, base_url+"/"+PREFIX_UI_CTRLS_FIND+"/",
                                                                 base_url+"/img/ui_buttons_find.png", "200px", "100px",
                                                                 base_url+"/img/ui_buttons_find_hover.png"))
        output.append("</td>")
        output.append('<td style="text-align:center;">')
        output.append(HtmlLayoutBarleymap.output_html_img_button(PREFIX_UI_CTRLS_ALIGN, base_url+"/"+PREFIX_UI_CTRLS_ALIGN+"/",
                                                                 base_url+"/img/ui_buttons_align.png", "200px", "100px",
                                                                 base_url+"/img/ui_buttons_align_hover.png"))
        output.append("</td>")
        output.append('<td style="text-align:center;">')
        output.append(HtmlLayoutBarleymap.output_html_img_button(PREFIX_UI_CTRLS_LOCATE, base_url+"/"+PREFIX_UI_CTRLS_LOCATE+"/",
                                                                 base_url+"/img/ui_buttons_locate.png", "200px", "100px",
                                                                 base_url+"/img/ui_buttons_locate_hover.png"))
        output.append("</td>")
        output.append('<td style="text-align:center;">')
        output.append(HtmlLayoutBarleymap.output_html_img_button("help", base_url+"/help/",
                                                                 base_url+"/img/ui_buttons_help.png", "200px", "100px",
                                                                 base_url+"/img/ui_buttons_help_hover.png"))
        output.append("</td>")
        output.append("</tr>")
        output.append("</table>")
        output.append("</div>")
        #output.append('<br/>')
        
        output.append('<div id="main_text">')
        output.append(HtmlLayoutBarleymap.text_menu(citation, base_url, show_last_changes = True))
        output.append("</div>")
        
        return "".join(output)
    
    @staticmethod
    def head(base_url):
        return """
        <!DOCTYPE html>
        <!--[if lt IE 7 ]> <html class="ie6"> <![endif]-->
        <!--[if IE 7 ]>    <html class="ie7"> <![endif]-->
        <!--[if IE 8 ]>    <html class="ie8"> <![endif]-->
        <!--[if IE 9 ]>    <html class="ie9"> <![endif]-->
        <!--[if (gt IE 9)|!(IE)]><!--> <html class=""> <!--<![endif]-->
        <head>
            <meta charset="utf-8" />
            <title>excap</title>
            <meta content="CPCantalapiedra" name="CPCantalapiedra" />
            <link rel="stylesheet" href="{0}" type="text/css" media="screen"/>
        </head>""".format(base_url+"/style.css")
    
    @staticmethod
    def js_scripts(base_url):
        scripts = ""
        
        scripts = """
            <body>
        <script src="{0}"></script>
        <script src="{1}"></script>
        """.format("http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js", \
                   base_url+"/js/index.js")
        
        return scripts
    
    @staticmethod
    def js_scripts_maps(base_url, app_google_analytics_id):
        scripts = ""
        
        scripts = """
            <body>
        <script src="{0}"></script>
        <script src="{1}"></script>
        """.format("http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js", \
                   base_url+"/js/maps.js")
        
        scripts = scripts + """
        <!-- Google Analytics -->
        <script>
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
          
            ga('create', '"""+app_google_analytics_id+"""', 'auto');
            ga('send', 'pageview');
          
        </script>
        """
        
        return scripts
    
    @staticmethod
    def title_header(base_url):
        return """
        <header id="top">
            <h2><a href="{1}/">excap web app</a></h2>
            <h3 class="infobar">({0})</h3>
        </header>
        """.format("Retrieve exome capture markers", base_url)
    
    @staticmethod
    def footer():
        return """
        <footer class="infobar">
            <a href="http://www.eead.csic.es/compbio/" target="_blank">Laboratory of Computational Biology</a>
            ::
            <a href="http://eead.csic.es/" target="_blank">Estaci&oacute;n Experimental de Aula Dei</a>
            ::
            <a href="http://www.csic.es/" target="_blank">Consejo Superior de Investigaciones Cient&iacute;ficas</a>
        </footer>
        """
    
    @staticmethod
    def text_menu(base_url, show_last_changes = False):
        text_buffer = []
            
        text_buffer.append("""
            <i>vilely adapted from barleymap web app by Carlos P. Cantalapiedra at EEAD-CSIC...</i>
            <br/>
            <hr/>
            <div style="text-align:center;"><strong>>>>>> excap web app <<<<<</strong></div>
            <hr/>
            Types of query:
            <ul style="font-size:12px">
            <li><strong>Contig</strong>: write the contig identifier and choose the "Contig/chr" option in the radio button.
            Example: contig_10000</li>
            <li><strong>Chr</strong>: write the chromosome identifier, choose the "Contig/chr" option in the radio button.
            Example: chr1H</li>
            It is VERY IMPORTANT to specify <strong>start</strong> and <strong>end</strong> positions when searching in chromosomes.
            If not <strong>start</strong> and <strong>end</strong> positions are specified,
            all positions from a given contig, chromosome or gene will be reported.
            <li><strong>Gene</strong>: write the gene identifier and choose the "Gene" option in the radio button.
            If the identifier does not contain ".", results for all the gene isoforms will be reported. Example: MLOC_3.
            If the identifier contains ".", results from only a specific isoform will be reported. Exmaple: MLOC_3.2.</li>
            </ul>
            
            <strong>Max. miss</strong>, <strong>Max. hets</strong> and <strong>MAF</strong> and optional parameters to filter out results.
            Default values are 1.0, 1.0 and 0.0, respectively, which produce no filtering.
            <br/><br/>
            The results table has the <strong>genotypic values</strong>, which can be:
            <ul style="font-size:12px">
            <li>1 or 0 (homozygot genotype)</li>
            <li>0.5 (heterozygot genotype)</li>
            <li>-1 (missing value).</li>
            </ul>
            
            <br/>
        """)
        
        return "".join(text_buffer)
    
## END
