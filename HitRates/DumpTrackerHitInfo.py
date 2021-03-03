#!/usr/bin/env python
"""
------------------------------------------------------------------------

A script to read in simulated MEGALib events & store infomation as pandas dataframes.

Author: Henrike Fleischhack (fleischhack@cua.edu)
Date: Feb 17th, 2021

------------------------------------------------------------------------
"""

import os
import time
import sys
import numpy
import glob
import pandas
import math

import gzip

from matplotlib import pyplot

import ROOT

#This is needed to get access to MEGAlib internal classes
ROOT.gSystem.Load("$(MEGALIB)/lib/libMEGAlib.so")
G = ROOT.MGlobal()
G.Initialize()

#We can use the following to make printing of MEGAlib (and other root classes) easier.
def MegaPrint(self):
    try:
        return self.Data()
    except:
        return ":("
    
def MegaToStringPrint(self):
    try:
        return self.ToString().Data()
    except:
        return ":("

def MegaNamePrint(self):
    try:
        return self.GetName().Data()
    except:
        return ":("

setattr(ROOT.MString, '__str__', MegaPrint)
setattr(ROOT.MVector, '__str__', MegaToStringPrint)
setattr(ROOT.MSimHT, '__str__', MegaToStringPrint)
setattr(ROOT.MSimIA, '__str__', MegaToStringPrint)
setattr(ROOT.MComptonEvent, '__str__', MegaToStringPrint)
setattr(ROOT.MPairEvent, '__str__', MegaToStringPrint)
setattr(ROOT.MPhysicalEvent, '__str__', MegaToStringPrint)
setattr(ROOT.MDDetector, '__str__', MegaNamePrint)
setattr(ROOT.MDVoxel3D,  '__str__', MegaNamePrint)
setattr(ROOT.MDStrip2D,  '__str__', MegaNamePrint)

#Now, we can print e.g. a MSimHT object to screen without having to call "ToString().Data()" each time.



def MegaSimEventToDict(Event, Geometry, TimeOffset = 0):
    '''
    Extract some information  from a MEGAlib event.
    Parameters:
        Event: A MEGAlib MSimEvent object.
        Geometry: A MEGAlib MDGeometryQuest object.
        TimeOffset (double): An optional time offset to add to each event time.
    Returns:
        a list of dictionaries, each containing information (x,y,z,time,energy) about one tracker hit.
    '''
    
    thePixelHits = []
    
    #In MEGAlib convention, GetICOrigin() is the "vector" of the original particle or gamma "towards the detector".
    #Multiplied by -1, this is the vector "to the source".
    #Meaning, theta=0 would correspond to a particle from zenith (top of the detector),
    #theta=90 degrees is a particle from the side,
    #theta=180 degrees is a particle from the bottom (albedo).
    #(I THINK)
    initialParticleDirection = -1*Event.GetICOrigin()
    
    #this is the position at which the particle is injected/initialized, not the first interaction
    initialPosition = Event.GetIAAt(0).GetPosition()
    
    #loop over simulated hits
    for iH in range(0, Event.GetNHTs()):
        theHit = Event.GetHTAt(iH)
        
        detectorType = theHit.GetDetector()
        
        if detectorType == 1: #strip type detector
            hitDict = {}
            hitDict["EventID"] = Event.GetID()
            hitDict["Time"] = Event.GetTime().GetAsDouble() + TimeOffset
            hitPos = theHit.GetPosition()

            hitDict["HitX"] = hitPos.GetX()
            hitDict["HitY"] = hitPos.GetY()
            hitDict["HitZ"] = hitPos.GetZ()
            hitDict["HitEnergyMeV"] = theHit.GetEnergy()/1e3 #Energy deposit given in keV, convert to MeV
            
            hitDict["InitialTheta"] = initialPhotonDirection.Theta()
            hitDict["InitialPhi"] =  initialPhotonDirection.Phi()
            hitDict["InitialX"] = initialPosition.GetX()
            hitDict["InitialY"] = initialPosition.GetY()
            hitDict["InitialZ"] = initialPosition.GetZ()
            

            #These two aren't really helpfull, just for illustration.
            #hitDict["HitDetector"] = Geometry.GetDetector( theHit.GetPosition() ).GetName().Data()
            #hitDict["HitVolume"] = Geometry.GetVolume( theHit.GetPosition() ).GetName().Data()

            thePixelHits.append( hitDict )
               
    return thePixelHits


def readSimFile( FileName, GeometryName, MaxTime=None, TimeOffset=0 ):
    '''
    Extract information  from a MEGAlib sim file and return as pandas DataFrame.
    Parameters:
        FileName: Input file path. Can be a .sim file or a .sim.gz file.
        GeometryName: Input geometry path
        MaxTime: Optional; if not None: Only read in events up to the specified time (in seconds).
        TimeOffset (double): An optional time offset to add to each event time in the output file.
    Returns:
        A pandas DataFrame with information about each tracker hit.
    '''

    theHits = []

    # Use MEGAlib reader to loop through the file.
    
    #first, we need to define our geometry.
    Geometry = ROOT.MDGeometryQuest()
    if Geometry.ScanSetupFile(ROOT.MString(GeometryName)) == True:
        print("Geometry " + GeometryName + " loaded!")
    else:
        print("Unable to load geometry " + GeometryName + " - Aborting!")
        quit()

    #now, we can try to read in the sim file.
    Reader = ROOT.MFileEventsSim(Geometry)
    if Reader.Open(ROOT.MString(FileName)) == False:
        print("Unable to open file " + FileName + ". Aborting!")
        quit()

    #loop through events in the file
    while True:
    
        Event = Reader.GetNextEvent()
        
        #break loop at end of file
        if not Event:
            break
            
        ROOT.SetOwnership(Event, True) #not sure what this does but it seems to be necessary
                
        #optional time cut
        if MaxTime is not None and Event.GetTime().GetAsDouble() > MaxTime:
            break
        
        hitList = MegaSimEventToDict(Event, Geometry, TimeOffset)
        theHits.extend( hitList )
    
    df = pandas.DataFrame(theHits)
    
    return df


def readOneSetOfSims( geometry, simFileName, MaxTime=None, TimeOffset=0):
    '''
    Extract information  from a MEGAlib sim file and save to disk as pandas DataFrame -> csv .
    Parameters:
        FileName: Input file path. Can be a .sim file or a .sim.gz file.
        GeometryName: Input geometry path
        MaxTime: Optional; if not None: Only read in events up to the specified time (in seconds).
        TimeOffset (double): An optional time offset to add to each event time in the output file.
    '''

    hitDfName = simFileName.replace(".sim", ".trackerHits.csv" ).replace(".gz", "")

    hitData = readSimFile(simFileName, geometry, MaxTime, TimeOffset)
    hitData.to_csv( hitDfName )
    
    
#example for how to use the functions above to write a .csv file to disk.
# readOneSetOfSims( "/Users/hfleisc1/amego_software/ComPair/sim_scripts/run_scripts/../../Geometry/AMEGO_Midex/TradeStudies/Tracker/BasePixelTracker/AmegoBase.geo.setup",  "/Users/hfleisc1/amego_software/ComPair/simfiles/test_pixel/sim/FarFieldPointSource_100.000MeV_Cos0.8_Phi0.0.inc1.id1.sim" )


#afterwards, the dataframe can be read back in from the .csv file using pandas.read_csv("filename" )
#or, just call readSimFile directly instead of readOneSetOfSims and deal with the resulting data frame immediately (combine with other data frames, plot etc).

