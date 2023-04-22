# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2022 Keith Sloan <keith@sloan-home.co.uk>              *
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
#    Takes as input a Volume Name, GDML file  and outputs                  *
#              a directory structure starting at the specified Volume Name *
#                                                                          *
#                                                                          *
#    python3 buildDirStruct.py <parms> <Volume> <gdml_file> <Out_dir>      *
#                                                                          *
#       parms for future use ( use 1 for now )                             *
#       Volume    : Name of Volume to be extracted                         *
#       gdml_file : Source GDML file                                       *
#       Out_dir   : Output Directory                                       *
#                                                                          *
#  Where each Volume, Assembly is created as a sub directory               *
#                                                                          *
#           volumeName.gdml                                                *
#           volumeName_define.xml                                          *
#           volumeName_materials.xml                                       *
#           volumeName_solids.xml                                          *
#           volumeName_struct.xml                                          *
#           volumeName_setup.xml                                           *
#           < sub Volumes/Assemblies >                                     *
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

        self.define    = self.root.find('define')
        self.materials = self.root.find('materials')
        self.solids    = self.root.find('solids')
        self.structure = self.root.find('structure')
        #self.volAsmDict = {}  # Can have number of PhysVols that refer to same
        # Needs to be in VolAsm   
        self.VolAsmStructDict = {}

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


    def addVolAsmStructDict(self, name, elem):
        self.VolAsmStructDict[name] = elem


    def getRawVolAsmStruct(self, vaname):
        newStruct = copy.deepcopy(self.structure)
        struct = newStruct.find(f"*[@name='{vaname}']")
        return struct


    def getVolAsmStruct(self, vaname):
        # Needs to be structure and sub volumes 
        # So cannot just use structure in source#
        print(f"VolAsmStructDict {self.VolAsmStructDict.keys()}")
        ret = self.VolAsmStructDict[vaname]
        if ret is not None:
            return ret
        else:
            print(f"{vaname} not found in Dict")    


    def getPosition(self, posName):
        return self.define.find(f"position[@name='{posName}']")


    def getRotation(self, rotName):
        return self.define.find(f"rotation[@name='{rotName}']")


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


    # Should no longer be used.
    def processElement(self, matxml, elem):
        print(f"Process Element : {elem}")
        elemXml = self.materials.find(f"*[@name='{elem}']")
        if elemXml is not None:
            # <- make a deep copy of the found elemen
            newelemXml = copy.deepcopy(elemXml)
            print(f"Element : {elemXml.get('name')}")
            #matxml.append(newelemXml)
            self.materials.append(newelemXml)
            #self.printMaterials()


    def processMaterial(self, volAsm, mat):
        #print(f"Process Material  {mat} {volAsm}")
        print(f"Process Material  {mat}")
        matXml = self.materials.find(f"*[@name='{mat}']")
        print(f"matXml {matXml}")
        if matXml is not None:
            # <- make a deep copy of the found elemen
            newmatXml = copy.deepcopy(matXml)
            #self.printMaterial(newmatXml)
            volAsm.newMaterials.append(newmatXml)


    def processMaterials(self, volAsm, matList):
        print(f"Process Materials {matList} {volAsm}")
        #print(f"Process Materials {matList}")
        for mat in matList:
            newMat = self.processMaterial(volAsm, mat)
            #        if newMat is not None:
            #            while volAsm is not None:
            #print(f"insert into Materials XML {volAsm.newMaterials}")
            #volAsm.newMaterials.append(newMat)
            #                volAsm = volAsm.getParent()


    def processMaterialElements(self, volAsm, mat):
        # Need to process Fraction and composite first
        #print(f"Process Material Elements : {volAsm} {mat}")
        print(f"Process Material Elements for : {mat}")
        matXml = self.materials.find(f"*[@name='{mat}']")
        print(f"matXml {matXml}")
        if matXml is not None:
            # Need to process Fraction and composite first
            for fractXml in matXml.findall("fraction"):
                ref = fractXml.get("ref")
                print(f"Faction ref {ref}")
                volAsm.checkAddMaterial(ref)

            for compXml in matXml.findall("composite"):
                ref = compXml.get("ref")
                print(f"Composite ref {ref}")
                volAsm.checkAddMaterial(ref)


    def processMaterialsElements(self, volAsm, matList):
        # Need to process Fraction and composite first
        print(f"Process Materials Elements {matList} {volAsm}")
        while volAsm is not None:
            for mat in matList:
                self.processMaterialElements(volAsm, mat)
            volAsm = volAsm.getParent()


    def checkBooleanSolids(self, volAsm, solidXml):
        #print(f"{solidXml}")
        #print(solidXml.attrib)
        #print(solidXml.keys)
        #print(dir(solidXml))
        tag = solidXml.tag
        if tag == 'union' or tag == 'subtraction' or tag == 'intersection':
            for child in solidXml:
                if child.tag == "first" or child.tag == "second":
                    solidRef = child.attrib.get("ref")
                    print(f"Solid Ref {solidRef}")
                    self.processSolid(volAsm, solidRef)

        elif tag == 'multiUnion':
            for child in solidXml:
                if child.tag == 'multiUnionNode':
                    for el in child:
                        if el.tag == 'solid':
                            solidRef = el.attrib.get("ref")            
                            print(f"Solid Ref {solidRef}")
                            self.processSolid(volAsm, solidRef)

    def processSolid(self, volAsm, sname):
        solidXml = self.solids.find(f"*[@name='{sname}']")
        #print(f"solidXml {solidXml}")
        newSolidXml = copy.deepcopy(solidXml)
        if newSolidXml is not None:
            volAsm.newSolids.append(newSolidXml)
            self.checkBooleanSolids(volAsm, newSolidXml)


    def processSolids(self, volAsm, solidList):
        #print(f"Process Solids {solidList} {volAsm}")
        print(f"Process Solids {solidList}")
        for sname in solidList:
            self.processSolid(volAsm, sname)


    def processPosDefine(self, volAsm, pos):
        posXml = self.define.find(f"*[@name='{pos}']")
        #print(f"posXml {posXml}")
        newPosXml = copy.deepcopy(posXml)
        if newPosXml is not None:
            volAsm.newDefine.append(newPosXml)


    def processPosDefines(self, volAsm, definePosList):
        #print(f"Process Solids {definePosList} {volAsm}")
        #print(f"Process Pos defines {definePosList}")
        if len(definePosList) > 0:
            for pos in definePosList:
                self.processPosDefine(volAsm, pos)


    def processRotDefine(self, volAsm, rot):
        rotXml = self.define.find(f"*[@name='{rot}']")
        #print(f"rotXml {rotXml}")
        newRotXml = copy.deepcopy(rotXml)
        if newRotXml is not None:
            volAsm.newDefine.append(newRotXml)


    def processRotDefines(self, volAsm, defineRotList):
        #print(f"Process Solids {definePosList} {volAsm}")
        #print(f"Process Rot defines {defineRotList}")
        if len(defineRotList) > 0:
            for rot in defineRotList:
                self.processRotDefine(volAsm, rot)


    # def addEntity(self, elemName, xmlFile) :
    #    self.docString += "<!ENTITY " + elemName + ' SYSTEM "' + xmlFile+'">\n'
    #    self.gdml.append(etree.Entity(elemName))

    # def closeElements(self) :
    #    self.docString += ']\n'

    def writeGDML(self, path, vname):
        # indent(iself.gdml)
        etree.ElementTree(self.gdml).write(os.path.join(path, vname+'.gdml'), \
               doctype = self.docString.encode('UTF-8'))



