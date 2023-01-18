import sys, os
from lxml import etree

class gdml_lxml() :
    def __init__(self, filename) :
        try:
            from lxml import etree
            print('Running with lxml.etree\n')
            print(filename)
            parser = etree.XMLParser(resolve_entities=True)
            self.root = etree.parse(filename, parser=parser)

        except ImportError :
            try :
                import xml.etree.ElementTree as etree
                print("Rnning with etree.ElementTree (import limitations)\n")
                self.tree = etree.parse(filename)
                self.root = self.tree.getroot()
            except :
                print('No lxml or xml')

        self.define    = self.root.find('define')
        self.materials = self.root.find('materials')
        self.solids    = self.root.find('solids')
        self.structure = self.root.find('structure')
        self.volAsmDict = {}  # Can have number of PhysVols that refer to same

    def printElement(self, elem):
        import lxml.html as html    
        print(html.tostring(elem))


    def printName(self, elem):
        name = elem.attrib.get('name')
        print(f"{elem} : {name}")

    def checkVolAsmDict(self, name):
        #print(f"Check Vol Asm Dict {self.volAsmDict}")
        if name in self.volAsmDict.keys():
            return False        # No need to process
        return True             # NEED to process

    def addVolAsmDict(self, name, elem):
        self.volAsmDict[name] = elem

    def getPosition(self, posName) :
        return self.define.find(f"position[@name='{posName}']")

    def getRotation(self, rotName) :
        return self.define.find(f"rotation[@name='{rotName}']")

    def getSolid(self, sname) :
        self.solids    = self.root.find('solids')
        print(f"getSolid : {self.solids} {len(self.solids)} {sname}")
        #self.printElement(self.solids)
        #return self.solids.find(f"*[@name='{sname}']")
        ret = self.solids.find(f"*[@name='{sname}']")
        print(f"getSolid : {self.solids} {len(self.solids)} {sname}")
        if ret is not None:
            self.printElement(ret)
        print(ret)
        return ret

    def getMaterials(self):
        return(self.materials)


    def processElement(self, elem):
        print(f"Process Element : {elem}")
        elemXml = self.materials.find(f"*[@name='{elem}']")
        if elemXml is not None:
            print(f"Element : {elemXml.get('name')}")


    def processMaterial(self, newMat, mat):
        print(f"Process Material : {mat}")
        matXml = self.materials.find(f"*[@name='{mat}']")
        print(f"matXml {matXml}")
        if matXml is not None:
            #newMat.insert(0, matXml)
            for fractXml in matXml.findall("fraction"):
                ref = fractXml.get("ref")
                print(f"Faction ref {ref}")
                self.processElement(ref)
            for compXml in matXml.findall("composite"):
                ref = compXml.get("ref")
                print(f"Composite ref {ref}")
                self.processElement(ref)
            return matXml    


    def processMaterials(self, volAsm, matList):
        print(f"Process Materials {matList}")
        #newMat = etree.Element("materials")
        for mat in matList:
            matXml = self.processMaterial(volAsm, mat)
            # Munther please REVIEW
            if matXml is not None:
                print(f"insert into Materials XML {volAsm.newMaterials}")
            #    newMat.insert(0, matXml)
            #    volAsm.newMaterials.insert(0, matXml)

    def getVolAsm(self, vaname) :
        return self.structure.find(f"*[@name='{vaname}']")

    #def addEntity(self, elemName, xmlFile) :
    #    self.docString += "<!ENTITY " + elemName + ' SYSTEM "' + xmlFile+'">\n'
    #    self.gdml.append(etree.Entity(elemName))

    #def closeElements(self) :
    #    self.docString += ']\n'

    def writeGDML(self, path,vname) :
        #indent(iself.gdml)
        etree.ElementTree(self.gdml).write(os.path.join(path,vname+'.gdml'), \
               doctype=self.docString.encode('UTF-8'))

