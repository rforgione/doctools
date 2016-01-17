class MDVars(object):
    
    _md_vars = {}
    
    def __init__(self):
        pass
    
    def add_var(self, var_name, var_dict):
        assert type(var_dict) == dict, """var_dict argument must be a dictionary."""
        assert sorted(var_dict.keys()) == ['form_func', 'value'], """
            var_dict argument must follow schema {'value': ##some value##, 'form_func': ##some formatting function(s)##}"""
        # check to see if the number of formatting functions matches the value passed
        # i.e. dataframes should have a dict with one formatting func per column
        # single numbers should have a single func, etc.
        
        self._md_vars[var_name] = var_dict
        
    def get_var(self, var_name, formatted=False):
        assert var_name in self._md_vars.keys(), "No variable stored with the name %s." % var_name
        
        if formatted:
            if MDVars.is_df(self._md_vars[var_name]['value']):
                var_data = copy.deepcopy(self._md_vars[var_name])
                
                for col in var_data['value'].columns:
                    
                    # skip the iteration if no formatting function is passed
                    if var_data['form_func'][col] == None:
                        continue
                        
                    var_data['value'][col] = var_data['value'][col].apply(var_data['form_func'][col])
                    
                return var_data['value']
            else:
                var_data = self._md_vars[var_name]
                return var_data['form_func'](var_data['value'])
        else:
            return self._md_vars[var_name]['value']

    @staticmethod
    def is_df(obj):
        return type(obj) == pd.core.frame.DataFrame
    
    def get_final_dict(self):
        return {k:self.get_var(k, True).to_html() if MDVars.is_df(self.get_var(k,True))
                    else self.get_var(k, True)
                    for k in self._md_vars.keys()}
        