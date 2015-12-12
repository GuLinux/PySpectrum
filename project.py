import json
import os
from PyQt5.QtCore import QDate, Qt

class Project:
    def __init__(self, path='', file=None):
        self.data = {}
        self.set_path(path)
        if self.path:
            with open(self.__projectfile()) as data_file:
                self.data = json.load(data_file)
        
    def set_path(self, path):
        self.path = path
    def get_path(self):
        return self.path
        
    def set_name(self, name):
        self.data['name'] = name
    def get_name(self):
        return self.data.get('name', '')
        
    def set_observer(self, observer):
        self.data['observer']= observer
    def get_observer(self):
        return self.data.get('observer', '')

    def set_position(self, position):
        self.data['position'] = position
    def get_position(self):
        return self.data.get('position', '')
        
    def set_date(self, date):
        self.data['date'] = date.toString(Qt.ISODate)
    def get_date(self):
        return QDate.fromString(self.data.get('date', QDate.currentDate().toString(Qt.ISODate)), Qt.ISODate)

    def set_equipment(self, equipment):
        self.data['equipment'] = equipment
    def get_equipment(self):
        return self.data.get('equipment', '')
        
    def get_raw_profiles(self):
        return self.data.get('raw_profiles', [])
    
    def get_calibrated_profiles(self):
        return self.data.get('calibrated_profiles', [])
    
    def get_finished_profiles(self):
        return self.data.get('finished_profiles', [])
    
    def get_instrument_responses(self):
        return self.data.get('instrument_responses', [])
    
    
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
        return json.dumps(self.data, sort_keys=False, indent=4)