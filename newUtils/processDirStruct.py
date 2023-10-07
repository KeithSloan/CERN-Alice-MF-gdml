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

class volAsmDet:
    def __init__(self, vaName, path, level):
        self.vaName = vaName
        self.path = path
        self.level = level


class processVolAsm:
    def __init__(self, vaName, path):
        self.level = levelDet(vaName, path)
        self.path = path


    def processPath(self, path):
        print(f"Processing path {path}")
        for p in os.scandir(path):
            if p.is_dir():
                self.processPath(p.path)

    def exportStep(self):
        print(f"Export STEP {self.vaName} path {self.path}")


    def exportBrep(self):
        print(f"Export Brep {self.vaName} path {self.path}")


class levelDet:
    def __init__(self, vaName, path):
        self.level = 1
        self.volList = [[vaName, path, 1]]


    def getLevel(self):
        return self.level    


    def addVolAsm(self, volAsm, path):
        self.level += 1
        self.volList.append([volAsm, path, self.level])


class dirBase_class:
    def __init__(self, basePath):
        self.basePath = basePath
        self.pathList = []
        self.levelList = []
        self.currentLevel = 1

        vaName = os.path.splitext(os.path.basename(basePath))[0]

        baseVolAsm = processVolAsm(vaName, basePath)


    def addVolAsm(self, vaName, path):
        print(f"Adding volasm {vname} path {path}")
        volAsm = volAsmDet(vaName, path, self.currentLevel)
        self.pathList.append(volAsm)
        if self.currentLevel == 1:
            self.levelList.append(volAsm)
        else:
            self.currentLevel += 1
            self.levelList[self.currentLevel].addVolAsm(volAsm)

if len(sys.argv) < 2:
    print ("Usage: sys.argv[0] <gdml_directory>")
    sys.exit(1)

basePath = sys.argv[1]
baseVaName = os.path.splitext(os.path.basename(basePath))[0]
levDetail = levelDet(baseVaName, basePath)

print(f"\nProcessing GDML directory : {basePath}")

base = dirBase_class(basePath)
