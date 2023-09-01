# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2023 Keith Sloan <keith@sloan-home.co.uk>              *
# *                      Munther Hind                                      *
# *                                                                        **
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
#    Takes as input a GDML file and places multple sections                *
#    as in (defines, solids, materials, structure etc )                    *
#    in a directory structure and creates a main include file              *
#                                                                          *
#                                                                          *
#    python3 split <gdml_file> <Out_dir>                                   *
#                                                                          *
#       gdml_file : Source GDML file                                       *
#       Out_dir   : Output Directory                                       *
#                                                                          *
#                                                                          *
############################################################################

import sys, os
from lxml import etree
import copy

class gdml_lxml() :
    def __init__(self, filename):
        try:
            from lxml import etree
            print('Running with lxml.etree\n')
            print(filename)
            parser = etree.XMLParser(resolve_entities=True)
            self.root = etree.parse(filename, parser=parser)

        except ImportError:
            try:
                import xml.etree.ElementTree as etree
                print("Rnning with etree.ElementTree (import limitations)\n")
                self.tree = etree.parse(filename)
                self.root = self.tree.getroot()
            except:
                print('No lxml or xml')

        #self.define    = self.root.find('define')
        #self.materials = self.root.find('materials')
        #self.solids    = self.root.find('solids')
        #self.structure = self.root.find('structure')
        #self.volAsmDict = {}  # Can have number of PhysVols that refer to same
        # Needs to be in VolAsm   
        #self.VolAsmStructDict = {}

    def findAll(self, elem):
        return self.root.findall(elem)

    def printElement(self, elem):
        import lxml.html as html
        print(html.tostring(elem))


    def printMaterials(self):
        import lxml.html as html
        print(html.tostring(self.materials))


    def printMaterial(self, mat):
        import lxml.html as html
        print(html.tostring(mat))


    def printName(self, elem):
        name = elem.attrib.get('name')
        print(f"{elem} : {name}")


    #def checkVolAsmDict(self, name):
    #    # print(f"Check Vol Asm Dict {self.volAsmDict}")
    #    if name in self.volAsmDict.keys():
    #        return False        # No need to process
    #    return True             # NEED to process


    #def addVolAsmDict(self, name, elem):
    #    self.volAsmDict[name] = elem


    #def addVolAsmStructDict(self, name, elem):
    #    self.VolAsmStructDict[name] = elem


    #def getRawVolAsmStruct(self, vaname):
    #    newStruct = copy.deepcopy(self.structure)
    #    struct = newStruct.find(f"*[@name='{vaname}']")
    #    return struct


    #def getVolAsmStruct(self, vaname):
    #    # Needs to be structure and sub volumes 
    #    # So cannot just use structure in source#
    #    print(f"VolAsmStructDict {self.VolAsmStructDict.keys()}")
    #    ret = self.VolAsmStructDict[vaname]
    #    if ret is not None:
    #        return ret
    #    else:
    #        print(f"{vaname} not found in Dict")    



    def getSolid(self, sname):
        self.solids = self.root.find('solids')
        print(f"getSolid : {self.solids} {len(self.solids)} {sname}")
        # self.printElement(self.solids)
        # return self.solids.find(f"*[@name='{sname}']")
        ret = self.solids.find(f"*[@name='{sname}']")
        print(f"getSolid : {self.solids} {len(self.solids)} {sname}")
        if ret is not None:
            self.printElement(ret)
        print(ret)
        return ret


    def getMaterials(self):
        return(self.materials)



    def processSolid(self, volAsm, sname):
        solidXml = self.solids.find(f"*[@name='{sname}']")
        #print(f"solidXml {solidXml}")
        newSolidXml = copy.deepcopy(solidXml)
        if newSolidXml is not None:
            volAsm.newSolids.append(newSolidXml)
            self.checkBooleanSolids(volAsm, newSolidXml)



    def addEntity(self, elemName, xmlFile) :
        self.docString += "<!ENTITY " + elemName + ' SYSTEM "' + xmlFile+'">\n'
        self.gdml.append(etree.Entity(elemName))

    def closeElements(self) :
        self.docString += ']\n'

    def writeGDML(self, path, vname):
        # indent(iself.gdml)
        etree.ElementTree(self.gdml).write(os.path.join(path, vname+'.gdml'), \
               doctype = self.docString.encode('UTF-8'))




def checkDirectory(path):
    if not os.path.exists(path):
        print('Creating Directory : '+path)
        os.mkdir(path)


def writeElement(path, sname, type, elem, ext="xml"):
    import os

    fpath = os.path.join(path, sname+'_'+type)
    print('writing file : ' + fpath)
    etree.ElementTree(elem).write(fpath+'.'+ext)


def exportEntity(dirPath, elemName, elem):
    import os
    global gdml, docString

    etree.ElementTree(elem).write(os.path.join(dirPath, elemName))
    docString += '<!ENTITY '+elemName+' SYSTEM "'+elemName+'">\n'
    gdml.append(etree.Entity(elemName))


if len(sys.argv) < 3:
    print ("Usage: sys.argv[0] <in_file> <Out_directory>")
    sys.exit(1)

iName = sys.argv[1]
oName = sys.argv[2]

checkDirectory(oName)
#path = os.path.join(oName,vName)
#checkDirectory(path)
lxml = gdml_lxml(iName)
# setup = etree.Element('setup', {'name':'Default', 'version':'1.0'})
# etree.SubElement(setup,'world', { 'ref' : volList[-1]})
for n, elem in enumerate(lxml.findAll('materials')):
    fName = "materials_"+str(n)
    print(f"Materials file {n} {fName} elem : {elem}")
for n, elem in enumerate(lxml.findAll('define')):
    fName = "define_"+str(n)
    print(f"Define file {n} {fName} elem : {elem}")

