#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CSVWriter.py is part of Barleymap web app.
# Copyright (C)  2017  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

import sys, os, tempfile

##
class CSVWriter(object):
    
    def __init__(self):
        return
    
    def get_csv_file(self, tmp_files_path):
        csv_file = None
        
        try:
            
            (file_desc, file_name) = tempfile.mkstemp(suffix="_csv", dir=tmp_files_path)
            
            csv_file = (file_desc, file_name)
            #csv_file = os.fdopen(file_desc, 'wb')
            
        except Exception:
            raise
        #finally:
            #csv_file.close()
        
        return csv_file

## END