#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FormsFactory.py is part of Barleymap web app.
# Copyright (C) 2017  Carlos P Cantalapiedra.
# (terms of use can be found within the distributed LICENSE file).

#import sys

class FormsFactory(object):
    
    @staticmethod
    def get_retrieve_form_new(query = "", sets = "", start = -1, end = -1,
                              maxmiss = 1.0, maxhets = 1.0, maf = 0.0, type_query = "contig"):
        
        form = RetrieveForm()
        
        form.set_parameters(query, sets, start, end, maxmiss, maxhets, maf, type_query)
        
        return form
    
    @staticmethod
    def get_find_form_empty(DEFAULT_GENES_WINDOW_CM, DEFAULT_GENES_WINDOW_BP, DEFAULT_MAPS):
        
        find_form = FindForm()
        
        return find_form
    
    @staticmethod
    def get_find_form_session(session):
        find_form = None
        
        find_form = FindForm.init_from_session(session)
        
        return find_form

class InputForm(object):
    
    ACTION = "action"
    SESSION = "session_token"
    QUERY = "query"
    SETS = "sets"
    
    _action = ""
    _query = ""
    _sets = ""
    _start = -1
    _end = -1
    _maxmiss = 1.0
    _maxhets = 1.0
    _maf = 0.0
    _type_query = "contig"
    
    _is_empty = True
    
    def get_action(self, ):
        return self._action
    
    def set_action(self, action):
        self._action = action
    
    def get_query(self):
        return self._query
    
    def set_query(self, query):
        self._query = query
    
    def get_sets(self, ):
        return self._sets
    
    def set_sets(self, sets):
        self._sets = sets
    
    def set_start(self, start):
        self._start = start
    
    def get_start(self,):
        return self._start
    
    def set_end(self, end):
        self._end = end
    
    def get_end(self,):
        return self._end
    
    def set_maxmiss(self, maxmiss):
        self._maxmiss = maxmiss
    
    def get_maxmiss(self,):
        return self._maxmiss
    
    def set_maxhets(self, maxhets):
        self._maxhets = maxhets
        
    def get_maxhets(self,):
        return self._maxhets
    
    def set_maf(self, maf):
        self._maf = maf
        
    def get_maf(self,):
        return self._maf
    
    def set_type_query(self, type_query):
        self._type_query = type_query
    
    def get_type_query(self,):
        return self._type_query
    
    def set_session_input_form(self, session):
        
        session[self.SESSION] = self.SESSION
        session[self.ACTION] = self._action
        
        session[self.QUERY] = self.get_query()
        session[self.SETS] = self.get_sets()
        
        return
    
    @staticmethod
    def init_from_session(session, form):
        
        if session[form.ACTION] == form.get_action():
            form._query = session.get(form.QUERY)
        else: # Comes from find action
            form._query = ""
        
        form._sets = session.get(form.SETS)
        
        form._is_empty = False
        
        if session[form.ACTION] == "index":
            form.set_action("index")
        
        return form
    
    def set_parameters(self, query = "", sets = "", start = -1, end = -1,
                       maxmiss = 1.0, maxhets = 1.0, maf = 0.0, type_query = "contig"):
        form = self
        
        form.set_query(query)
        form.set_sets(sets)
        form.set_start(start)
        form.set_end(end)
        form.set_maxmiss(maxmiss)
        form.set_maxhets(maxhets)
        form.set_maf(maf)
        form.set_type_query(type_query)
        
        return
    
    def as_params_string_input_form(self, ):
        ret_value = []
        
        ret_value.append("Sets: "+",".join(self.get_sets()))
        
        return "\n".join(ret_value)

class RetrieveForm(InputForm):
    
    _action = "retrieve"
    
    def __init__(self):
        pass
    
    @staticmethod
    def init_from_session(session):
        
        new_form = RetrieveForm()
        
        InputForm.init_from_session(session, new_form)
        
        return new_form
    
    def set_session(self, session):
        
        self.set_session_input_form(session)
        
        return
    
    def as_params_string(self, ):
        ret_value = []
        
        ret_value.append(self.as_params_string_input_form())
        
        return "\n".join(ret_value)

## END
