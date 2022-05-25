import numpy as np
import datetime
import csv
import face_recog

lastIds = []
lastNames = []
cachedNames = {}

def identifyFaceFromEmployees(person):
    name = face_recog.identify(person["cutout"], str(person["id"]))
    global cachedNames
    cachedNames[person["id"]] = name
    return name

def getCachedNameIfAny(person):
    id = person["id"]
    global cachedNames
    if id in cachedNames and cachedNames[id] != 'No Face' and cachedNames[id] != 'Unknown':
        return cachedNames[id]
    else:
        return identifyFaceFromEmployees(person)

def process(outputs):
    
    ids = [entry["id"] for entry in outputs]
    names = [getCachedNameIfAny(entry) for entry in outputs]
    

    # declare global variable
    global lastIds
    global lastNames  
    global cachedNames

    if(checkEqualityTwoArrays(ids, lastIds) == False or checkEqualityTwoArrays(names, lastNames) == False):
        handleChange(names)
        lastIds = ids
        lastNames = names


def handleChange(names):
    namesStr = 'No person'

    if(len(names) != 0):
        namesStr = ';'.join(names)
    
    with open('./data.csv', 'a', newline='') as f:
        current_time = datetime.datetime.now()
        writer = csv.writer(f)
        writer.writerow([current_time, namesStr])

def checkEqualityTwoArrays(a, b):
    return np.array_equal(a, b)

