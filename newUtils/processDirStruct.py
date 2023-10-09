# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2023 Keith Sloan <keith@sloan-home.co.uk>              *
# *                      Munther Hind                                      *
# *                                                                        *
# *   This program is free software; you can redistribute it and/or modify *
# *   it under the terms of the GNU Lesser General Public License (LGPL)   *
# *   as published by the Free Software Foundation; either version 2 of    *
# *   the License, or (at your option) any later version.                  *
# *   for detail see the LICENCE text file.                                *
# *                                                                        *
# *   This program is distributed in the hope that it will be useful,      *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
# *   GNU Library General Public License for more details.                 *
# *                                                                        *
# *   You should have received a copy of the GNU Library General Public    *
# *   License along with this program; if not, write to the Free Software  *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
# *   USA                                                                  *
# *                                                                        *
# *   Acknowledgements :                                                   *
#                                                                          *
#     Takes as input a GDML file directory and creates/updates             *
#          STEP / BREP files from the GDML definitions                     *
#                                                                          *
#             python3 processDirStruct.py <directory>                      *
#                                                                          *
#***************************************************************************
import sys, os

class volAsm_class:
    #def __init__(self, vaName, path, level):
    def __init__(self, vaName, path):
        self.vaName = vaName
        self.path = path
        self.subVolAsmList = []
        self.level = 1


    def getName(self):
        print(self.vaName)


    def addSubVolAsms(self, volasmList):
        self.subVolAsmList = volasmList


    def getSubVolAsms(self):
        return self.subVolAsmList


    def printSubVolAsms(self):
        print(f"Volume {self.vaName}")
        for i in self.subVolAsmList:
            print(i.getName())    


    def processPath(self, path, levels, volAsmDict):
        print(f"Processing path {path}")
        vaName = os.path.splitext(os.path.basename(path))[0]
        print(f"Processing VolAsm {vaName}")
        #volAsm = volAsm_class(vaName, path, self.level+1)
        volAsm = volAsm_class(vaName, path)
        # Add volume to dictionary
        volAsmDict[vaName] = volAsm
        levels.addVolAsm(volAsm, path, self.level)
        subVolAsms = os.scandir(path)
        for p in subVolAsms:
            if p.is_dir():
                self.processPath(p.path, levels, volAsmDict)


    def exportStep(self):
        print(f"Export STEP {self.vaName} path {self.path}")


    def exportBrep(self):
        print(f"Export Brep {self.vaName} path {self.path}")


class levelDet:
    def __init__(self):
        self.volAsmList = []


    def addVolAsm(self, vaName, path):
        self.volAsmList.append(volAsm_class(vaName, path))    


class levels_class:
    def __init__(self):
        self.levels = []

    def addLevel(self):
        print(f"levels add level")
        self.levels.append(levelDet())
        print(f"len self.levels {len(self.levels)}")

    def checkLevel(self, lvlNum):
        #print(f"levels checkLevel lvlNum {lvlNum} type {type(lvlNum)}")
        #print(len(self.levels))
        lvlNum = int(lvlNum)
        if lvlNum > len(self.levels):
            self.addLevel()

        return self.levels[lvlNum-1]
        # Lists index from 0
    
    def addVolAsm(self, volAsm, path, lvlNum):
        print(f"levels add VolAsm")
        levelDet = self.checkLevel(lvlNum)
        levelDet.addVolAsm(volAsm, path)

    def print(self):
        print(f"Levels {self.levels}")    


class dirBase_class:
    def __init__(self, basePath):
        self.basePath = basePath
        self.volAsmDict = {}
        self.levels = levels_class()
        self.currentLevel = 1


        vaName = os.path.splitext(os.path.basename(basePath))[0]

        self.baseVolAsm = volAsm_class(vaName, basePath)
        self.baseVolAsm.processPath(basePath, self.levels, self.volAsmDict)

        print(f"Base Path {self.basePath}\n")
        #print(f"Path List \n")
        #for i in self.pathList:
        #    print(i.getName())
        self.baseVolAsm.printSubVolAsms()
        self.levels.print()

if len(sys.argv) < 2:
    print ("Usage: sys.argv[0] <gdml_directory>")
    sys.exit(1)

basePath = sys.argv[1]
baseVaName = os.path.splitext(os.path.basename(basePath))[0]
levels = levels_class()

print(f"\nProcessing GDML directory : {basePath}")

base = dirBase_class(basePath)