class VolAsm():

    def __init__(self, vaname, parent):
        from lxml import etree
        self.vaname = vaname
        self.parent = parent
        NS = 'http://www.w3.org/2001/XMLSchema-instance'
        location_attribute = '{%s}noNameSpaceSchemaLocation' % NS
        self.gdml = etree.Element('gdml', attrib={location_attribute: \
        'http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd'})
        self.docString = "\n<!DOCTYPE gdml [\n"
        # self.newDefine = etree.SubElement(self.gdml,'define')
        self.newDefine = etree.Element('define')
        # self.newSolids = etree.SubElement(self.gdml,'solids')
        self.newMaterials = etree.Element('materials')
        self.newSolids = etree.Element('solids')
        self.newStruct = etree.Element('structure')
        self.newSetup = etree.Element('setup')
        self.matList = []       # List of found materials
        self.solidList = []
        self.definePosList = []
        self.defineRotList = []
        self.volAsmDict = {}
        self.posDict = {}
        self.rotDict = {}

    def getParent(self):
        return self.parent    

    def addDefine(self, d):
        if d is not None:
            self.newDefine.append(d)
        else:
            print('==== Problem with define')
            exit(1)

    def checkVolAsmDict(self, name):
        print(f"Check Vol Asm Dict {self.volAsmDict}")
        if name in self.volAsmDict.keys():
            print(f"volasm {name} already processed")
            return True
        else:
            print(f"volasm {name} Not Yet processed")
            return False
        #print("Always return True for now")
        #return True


    def addVolAsmDict(self, name, elem):
        print(f"add VolAsmDict {name} {elem}")
        self.volAsmDict[name] = elem


    def checkAddMaterial(self, mat):
        if mat not in self.matList:
            self.matList.append(mat)


    def processPosition(self, lxml, posName):
        # print(lxml.getPosition(posName))
        if posName not in self.posDict:
            pxml = lxml.getPosition(posName)
            if pxml is not None:
                self.posDict[posName] = pxml
                # self.newDefine.append(p)
            else:
                print(f"Position {posName} Not Found")

    def processRotation(self, lxml, rotName):
        # print(lxml.getPosition(rotName))
        if rotName not in self.rotDict:
            rxml = lxml.getPosition(rotName)
            if rxml is not None:
                self.rotDict[rotName] = rxml
                #  self.rotList.append(rotName)
                #  self.newDefine.append(p)
            else:
                print(f"Rotation {rotName} Not Found")


    def processSolid(self, lxml, sname):
        print(f"{self.vaname} Solid List {self.solidList}")
        if sname not in self.solidList:
            self.solidList.append(sname)


    def getStructContents(self):
        print(f"Children {self.newStruct.getchildren()}")
        return self.newStruct.getchildren()


    def combineStruct(self, source):
        if source.tag == 'structure':
            for child in source.getchildren():
                self.newStruct.append(child)
        else:        
            self.newStruct.append(source)


    def processPhysVols(self, lxml, volasm, path):
        vaname = volasm.attrib.get('name')
        volList = []
        print(f"Process Phys Vols of : {vaname}")
        for pv in volasm.findall('physvol'):
            volref = pv.find('volumeref')
            pname = volref.attrib.get('ref')
            print(f"physvol : {pname} volume {vaname}")
            # Is this a new VolAsm
            if self.checkVolAsmDict(pname) is False:
                print(f"need to process {pname}")
                npath = os.path.join(path, pname)
                print('New path : '+npath)
                checkDirectory(npath)
                new_pa = VolAsm(pname, self)
                new_pa.processVolAsm(lxml, npath, pname)
                volList.append(pname)
                # Need to get structure after processing subVolumes
                volasm = lxml.getVolAsmStruct(pname)
                self.addVolAsmDict(pname, volasm)
            # Process positions rotations
            posref = pv.find('positionref')
            if posref is not None:
                posname = posref.attrib.get('ref')
                print('Stack Position ref : '+posname)
                if posname not in self.definePosList:
                    self.definePosList.append(posname)
                self.updateParentPosDefines(posname)
                #self.processPosition(lxml, posname)
            rotref = pv.find('rotationref')
            if rotref is not None:
                rotname = rotref.attrib.get('ref')
                print('Stack Rotation ref : '+rotname)
                if rotname not in self.defineRotList:
                    self.defineRotList.append(rotname)
                self.updateParentRotDefines(rotname)
                #self.processRotation(lxml, rotname)
            print(f"Number of positions in : {vaname} : \
                     {len(self.definePosList)}")
            print(f"Number of rotations in : {vaname} : \
                     {len(self.definePosList)}")
            # print(self.posDict)
            #for posName in self.definePosList:
            #    print('Pull Position '+posName)
            #    self.addDefine(lxml.getPosition(posName))
            #for rotName in self.rotDict:
            #    self.addDefine(lxml.getRotation(rotNamer))
            #writeElement(path, vaname, 'defines', self.newDefine)
            #self.addEntity('define', vaname+'_defines.xml')

            # Make sure all sub volumes are added to this volumes struct
        print(f"=== Process sub volume structures {vaname} list {volList}")
        #print(lxml.VolAsmStructDict.keys())
        #for vname in reversed(volList):
        for vname in volList:
            print(f"add sub volume struct {vname}")
            target = lxml.getVolAsmStruct(vname)
            if target is not None:
                self.combineStruct(target)
            else:
                print(f"{vname} struct not found in Dict")    
        print(f"add volume struct {vaname}")
        self.combineStruct(lxml.getRawVolAsmStruct(vaname))
        print(f"add {vaname} volume struct to lxml Dict")
        lxml.addVolAsmStructDict(vaname, self.newStruct)


    def updateParentLists(self, material, sname):
        parent = self.getParent()
        while parent is not None:
            if material is not None:
                if material not in parent.matList:
                    parent.matList.append(material)
            if sname is not None:        
                if sname not in parent.solidList:
                    parent.solidList.append(sname)
            parent = parent.getParent()    


    def updateParentPosDefines(self, pos):
        parent = self.getParent()
        while parent is not None:
            if pos not in parent.definePosList:
               parent.definePosList.append(pos)
            parent = parent.getParent()    


    def updateParentRotDefines(self, rot):
        parent = self.getParent()
        while parent is not None:
            if rot not in parent.defineRotList:
               parent.defineRotList.append(rot)
            parent = parent.getParent()    


    def processVolume(self, lxml, path, vol):
        # Need to process physvols first
        vname = vol.attrib.get('name')
        print(f"Process Volume {vname}")

        self.processPhysVols(lxml, vol, path)
        #self.newStruct.append(lxml.getVolAsmStruct(vname))
        # added by processPhysVols
        solidRef = vol.find('solidref')
        sname = None
        if solidRef is not None:
            sname = solidRef.attrib.get('ref')
            if sname not in self.solidList:
                self.solidList.append(sname)
        materialRef = vol.find('materialref')
        material = None
        if materialRef is not None :
            material = materialRef.attrib.get('ref')
            if material not in self.matList:
                self.matList.append(material)
        self.updateParentLists(material, sname)
                

        # writeElement(path, vaname, 'solids', self.newSolids)
        # writeElement(path, vname, 'materials', materials)

    def processAssembly(self, lxml, path, assem):
        aname = assem.attrib.get('name')
        print('Process Assembly ; '+aname)
        self.processPhysVols(lxml, assem, path)
        #self.newStruct.append(lxml.getVolAsmStruct(aname))
        # added by processPhysVols


    def processVolAsm(self, lxml, path, vaname):
        if self.checkVolAsmDict(vaname) == False:
            volasm = lxml.getRawVolAsmStruct(vaname)
            self.addVolAsmDict(vaname, volasm)
            print(f"Processing VolAsm : {vaname} {volasm}")
            if volasm is not None:
                #writeElement(path, vaname, 'struct', volasm)
                #self.newStruct.append(volasm)
                if volasm.tag == 'volume':
                    self.processVolume(lxml, path, volasm)
                elif volasm.tag == 'assembly':
                    self.processAssembly(lxml, path, volasm)
                else:
                    print('Not Volume or Assembly : '+volasm.tag)
                self.flushDicts(lxml, path, vaname)
            return True
        else:
            print(f"Already processed {vaname}")
            return False

    def processSetup(self, lxml, vaname):
        #worldVol = next(iter(lxml.volAsmDict))
        #print(f"Vol Asm {worldVol}")
        setup = self.newSetup = etree.Element("setup", {"name" : "Default", "version" : "1.0"})
        etree.SubElement(setup, "world", {"ref" : vaname})
        #self.newSetup.append(setup)


    def flushDicts(self, lxml, path, vaname):
        print(f"Flush Dicts {vaname}")
        lxml.processPosDefines(self, self.definePosList)
        lxml.processRotDefines(self, self.defineRotList)
        if len(self.definePosList) > 0 or len(self.defineRotList) > 0:
            writeElement(path, vaname, 'define', self.newDefine)
            self.addEntity('define', vaname+'_define.xml')
        # Need to process Elements first to add to matList 
        print(f"Process Elements {self.matList}")
        lxml.processMaterialsElements(self, self.matList)
        print(f"Process final List {self.matList}")
        lxml.processMaterials(self, self.matList)
        #materialsXML = lxml.processMaterials(self, self.matList)
        writeElement(path, vaname, 'materials', self.newMaterials)
        self.addEntity('materials',vaname+'_materials.xml')
        lxml.processSolids(self, self.solidList)
        writeElement(path, vaname, 'solids', self.newSolids)
        self.addEntity('solids', vaname+'_solids.xml')
        writeElement(path, vaname, 'struct', self.newStruct)
        self.addEntity('struct',vaname+'_struct.xml')
        #print(f"Add struct dict")
        #lxml.addVolAsmStructDict(vaname, self.newStruct)
        self.processSetup(lxml, vaname)
        writeElement(path, vaname, 'setup', self.newSetup)
        self.addEntity('setup', vaname+'_setup.xml')
        self.closeEntities()
        self.writeGDML(path, vaname)

    def addEntity(self, elemName, xmlFile):
        self.docString += "<!ENTITY "+elemName+' SYSTEM "'+xmlFile+'">\n'
        self.gdml.append(etree.Entity(elemName))

    def closeEntities(self):
        self.docString += ']>\n'

    def writeGDML(self, path, vname):
        # indent(iself.gdml)
        etree.ElementTree(self.gdml).write(os.path.join(path, vname+'.gdml'), \
                                           doctype=self.docString.encode('UTF-8'))


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


if len(sys.argv) < 5:
    print ("Usage: sys.argv[0] <parms> <Volume> <in_file> <Out_directory> <materials>")
    print("/n For parms the following are or'ed together")
    print(" For future")
    sys.exit(1)

parms = int(sys.argv[1])
vName = sys.argv[2]
iName = sys.argv[3]
oName = sys.argv[4]

print('\nExtracting Volume : '+vName+' from : '+iName+' to '+oName)
checkDirectory(oName)
path = os.path.join(oName,vName)
checkDirectory(path)
lxml = gdml_lxml(iName)
volasm = VolAsm(vName, None)
volasm.processVolAsm(lxml, path, vName)
# setup = etree.Element('setup', {'name':'Default', 'version':'1.0'})
# etree.SubElement(setup,'world', { 'ref' : volList[-1]})
