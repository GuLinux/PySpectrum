import json

class Project:
    def __init__(self, name='', path='', file=None):
        self.name = name
        self.path = path
        if file:
            with open(file) as data_file:
                data = json.load(data_file)
                self.name = data['name']
                self.path = data['path']
                
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
        return "{}/project.json".format(self.path)
    
    def __to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)