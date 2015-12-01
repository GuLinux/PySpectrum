#!/usr/bin/python3
from astropy.io import fits
import sqlite3
import sys
import numpy as np

# L: Logical (Boolean)
# B: Unsigned Byte
# I: 16-bit Integer
# J: 32-bit Integer
# K: 64-bit Integer
# E: Single-precision Floating Point
# D: Double-precision Floating Point
# C: Single-precision Complex
# M: Double-precision Complex
# A: Character

for t in (np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64):
    sqlite3.register_adapter(t, int)
for t in (np.float16, np.float32, np.float64, np.float128):
    sqlite3.register_adapter(t, float)

def file2table(filename, hdu, tablename, database, create_table = True):
    fits_file = fits.open(filename)
    table = fits_file[hdu]
    codes = {'L': 'INTEGER', 'B': 'BLOB', 'I': 'INTEGER', 'J': 'INTEGER', 'K': 'INTEGER', 'E': 'REAL', 'D': 'REAL', 'A': 'TEXT'}
    conn = sqlite3.connect(database)
    c = conn.cursor()
    column_names = [c.name.replace('-', '_') for c in table.columns]
    if create_table:
        columns = ["{} {}".format(column.name.replace('-', '_'), codes[column.format[-1]]) for column in table.columns]
        query="CREATE TABLE {} ({});".format(tablename, ", ".join(columns))
        print("Creating table with query:")
        print(query)
        c.execute(query)
        print("\n")
    query = "INSERT INTO {} ({}) VALUES({});".format(tablename, ', '.join(column_names), ', '.join(['?']*len(table.columns)))
    print("Adding data with query: ")
    print(query)
    c.executemany(query, table.data)
    conn.commit()