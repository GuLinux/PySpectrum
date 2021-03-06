import json
import os
from PyQt5.QtCore import QDate, QObject, Qt, pyqtSignal, QDateTime
from astropy.io import fits
from fits_spectrum import *
from qtcommons import *
from pyspectrum_commons import *
import numpy as np

class ProjectJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QDateTime):
            return {'datetime': obj.toString(Qt.ISODate)}
        return json.JSONEncoder.default(self, obj)

class ProjectJSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.decode_obj)

    def decode_obj(self, obj):
        if 'datetime' in obj and len(obj.keys()) == 1:
            return QDateTime.fromString(obj['datetime'], Qt.ISODate)
        return obj

class Project(QObject):
    RAW_PROFILE = 'raw_profiles'
    CALIBRATED_PROFILE = 'calibrated_profiles'
    FINISHED_PROFILES = 'finished_profiles'
    EXPORTED_IMAGES = 'exported_images'
    INSTRUMENT_RESPONSES = 'instrument_responses'
    
    filesChanged = pyqtSignal()
    
    def __init__(self, path='', file=None):
        QObject.__init__(self)
        self.data = {}
        self.set_path(path)
        if self.path:
            with open(self.__projectfile()) as data_file:
                self.data = json.load(data_file, cls=ProjectJSONDecoder)
            for _type in [Project.RAW_PROFILE, Project.CALIBRATED_PROFILE, Project.FINISHED_PROFILES, Project.INSTRUMENT_RESPONSES, Project.EXPORTED_IMAGES]:
                try:
                    os.makedirs(self.directory_path(_type))
                except FileExistsError:
                    pass
        
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
        return self.__get_files(Project.RAW_PROFILE)
    
    def get_calibrated_profiles(self):
        return self.__get_files(Project.CALIBRATED_PROFILE)
    
    def get_finished_profiles(self):
        return self.__get_files(Project.FINISHED_PROFILES)
    
    def get_instrument_responses(self):
        return self.__get_files(Project.INSTRUMENT_RESPONSES)
    
    def __get_files(self, _type, full_path = True):
        if not _type in self.data:
            self.data[_type] = []
        return [(f[0], self.file_path(_type, name=f[1]) if full_path else f[1]) for f in self.data[_type] if os.path.isfile(self.file_path(_type, name=f[1]))]
    
    def rotation_degrees(self):
        return self.__avg_from_files(FitsSpectrum.ROTATION, self.get_raw_profiles())
    
    def avg_dispersion(self):
        return self.__avg_from_files(FitsSpectrum.DISPERSION, self.get_calibrated_profiles())
    
    def __avg_from_files(self, header, files, default = None):
        data = [ fits.getheader(f[1])[header] for f in files]
        return np.mean(data) if len(data) else default
    
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
        return json.dumps(self.data, sort_keys=False, indent=4, cls=ProjectJSONEncoder)
    
    def file_path(self, _type, object_properties = None, name = None, bare_name = None):
        if not name:
            if bare_name:
                name = "{}.fit.gz".format(bare_name)
            if object_properties:
                name = "{}_{}.fit.gz".format(object_properties.name, object_properties.date.toString(Qt.ISODate))
        return os.path.join(self.directory_path(_type), name)
    
    def add_file(self, _type, on_added, object_properties = None, name = None, bare_name = None):
        file_path = self.file_path(_type, name=name, bare_name = bare_name, object_properties = object_properties)
        files = [f for f in self.__get_files(_type, full_path = False) if f[1] != file_path]
        files.append((QDateTime.currentDateTime(), os.path.basename(file_path)))
        
        self.data[_type] = sorted(files, key=lambda o: o[0], reverse=True)
        self.save()
        on_added(file_path)
        name = fits.getheader(file_path).get('OBJECT', os.path.basename(file_path))
        Notification('File {} saved in {}/{}'.format(name, self.get_name(), _type), title='File Saved', type='success', timeout=5)
        self.filesChanged.emit()
        return file_path
    
    def directory_path(self, _type):
        return os.path.join(self.path, _type)
