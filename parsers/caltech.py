from dataset import DataSetMulti
from objects import BoundingBox
import os
import os.path

data_type = "images"

name = "CaltechParser"

def describe():
    return "Parser for the Caltech results."

def recognize(file):
    return False

def get_object(data, i):
    xmin, xmax, ymin, ymax = None, None, None, None
    object_char = data.find("object %d"%(i,))
    while object_char != -1:
        begin_line = data[:object_char].rfind("\n") + 1
        end_line = begin_line+1 + data[begin_line+1:].find("\n")
        line = data[begin_line:end_line]
        if line.find("Bounding box") != -1:
            # if this happens, there are other objects than pedestrians in the annotation :
            assert(line.find("PASperson") != -1)
            box_begin = line.rfind(":") + 1
            box_str = line[box_begin:]
            box_str = box_str[box_str.find("(")+1:].strip()
            xmin = int(box_str[:box_str.find(",")].strip().rstrip())
            box_str = box_str[box_str.find(",")+1:].strip()
            ymin = int(box_str[:box_str.find(")")].strip().rstrip())
            box_str = box_str[box_str.find("(")+1:].strip()
            xmax = int(box_str[:box_str.find(",")].strip().rstrip())
            box_str = box_str[box_str.find(",")+1:].strip()
            ymax = int(box_str[:box_str.find(")")].strip().rstrip())
            break
        object_char = object_char+1 + data[object_char+1:].find("object %d"%(i,))
    if xmin == None:
        return None
    return BoundingBox(xmin, ymin, xmax, ymax)

def parse_file_multi(file, filename, dataset):
    for line in file:
        (x, y, w, h, score) = tuple([float(a) for a in line.strip().rstrip().split(",")])
        dataset.add_obj(score, filename, BoundingBox(x, y, x+w, y+h))

def parse_multi(path):
    ret = DataSetMulti()
    filenames = os.listdir(path)
    for filename in filenames:
        #TODO : check validity
        file = open(os.path.join(path, filename), "r")
        parse_file_multi(file, filename, ret)
        file.close()
    print ret
    return ret
