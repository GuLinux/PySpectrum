import json
import os

class Project:
    def __init__(self, path='', file=None):
        self.path = path
        if path:
            with open(self.__projectfile) as data_file:
                data = json.load(data_file)
                self.name = data['name']
                self.path = data['path']
                
    def set_path(self, path):
        self.path = path
        
    def raw_profiles(self):
        pass
    
    def calibrated_profiles(self):
        pass
    
    def instrument_responses(self):
        pass
    
    def finished(self):
        pass
    
    def rotation_angle(self):
        pass
    
    def dispersion(self):
        pass
    
    def save(self):
        pass
    
    def __projectfile(self):
        return os.path.join(self.path, 'project.json')
    
    def __to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)