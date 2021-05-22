#!/usr/bin/env python3
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
from scipy.stats import pearsonr
from ser_header import SERHeader
        
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
        return np.inf, (-np.inf, +np.inf)
    return roots[-1]-roots[0], roots

def rotate(data, d, order=3, background = 0):
    return scipy.ndimage.interpolation.rotate(data, d, reshape=True, order=order, mode='constant', cval = background)

def spatial(data):
    return range(0, len(data)), data.sum(1)


def min_angle(data, background = 0, fmin=0, fmax=360):
    def get_data(deg):
        rotated = rotate(data, deg, background=background)
        fwhms = fwhm(rotated, 0.25)[0],fwhm(rotated, 0.78)[0]
        print('deg: {}, fwhm[base]: {}, fwhm[top]: {}'.format(deg, fwhms[0], fwhms[1]))
        return fwhms[1]-fwhms[0]
    return minimize_scalar(get_data, bounds=[fmin,fmax], method='bounded', tol=1e-10)

def calc_min_angle(data, background = 0, max_precision = False):    
    ratio = 1./max(data.shape[0]/100, data.shape[1]/100)
    find_angle = lambda range, ratio: sorted([(d, fwhm( rotate(scipy.ndimage.interpolation.zoom(data, ratio), d, background=background), 0.15)[0] ) for d in range], key=lambda a: a[1])[0][0]
    angle = find_angle(np.arange(0, 180, step=0.5), ratio)
    angle = find_angle(np.arange(angle-3, angle+3, step=0.1), min(ratio, 2.))
    angle = find_angle(np.arange(angle-1, angle+1, step=0.01), min(ratio, 3.))
    if max_precision:
        print("Using better precision for last step")
        angle = find_angle(np.arange(angle-0.05, angle+0.05, step=0.001), min(ratio, 5.))
    while angle < 0:
        angle += 360.
    while angle > 360:
        angle -= 360.
    return angle

def sorted_by_quality(images):
    return sorted(images, key=lambda i: i['quality'])

def print_progress_percent(current, total, fwhm, message=''):
    sys.stderr.write("\r{}{:.2f}% ({} of {}): {:.5f}".format(message, (current+1.)*100./total, current+1, total, fwhm) )
    sys.stderr.flush()
    
def name_with_suffix(name, suffix):
    fname_parts = list(os.path.splitext(name))
    fname_parts[0] = '{}{}'.format(fname_parts[0], suffix)
    return ''.join(fname_parts)    

def quality_by_fwhm(image, vindexes, reference_hcurve):
    qualities = fwhm(image[vindexes[0]:vindexes[1],:], 0.15), fwhm(image[vindexes[0]:vindexes[1],:], 0.75)
    return qualities[0][0]/qualities[1][0]
    
def quality_by_reference(image, vindexes, reference_hcurve):
    hcurve = image[vindexes[0]:vindexes[1],:].sum(0)
    offset_range = 50
    hindexes = (offset_range, len(hcurve)-offset_range)
    max_quality = (-np.inf, 0)
    reference=reference_hcurve[hindexes[0]:hindexes[1]]
    #print(hindexes)
    hrange = range(0, len(reference))

                               
    for offset in range(-int(offset_range/2), int(offset_range/2)):
        curve = hcurve[hindexes[0]+offset:hindexes[1]+offset]
        quality = pearsonr(reference, hcurve[hindexes[0]+offset:hindexes[1]+offset])
        if quality[0] > max_quality[1]:
            max_quality = (offset, quality[0])
    return 1.-max_quality[1]
    
def calc_qualities(sequence, limit = np.inf, reference = 0, max_angle_precision = False, print_progress = None, quality_calculator = None):
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
    hprofile = reference_image[indexes[0]:indexes[1],:].sum(0)
    
    for i in range(0, min(total_images, limit)):
        image = rotate(sequence.image(i), angle, background = background)
        image_quality = quality_calculator(image, indexes, hprofile)
        images.append({'index': i, 'quality': image_quality})
        if print_progress:
            print_progress(i, total_images, image_quality)
        #print("{}/{}: {}".format(i+1, total_images, _fwhm[0]))
    return images

parser = argparse.ArgumentParser(description='Calculates quality for spectrum images, and filters sequences according to them')
parser.add_argument('sequences', metavar='seq', type=str, nargs='+', help='sequence files to be evaluated')
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--perc', metavar='percentage', type=float, help='percent of frames to be kept for each sequence')
group.add_argument('-o', '--only-evaluate', dest='filter', action='store_const', const=False, default=True, help='No filter, just evaluate quality')
parser.add_argument('-r', '--reference', metavar='reference', type=int, help='use a reference frame for curves similarity calculation')
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
        if args['reference']:
            images = calc_qualities(sequence, reference = args['reference'], quality_calculator = quality_by_reference, max_angle_precision = True, print_progress = lambda c, t, f: print_progress_percent(c, t, f, message='{}: quality matching to reference: '.format(file) ))
        else:
            images = sorted_by_quality(calc_qualities(sequence, limit = 30, quality_calculator=quality_by_fwhm, print_progress = lambda c, t, f: print_progress_percent(c, t, f, message='{}: first phase: '.format(file) )))
            sys.stderr.write("\nFirst step done, improving precision\n")
            images = calc_qualities(sequence, reference = images[0]['index'], quality_calculator = quality_by_fwhm, max_angle_precision = True, print_progress = lambda c, t, f: print_progress_percent(c, t, f, message='{}: final phase: '.format(file) ))
            sys.stderr.write('\n')
            sys.stderr.flush()
        
    images = sorted_by_quality(images)
    with open(indexes_filename, 'w') as indexes_file:
        json.dump(images, indexes_file, indent=2)

    if args['filter']:
        images_selection =int(len(images) / (100./args['perc']))
        best = images[0:images_selection]
        
        bestfile = name_with_suffix(file, '_best{}'.format(len(best)))
        sequence.write(bestfile, images[0:images_selection])
        with open(bestfile+'.qualities', 'w') as qualities:
            json.dump(best, qualities, indent=2)
        print('Wrote ' + bestfile)

        worst = images[images_selection:]
        worstfile = name_with_suffix(file, '_worst{}'.format(len(worst)))
        sequence.write(worstfile, worst)
        with open(worstfile+'.qualities', 'w') as qualities:
            json.dump(worst, qualities, indent=2)
        print('Wrote ' + worstfile)