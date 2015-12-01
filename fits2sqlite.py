#!/usr/bin/python3
from astropy.io import fits
#import sqlite3
import sys

fits_file = fits.open(sys.argv[1])
try:
    table = fits_file[sys.argv[2]]
except KeyError:
    table = fits_file[int(sys.argv[2])]
print(table.columns)
