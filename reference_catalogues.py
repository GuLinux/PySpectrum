from PyQt5.QtCore import QStandardPaths
import os
import json
import urllib.request
import gzip
import collections

class ReferenceCatalogues:
    def __init__(self, database):
        self.database = database
        c = database.cursor()
        cats = c.execute('SELECT id, "table", "name", spectra_url, gzipped, file_column, sptype_column FROM spectra_catalogues ORDER BY id ASC')
        self.catalogues = collections.OrderedDict([(c[2], {'id':c[0],'table':c[1],'name':c[2],'url':c[3],'gzipped':c[4]==1, 'columns': {'sptype': c[6], 'file':c[5]} }) for c in cats])
        
    def spectra(self, catalog):
        cat_info = self.catalogues[catalog]
        query = "SELECT {0}, {1} FROM {2} WHERE {1} <> '' ORDER BY {1} ASC".format(cat_info['columns']['file'], cat_info['columns']['sptype'], cat_info['table'])
        c = self.database.cursor()
        return [{'catalog': catalog, 'sptype': r[1], 'file': r[0]} for r in c.execute(query)]
    
    def fits(self, entry):
        catname = entry['catalog']
        catalog = self.catalogues[catname]
        return ReferenceCatalogues.get_fits(catname, entry['file'], catalog['url'], catalog['gzipped'])
        
    def get_fits(catname, filename, url, is_gzipped):
        cache_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.CacheLocation), catname)
        file_path = os.path.join(cache_path, '{}.gz'.format(cache_path, filename))
        try:
            os.makedirs(cache_path)
        except FileExistsError:
            pass
        if not os.path.exists(file_path):
            if is_gzipped:
                urllib.request.urlretrieve(url.format("{}.gz".format(filename)), file_path )
            else:
                request = urllib.request.urlopen(url.format(filename))
                with gzip.open(file_path, 'wb') as f:
                    f.write(request.read())
        return file_path