class VolAsm() :

    def __init__(self, vaname) :
        from lxml import etree

        self.vaname    = vaname
        NS = 'http://www.w3.org/2001/XMLSchema-instance'
        location_attribute = '{%s}noNameSpaceSchemaLocation' % NS
        self.gdml = etree.Element('gdml',attrib={location_attribute: \
        'http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd'})
        self.docString = "\n<!DOCTYPE gdml [\n"
        #self.newDefine = etree.SubElement(self.gdml,'define')
        self.newDefine = etree.Element('define')
        #self.newSolids = etree.SubElement(self.gdml,'solids')
        self.newSolids = etree.Element('solids')
        self.newMaterials = etree.Element('materials')
        self.matList = []       # List of found materials
        self.solidDict = {}
        self.posDict  = {}
        self.rotDict  = {}


    def addDefine(self, d) :
        if d is not None  :
            self.newDefine.append(d)
        else :
            print('==== Problem with define')
            exit(1)
  
    def processPosition(self, lxml, posName) :
       #print(lxml.getPosition(posName))
       if posName not in self.posDict :
          pxml = lxml.getPosition(posName)
          if pxml is not None:
            self.posDict[posName] = pxml
            #self.newDefine.append(p)
          else:
             print(f"Position {posName} Not Found")

    def processRotation(self,lxml, rotName) :
       #print(lxml.getPosition(rotName))
       if rotName not in self.rotDict :
           rxml = lxml.getPosition(rotName)
           if rxml is not None:
               self.rotDict[rotname] = rxml
               #  self.rotList.append(rotName)
               #  self.newDefine.append(p)
           else:
               print(f"Rotation {rotName} Not Found")

   
    def processSolid(self, lxml, sname) :
       print(f"{self.vaname} Solid List {self.solidDict}")
       if sname not in self.solidDict :
           sxml = lxml.getSolid(sname)
           if sxml is not None:
               self.solidDict[sname] = sxml
               print(f"solidDict {self.solidDict}")
           else :
               print(f"Solid : {sname} Not Found")
               exit(1)

    def processPhysVols(self, lxml, volasm, path) :
       vaname = volasm.attrib.get('name')
       print('Process Phys Vols of : '+vaname)
       for pv in volasm.findall('physvol') :
           volref = pv.find('volumeref')
           pname = volref.attrib.get('ref')
           print('physvol : '+pname)
           # Is this a new VolAsm
           if lxml.checkVolAsmDict(pname) == True:
                npath = os.path.join(path, pname)
                print('New path : '+npath)
                checkDirectory(npath)
                new_pa = VolAsm(pname)
                new_pa.processVolAsm(lxml, npath, pname)
           posref = pv.find('positionref')
           if posref is not None :
              posname = posref.attrib.get('ref')
              print('Stack Position ref : '+posname)
              self.processPosition(lxml, posname)
           rotref = pv.find('rotationref')
           if rotref is not None :
              rotname = rotref.attrib.get('ref')
              print('Stack Rotation ref : '+rotname)
              self.processRotation(lxml, rotname)
           print('Number of positions in : '+vaname+' : '+str(len(self.posDict)))
           #print(self.posDict)
           for posName in self.posDict :
               print('Pull Position '+posName)
               self.addDefine(self.posDict[posName])
           for rotName in self.rotDict :
               self.addDefine(self.rotDict[rotName])
           writeElement(path, vaname, 'defines', self.newDefine)
           self.addEntity('define',vaname+'_defines.xml')
  
    def processVolume(self, lxml, path, vol) :
        print('Process Volume')
        lxml.printName(vol)
        # Need to process physvols first
        vname = vol.attrib.get('name')
        print('volume : ' + vname)
        self.processPhysVols(lxml, vol, path)
        solid = vol.find('solidref')
        sname = solid.attrib.get('ref')
        print('Process Solid : '+sname)
        self.processSolid(lxml, sname)
        materialRef = vol.find('materialref')
        if materialRef is not None :
            material = materialRef.attrib.get('ref')
            if material not in self.matList:
                self.matList.append(material)
        #writeElement(path, vaname, 'solids', self.newSolids)
        #writeElement(path, vname, 'materials', materials)

    def processAssembly(self, lxml, path, assem) :
       aname = assem.attrib.get('name')
       print('Process Assembly ; '+aname)
       self.processPhysVols(lxml, assem, path)

    def processVolAsm(self, lxml, path, vaname):
        if lxml.checkVolAsmDict(vaname):
            volasm = lxml.getVolAsm(vaname)
            lxml.addVolAsmDict(vaname, volasm)
            print('Processing VolAsm : '+vaname)
            lxml.printName(volasm)
            if volasm is not None:
                writeElement(path, vaname, 'struct', volasm)
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

    def flushDicts(self, lxml, path, vaname):
       print(f"Flush Dicts {vaname}") 
       for sName in self.solidDict:
            self.newSolids.append(self.solidDict.get(sName))
       writeElement(path, vaname, 'solids', self.newSolids)
       self.addEntity('solids',vaname+'_solids.xml')
 
       materialsXML = lxml.processMaterials(self, self.matList)
       #writeElement(path, vaname, 'materials', materialsXML)
       #self.addEntity('materials',vaname+'_materials.xml')
       self.closeEntities()
       self.writeGDML(path, vaname)

    def addEntity(self, elemName, xmlFile) :
        self.docString += "<!ENTITY "+elemName+' SYSTEM "'+xmlFile+'">\n'
        self.gdml.append(etree.Entity(elemName))

    def closeEntities(self) :
        self.docString += ']\n'

    def writeGDML(self, path, vname) :
        #indent(iself.gdml)
        etree.ElementTree(self.gdml).write(os.path.join(path,vname+'.gdml'), \
               doctype=self.docString.encode('UTF-8'))


def checkDirectory(path):
    if not os.path.exists(path):
       print('Creating Directory : '+path)
       os.mkdir(path)

def writeElement(path, sname, type, elem, ext="xml") :
    import os

    fpath = os.path.join(path,sname+'_'+type)
    print('writing file : '+fpath)
    etree.ElementTree(elem).write(fpath+'.'+ext)

def exportEntity(dirPath, elemName, elem) :
    import os
    global gdml, docString

    etree.ElementTree(elem).write(os.path.join(dirPath,elemName))
    docString += '<!ENTITY '+elemName+' SYSTEM "'+elemName+'">\n'
    gdml.append(etree.Entity(elemName))

if len(sys.argv)<5:
  print ("Usage: sys.argv[0] <parms> <Volume> <in_file> <Out_directory> <materials>")
  print("/n For parms the following are or'ed together")
  print(" For future")
  sys.exit(1)

parms  = int(sys.argv[1])
vName = sys.argv[2]
iName = sys.argv[3]
oName = sys.argv[4]

print('\nExtracting Volume : '+vName+' from : '+iName+' to '+oName)
checkDirectory(oName)
path = os.path.join(oName,vName)
checkDirectory(path)
lxml = gdml_lxml(iName)
volasm = VolAsm(vName)
volasm.processVolAsm(lxml, path, vName)
#setup = etree.Element('setup', {'name':'Default', 'version':'1.0'})
#etree.SubElement(setup,'world', { 'ref' : volList[-1]})
