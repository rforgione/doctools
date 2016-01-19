import pandas as pd
import numpy as np
from copy import deepcopy

class MDVars(object):
    
    _md_vars = {}
    
    def __init__(self):
        pass
    
    def add_var(self, var_name, var_dict):
        assert type(var_dict) == dict, """var_dict argument must be a dictionary."""
        
        if MDVars.is_df(var_dict["value"]):
            assert sorted(var_dict.keys()) == ['form_func', 'index', 'value'], """
                For a DataFrame object, var_dict must follow schema 'value', 'form_func', 'index'."""
        else:
            assert sorted(var_dict.keys()) == ['form_func', 'value'], """
                For numerical objects, var_dict must follow schema 'value', 'form_func'."""

        # check to see if the number of formatting functions matches the value passed
        # i.e. dataframes should have a dict with one formatting func per column
        # single numbers should have a single func, etc.
        
        self._md_vars[var_name] = var_dict         
        
    def get_var(self, var_name, formatted=False):
        assert var_name in self._md_vars.keys(), "No variable stored with the name %s." % var_name
        
        if formatted:
            if MDVars.is_df(self._md_vars[var_name]['value']):
                var_data = deepcopy(self._md_vars[var_name])
                
                for col in var_data['form_func'].keys():
                    
                    # skip the iteration if no formatting function is passed
                    if var_data['form_func'][col] == None:
                        continue
                        
                    var_data['value'][col] = var_data['value'][col].apply(var_data['form_func'][col])
                    
                return var_data['value'].to_html(index=var_data['index'])
            else:
                var_data = self._md_vars[var_name]
                return var_data['form_func'](var_data['value'])
        else:
            if MDVars.is_df(self._md_vars[var_name]['value']):
                return self._md_vars[var_name]['value'].to_html(index=self._md_vars[var_name]['index'])
            else:
                return self._md_vars[var_name]['value']

    @staticmethod
    def is_df(obj):
        return type(obj) == pd.core.frame.DataFrame
    
    def get_final_dict(self):
        return {k:self.get_var(k, True) for k in self._md_vars.keys()}
        