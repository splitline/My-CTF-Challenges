#!/usr/local/bin/python3
import pickle, collections, io

class RestrictedUnpickler(pickle.Unpickler): 
     def find_class(self, module, name): 
        if module == 'collections' and '__' not in name:
            return getattr(collections, name)
        raise pickle.UnpicklingError('bad')

data = bytes.fromhex(input("(hex)> "))
RestrictedUnpickler(io.BytesIO(data)).load()
