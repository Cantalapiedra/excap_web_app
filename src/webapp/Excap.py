#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bmap.py is part of Barleymap web app.
# Copyright (C) 2017  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import sys, tempfile, os, csv

from parse_contigs_variants import parse_contigs
from parse_gene_variants import parse_genes

#from CSVWriter import CSVWriter
#from CSVWriter import CSVWriter
#from html.output.OutputMaps import OutputMaps

#import m2p_mail

FIND_ACTION = "find"
ALIGN_ACTION = "align"
LOCATE_ACTION = "locate"
RETRIEVE_ACTION = "retrieve"

class Excap(object):
    
    _default_sort = None
    _max_queries = None
    _action = None
    _n_threads = None
    _app_name = None
    
    _verbose = False
    
    def __init__(self, app_name, verbose = False):
        self._app_name = app_name
        self._verbose = verbose
    
    def output_download_html_img(self, url, img_url):
        output_buffer = []
        if url and img_url:
            output_buffer.append('<a href="'+url+'" download="report.csv">'+\
                                 '<img style="width:4%;height:8%;" src="'+img_url+'"/></a>')
        else:
            raise m2pException("No URL or img_url provided to output_html_link in html_writer.py")
        
        return output_buffer
    
    ##
    def retrieve(self, form):
        
        query = form.get_query()
        sets = form.get_sets()
        start = form.get_start()
        end = form.get_end()
        maxmiss = form.get_maxmiss()
        maxhets = form.get_maxhets()
        maf = form.get_maf()
        type_query = form.get_type_query()
        
        sys.stderr.write(query+"\n")
        sys.stderr.write(str(sets)+"\n")
        
        # Sets
        sets_conf_file = "/var/www/html/excap/sets_conf_file"
        
        sys.stderr.write(str(sets_conf_file)+"\n")
        ## Read sets conf file
        sets_list = []
        for line in open(sets_conf_file, 'r'):
            line_data = line.strip().split()
            set_id = line_data[0]
            set_name = line_data[1]
            set_path = line_data[2]
            
            if set_id in sets:
                sets_list.append((set_id, set_name, set_path))
        
        tmp_files_path = "/var/www/html/excap/tmp_files"
        
        ## Retrieve variants from set
        if type_query == "contig":
            csv_file = parse_contigs(query, sets_list, start, end, maxmiss, maxhets, maf, tmp_files_path)
        elif type_query == "gene":
            csv_file = parse_genes(query, sets_list, start, end, maxmiss, maxhets, maf, tmp_files_path)
        else:
            raise Exception("Type of query unknown "+str(type_query))
        
        basename_csv_file = os.path.split(csv_file[1])[1]
        sys.stderr.write(basename_csv_file+"\n")
        base_url = "/excap"
        url = base_url+"/"+os.path.basename(tmp_files_path)+"/"+basename_csv_file
        img_url = base_url+"/img/csv_download.jpg"
        output_buffer = self.output_download_html_img(url, img_url)
        ## Return variants
        #results = csv_file
        
        return "".join(output_buffer)
    
    ## Output mapping results
    ##
    # def output(self, all_mapping_results, form, html_layout, csv_files):
    #     
    #     output_maps = OutputMaps(self._paths_config, self._app_name, html_layout)
    #     
    #     output = output_maps.output(all_mapping_results, form, csv_files)
    #     
    #     return output
    
    ## Obtain csv files
    ##
    # def csv_files(self, all_mapping_results, form):
    #     
    #     csv_writer = CSVWriter(self._paths_config, self._verbose)
    #     
    #     csv_files = csv_writer.output_maps(all_mapping_results, form)
    #     
    #     return csv_files
    
    ## Send email with results
    ##
    # def email(self, form, csv_files, email_conf):
    #     
    #     # Maps configuration files
    #     paths_config = self._paths_config
    #     __app_path = paths_config.get_app_path()
    #     maps_conf_file = __app_path+MAPS_CONF
    #     maps_config = MapsConfig(maps_conf_file, self._verbose)
    #     
    #     try:
    #         csv_filenames = []
    #         csv_filedescs = []
    #         maps_csv_files = csv_files.get_maps_csv_files()
    #         for map_id in maps_csv_files:
    #             map_name = maps_config.get_map_config(map_id).get_name()
    #             
    #             map_csv_files = maps_csv_files[map_id]
    #             if map_csv_files.get_mapped():
    #                 csv_filenames.append(map_csv_files.get_mapped())
    #                 csv_filedescs.append(map_name+".mapped")
    #             
    #             if map_csv_files.get_map_with_genes():
    #                 csv_filenames.append(map_csv_files.get_map_with_genes())
    #                 csv_filedescs.append(map_name+".with_genes")
    #             
    #             if map_csv_files.get_map_with_markers():
    #                 csv_filenames.append(map_csv_files.get_map_with_markers())
    #                 csv_filedescs.append(map_name+".with_markers")
    #             
    #             if map_csv_files.get_map_with_anchored():
    #                 csv_filenames.append(map_csv_files.get_map_with_anchored())
    #                 csv_filedescs.append(map_name+".with_anchored")
    #             
    #             if map_csv_files.get_unmapped():
    #                 csv_filenames.append(map_csv_files.get_unmapped())
    #                 csv_filedescs.append(map_name+".unmapped")
    #             
    #             if map_csv_files.get_unaligned():
    #                 csv_filenames.append(map_csv_files.get_unaligned())
    #                 csv_filedescs.append(map_name+".unaligned")
    #             
    #         
    #         ## Send CSV by EMAIL if requested
    #         if form.get_send_email() and form.get_send_email()=="1" and len(csv_filenames)>0:
    #             m2p_mail.send_files(form, csv_filenames, csv_filedescs, email_conf)
    #         
    #     except m2pException as e:
    #         ## Just log it, but keep giving output maps to the user
    #         sys.stderr.write("Error sending email.\n")
    #     
    #     return

## END