from PyQt5.QtCore import QStandardPaths
import os
import json
import urllib


class Miles:
    def __init__(self):
        json_file = open('data/miles.json', 'r')
        self.catalog = json.load(json_file)
        json_file.close()
        
    def fits(self, miles_number):
        cache_path = QStandardPaths.writableLocation(QStandardPaths.CacheLocation) + "/miles"
        file_path = "{}/s{}.fits".format(cache_path, miles_number)
        try:
            os.makedirs(cache_path)
        except FileExistsError:
            pass
        if not os.path.exists(file_path):
            
            remote_file = urllib.request.FancyURLopener()
            remote_file.retrieve("http://www.iac.es/proyecto/miles/media/stellar_libraries/MILES/s{}.fits".format(miles_number), file_path)
        return file_path