#!/usr/bin/python3
import struct
import os
import sys
import array
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage.interpolation
from scipy.interpolate import UnivariateSpline
from scipy.optimize import *
import copy
import json
import argparse

class SERHeader(object):
    FORMAT = '=14siiiiiii40s40s40sqq'
    SIZE=178
    def __init__(self, data):
        self.unpacked = struct.unpack(SERHeader.FORMAT, data)
        self.color_id = self.unpacked[2]
        self.width = self.unpacked[4]
        self.height = self.unpacked[5]
        self.depth = self.unpacked[6]
        self.frames = self.unpacked[7]
        self.observer = self.unpacked[8].decode().strip()
        self.instrument = self.unpacked[9].decode().strip()
        self.telescope = self.unpacked[10].decode().strip()
    def __str__(self):
        return 'frames: {}; size: {}x{}, depth: {}, planes: {}, frame bytes: {}, observer: {}, instrument: {}, telescope: {}'.format(
            self.frames, self.width, self.height, self.depth, self.planes(), self.frame_bytes(), self.observer, self.instrument, self.telescope
            )
    
    def planes(self):
        return 1 if self.color_id < 20 else 3
    
    def frame_bytes(self):
        return self.width * self.height * self.planes() * (1 if self.depth == 8 else 2)
    
    def pack(self):
        return struct.pack(SERHeader.FORMAT, self.unpacked[0], self.unpacked[1], self.color_id, self.unpacked[3], self.width, self.height, self.depth, self.frames, 
                           self.observer.encode(), self.instrument.encode(), self.telescope.encode(), self.unpacked[11], self.unpacked[12])
    
        
class SERSequence(object):
    def __init__(self, file):
        self.file = open(file, 'rb')
        self.header = SERHeader(self.file.read(SERHeader.SIZE))
        print(self.header)
    def images(self):
        return self.header.frames
    
    def image(self, index):
        b = self.header.frame_bytes()
        self.file.seek(SERHeader.SIZE + index*b)
        data = self.file.read(b)
        return np.array(array.array('B' if self.header.depth == 8 else 'H', data)).reshape(self.header.height, self.header.width)
    
    def write(self, newfile, images):
        header = copy.deepcopy(self.header)
        header.frames = len(images)
        f = open(newfile, 'wb')
        f.write(header.pack())
        for image in images:
            f.write(self.image(image['index']))
        f.close()

def fwhm(data, ypos=0.5):
    spatial = data.sum(1)
    spatial = spatial-np.min(spatial)
    spatial_range = range(0, len(spatial))
    spline = UnivariateSpline(spatial_range, (spatial -np.max(spatial)*ypos), s=0.1, k=3)
    roots = spline.roots()
    if len(roots) < 2:
        return np.inf
    return roots[-1]-roots[0], roots

def rotate(data, d, order=3, background = 0):
    return scipy.ndimage.interpolation.rotate(data, d, reshape=True, order=order, mode='constant', cval = background)

def spatial(data):
    return range(0, len(data)), data.sum(1)


def min_angle(data, background = 0, fmin=0, fmax=360):
    get_data = lambda d: fwhm(rotate(data, d, background=background))[0]
    return minimize_scalar(get_data, bracket=[fmin,fmax], method='brent', options={'xtol': 1e-10})

def calc_min_angle(data, background = 0, max_precision = False):    
    ratio = 1./max(data.shape[0]/100, data.shape[1]/100)
    angle = min_angle(scipy.ndimage.interpolation.zoom(data, ratio), background, fmin=0, fmax=180)
    angle = min_angle(scipy.ndimage.interpolation.zoom(data, min(ratio, 2.)), background, fmin=angle.x - 3, fmax=angle.x + 3)
    angle = min_angle(scipy.ndimage.interpolation.zoom(data, min(ratio, 4.)), background, fmin=angle.x - 1, fmax=angle.x + 1)
    if max_precision:
        print("Using better precision for last step")
        angle = min_angle(scipy.ndimage.interpolation.zoom(data, min(ratio, 8.)), background, fmin=angle.x - 1, fmax=angle.x + 1)
    angle = angle.x
    while angle < 0:
        angle += 360.
    while angle > 360:
        angle -= 360.
    return angle

def sorted_by_quality(images):
    return sorted(images, key=lambda i: i['quality'])

def print_progress_percent(current, total, fwhm, message=''):
    sys.stderr.write("\r{}{:.2f}% ({} of {}): {:.2f}".format(message, (current+1.)*100./total, current+1, total, fwhm) )
    sys.stderr.flush()

def calc_qualities(sequence, limit = np.inf, reference = 0, max_angle_precision = False, print_progress = None):
    images = []
    reference_image = sequence.image(reference)
    background = np.median(reference_image)
    angle = calc_min_angle(reference_image, background, max_precision = max_angle_precision)
    print("Rotation angle: {} (max precision: {})".format(angle, max_angle_precision))
    reference_image = rotate(reference_image, angle, background=background)
    img_fwhm = fwhm(reference_image)
    roots = img_fwhm[1][0],img_fwhm[1][-1]
    distance = (roots[1]-roots[0])
    indexes = roots[0]-distance*4, roots[1]+distance*4
    total_images = sequence.images()
    
    for i in range(0, min(total_images, limit)):
        image = rotate(sequence.image(i), angle, background = background)
        _fwhm = fwhm(image[indexes[0]:indexes[1],:])
        images.append({'index': i, 'quality': _fwhm[0]})
        if print_progress:
            print_progress(i, total_images, _fwhm[0])
        #print("{}/{}: {}".format(i+1, total_images, _fwhm[0]))
    return images

parser = argparse.ArgumentParser(description='Calculates quality for spectrum images, and filters sequences according to them')
parser.add_argument('sequences', metavar='seq', type=str, nargs='+', help='sequence files to be evaluated')
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--perc', metavar='percentage', type=float, help='percent of frames to be kept for each sequence')
group.add_argument('-o', '--only-evaluate', dest='filter', action='store_const', const=False, default=True, help='No filter, just evaluate quality')
args = vars(parser.parse_args())

for file in args['sequences']:
    sequence = SERSequence(file)
    indexes_filename = '{}.qualities'.format(file)

    images = []
    try:
        with open(indexes_filename, 'r') as indexes_file:
            images = json.load(indexes_file)
            print('Using indexes file {}, to recalculate indexes just delete it'.format(indexes_filename))
    except FileNotFoundError:
        images = sorted_by_quality(calc_qualities(sequence, limit = 30, print_progress = lambda c, t, f: print_progress_percent(c, t, f, message='{}: first phase: '.format(file) )))
        print("First step done, improving precision")
        images = calc_qualities(sequence, reference = images[0]['index'], max_angle_precision = True, print_progress = lambda c, t, f: print_progress_percent(c, t, f, message='{}: final phase: '.format(file) ))
        sys.stderr.write('\n')
        sys.stderr.flush()
        
    images = sorted_by_quality(images)
    with open(indexes_filename, 'w') as indexes_file:
        json.dump(images, indexes_file)

    if args['filter']:
        images_selection =int(len(images) / (100./args['perc']))
        fname_parts = list(os.path.splitext(file))
        fname_parts[0] = '{}_best{}'.format(fname_parts[0], images_selection)
        newfile = ''.join(fname_parts)
        sequence.write(newfile, images[0:images_selection])
        print('Wrote ' + newfile)