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

        NS = 'http://www.w3.org/2001/XMLSchema-instance'
        location_attribute = '{%s}noNameSpaceSchemaLocation' % NS
        self.gdml = etree.Element('gdml', attrib={location_attribute: \
        'http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd'})
        self.docString = "\n<!DOCTYPE gdml [\n"


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


    def writeElement(self, path, fName, elem, ext="xml"):
        import os

        fpath = os.path.join(path, fName)
        print('writing file : ' + fpath)
        etree.ElementTree(elem).write(fpath+'.'+ext)


    def addEntity(self, elemName, elem, xmlFile) :
        self.docString += "<!ENTITY " + elemName + ' SYSTEM "' + xmlFile+'">\n'
        self.gdml.append(etree.Entity(elemName))


    def closeEntities(self) :
        self.docString += ']>\n'


    def processElements(self, name):

        for n, elem in enumerate(self.root.findall(name)):
            fName = name+"_"+str(n)
            print(f"{name}file {n} {fName} elem : {elem}")
            self.writeElement(oName, fName, elem)
            self.addEntity(fName, elem, fName+'.xml')


    def processElement(self, name):

        elem = self.root.find(name)
        fName = name
        print(f"{name}file {fName} elem : {elem}")
        self.writeElement(oName, fName, elem)
        self.addEntity(fName, elem, fName+'.xml')


    def writeGDML(self, path, fname):
        # indent(iself.gdml)
        #etree.ElementTree(self.gdml).write(os.path.join(path, fname+'.gdml'), \
        etree.ElementTree(self.gdml).write(os.path.join(path, fname), \
               doctype = self.docString.encode('UTF-8'))




def checkDirectory(path):
    if not os.path.exists(path):
        print('Creating Directory : '+path)
        os.mkdir(path)



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
lxml.processElements('materials')
lxml.processElements('define')
lxml.processElements('solids')
lxml.processElements('structure')
lxml.processElement('setup')
lxml.closeEntities()
lxml.writeGDML(oName, iName)
