import json
import os
from PyQt5.QtCore import QDate, Qt

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
                self.set_date(QDate.fromString(data['date'], Qt.ISODate))
                self.set_equipment(data['equipment'])
                self.raw_profiles = data['raw_profiles']
                self.calibrated_profiles = data['calibrated_profiles']
                self.instrument_responses = data['instrument_responses']
                self.finished_profiles = data['finished_profiles']
                
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
        return json.dumps({
            'name': self.name,
            'date': self.date.toString(Qt.ISODate),
            'observer': self.observer,
            'position': self.position,
            'equipment': self.equipment,
            'raw_profiles': self.raw_profiles,
            'calibrated_profiles': self.calibrated_profiles,
            'instrument_responses': self.instrument_responses,
            'finished_profiles': self.finished_profiles,
            }, sort_keys=False, indent=4)