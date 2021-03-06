# Copyright (C) 2010 Michael Mathieu <michael.mathieu@ens.fr>
# 
# This file is part of visiongrader.
# 
# visiongrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# visiongrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with visiongrader.  If not, see <http://www.gnu.org/licenses/>.
# 
# Authors :
#  Michael Mathieu <michael.mathieu@ens.fr>

import sys
#sys.path.insert(0, '/home/sermanet/installed/matplotlib/matplotlib-1.0.0/build/lib.linux-x86_64-2.4/')
import pylab
#import matplotlib
import cPickle
import measures

################################################################################
def print_ROC(multi_result, n_imgs, save_filename = None, show_curve = True,
              xmin = None, ymin = None, xmax = None, ymax = None,
              grid_major = False, grid_minor = False):
    points = []
    n_imps = float(n_imgs)
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        fn = float(result.n_false_negatives())
        #n_imgs = float(len(result.images))
        points.append((fp / n_imgs, tp / (tp + fn)))
    points.sort()
    if save_filename != None:
        f = open(save_filename, "w")
        cPickle.dump(points, f)
        f.close()
    if show_curve:
        pylab.semilogx([a[0] for a in points], [a[1] for a in points])
        if xmin != None:
            pylab.axis(xmin = xmin)
        if xmax != None:
            pylab.axis(xmax = xmax)
        if ymin != None:
            pylab.axis(ymin = ymin)
        if ymax != None:
            pylab.axis(ymax = ymax)
        pylab.xlabel("False positives per image (FPPI)")
        pylab.ylabel("Detection rate")
        pylab.show()

################################################################################
# DET
        
# Interpolate and return the y value at xtarget, given the initial
# values at x0 and x1 which must be on each side of xtarget.
# Then find the closest points on each side of xtarget in matrix points,
# and interpolate.
def interpolate(xtarget, x0, y0, x1, y1, points):
    if x0 > xtarget or x1 < xtarget:
        raise Exception('expected x0 < xtarget and x1 > xtarget')
    for a in points:
        x = a[0]
        y = -a[1]
        if (x > x0 and x <= xtarget):
          x0 = x
          y0 = y
        if (x < x1 and x >= xtarget):
          x1 = x
          y1 = y
    if (x0 == xtarget):
        return y0
    if (x1 == xtarget):
        return y1
    # we found closest points around target, interpolate
    return y0 + (y1 - y0) * (xtarget - x0) / (x1 - x0)
        
def print_DET(multi_result, n_imgs, save_filename = None, show_curve = True,
              xmin = None, ymin = None, xmax = None, ymax = None,
              grid_major = False, grid_minor = False):
    print "Printing DET curve with xmin: " + str(xmin) + " xmax: " + str(xmax) \
        + " ymin: " + str(ymin) + " ymax: " + str(ymax)
    points = []
    n_imgs = float(n_imgs)
    # each result is defined for a given threshold
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        fn = float(result.n_false_negatives())
        #n_imgs = float(len(result.images))
        #the "-" is a trick for sorting
        points.append((max(xmin, fp / n_imgs), - fn / (tp + fn)))
    points.sort()
    # interpolate value at 100FPPI
    y = 100 * interpolate(100.0, 0, 1, 1000, 10000, points)
    print "miss rate at 100FPPI=" + "%.2f%%"%y
    # interpolate value at 10FPPI
    y = 100 * interpolate(10.0, 0, 1, 1000, 10000, points)
    print "miss rate at 10FPPI=" + "%.2f%%"%y
    # interpolate value at 1FPPI
    y = 100 * interpolate(1.0, 0, 1, 1000, 10000, points)
    print "miss rate at 1FPPI=" + "%.2f%%"%y
    # interpolate value at .001FPPI
    y = 100 * interpolate(.01, 0, 1, 1000, 10000, points)
    print "miss rate at .01FPPI=" + "%.2f%%"%y
    # get area under curve percentage in 0-100
    x0 = 0
    y0 = 1
    x1 = 100
    auc = measures.auc_percent(points, x0, y0, x1);
    print "area under curve in range [" + str(x0) + ", " + str(x1) + "]: " \
        + "AUC" + str(x0) + "-" + str(x1) + "=" + str(auc) + "%"
    # get area under curve percentage in 0-10
    x0 = 0
    y0 = 1
    x1 = 10
    auc = measures.auc_percent(points, x0, y0, x1);
    print "area under curve in range [" + str(x0) + ", " + str(x1) + "]: " \
        + "AUC" + str(x0) + "-" + str(x1) + "=" + str(auc) + "%"
    # get area under curve percentage in 0-1
    x0 = 0
    y0 = 1
    x1 = 1
    auc = measures.auc_percent(points, x0, y0, x1);
    print "area under curve in range [" + str(x0) + ", " + str(x1) + "]: " \
        + "AUC" + str(x0) + "-" + str(x1) + "=" + str(auc) + "%"
#     # get total area under curve
#     auc = measures.auc_percent(points, x0, y0, x1);
#     print "area under curve in range [" + str(x0) + ", " + str(x1) + "]: " \
#         + "AUC" + str(x0) + "-" + str(x1) + "=" + str(auc) + "%"    
    # save curve
    if save_filename != None:
        f = open(save_filename, "w")
        cPickle.dump(points, f)
        f.close()
    #TODO : params
    if show_curve:
        pylab.loglog([a[0] for a in points], [- a[1] for a in points])
        if xmin != None:
            pylab.axis(xmin = xmin)
        if xmax != None:
            pylab.axis(xmax = xmax)
        if ymin != None:
            pylab.axis(ymin = ymin)
        if ymax != None:
            pylab.axis(ymax = ymax)
        pylab.xlabel("False positives per image (FPPI)")
        pylab.ylabel("Miss rate")
        if grid_major:
            pylab.grid(True, which='major')
        if grid_minor:
            pylab.grid(True, which='minor')
        pylab.show()



################## old : ####################
        
def print_ROC_posneg(multi_result):
    raise NotImplementedError() #TODO : do not use
    prints = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        tn = float(result.n_true_negatives())
        fn = float(result.n_false_negatives())
        points.append((fp / (fp + tn), tp / (tp + fn)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()

def print_DET_posneg(multi_result):
    raise NotImplementedError() #TODO : do not use
    points = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        tn = float(result.n_true_negatives())
        fn = float(result.n_false_negatives())
        #the "-" is a trick for sorting
        points.append((fp / (fp + tn), - fn / (tp + fn)))
    points.sort()
    print points
    pylab.plot([a[0] for a in points], [- a[1] for a in points])
    pylab.show()
