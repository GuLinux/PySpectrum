import json
import os
from PyQt5.QtCore import QDate

class Project:
    def __init__(self, path='', file=None):
        self.set_path(path)
        self.__init_fields()
        if self.path:
            with open(self.__projectfile()) as data_file:
                data = json.load(data_file)
                self.set_path(data['path'])
                self.set_name(data['name'])
                self.set_observer(data['observer'])
                self.set_date(data['date'])
                self.set_equipment(data['equipment'])
                
    def __init_fields(self):
        self.name = self.observer = self.position = self.equipment = ''
        self.date = QDate.currentDate()
        self.raw_profiles = []
        self.calibrated_profiles = []
        self.instrument_responses = []
        self.finished_profiles = []
        
    def set_path(self, path):
        self.path = path
        
    def set_name(self, name):
        self.name = name
        
    def set_observer(self, observer):
        self.observer = observer

    def set_position(self, position):
        self.position = position
        
    def set_date(self, date):
        self.date = date
        
    def set_equipment(self, equipment):
        self.equipment = equipment
        
    def rotation_angle(self):
        pass
    
    def dispersion(self):
        pass
    
    def save(self):
        with open(self.__projectfile(), 'w') as data_file:
            data_file.write(self.__to_JSON())
    
    def __projectfile(self):
        return os.path.join(self.path, 'project.json')
    
    def __to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)