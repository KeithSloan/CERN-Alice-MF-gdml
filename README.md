### Important Notice

This repro has a lot of files and therefore uses git-lfs
You therefore need to install git-lfs before cloning the repro

See https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage

### Create an initial directory structure

The buildDirStruct.py process a gdml file building a directory structure where each volume creates a directory
with a set of files.

      volname.gdml (With appropriate includes for the following)
      volname.setup.xml
      volname.solids.xml
      volname.materials.xml
      volname.structure.xml
      volname.define.xml

```
Run newUtils/buildDirStruct.py <option> <primary volume> <complete gdml file> <target directory>

<option>  : for future use
<primary> : the script will look for the primary volumes and start building the structure from there.
<complete gdml file> : source gdml file to be used to build the scructure from
<target directory> : target direcory
```

Example: (Note creating the stcucture for Alice takes around 12 hours

      python3 newUtils/buildDirStruct.py 1 ALIC Alice_original.gdml $HOME/Downloads/CERN-Alice

      see also script buildALic


### Latest Status

BrepShell is a Brep where totally enclosed shapes have been omitted

26/12/23

 * ProcessDirStruct_BrepShell.FCMacro
      Create BrepShell's in directory structure
 * ProcessDir_BrepShell.FCMacro
      Create BrepShells for all gdml files in a directory

23/11/23

Use the followings Macros to create Step & Brep files

  * ProcessDirStruct_Brep.FCMacro
  * ProcessDirStruct_Step.FCMacro
    
Remember that these need to be copied to FreeCAD's Macro directory

 * On MacOS is /Users/<user>/Library/Application Support/FreeCAD/Macro
 * On Linux is ???
 * On Windows is ???

Do not use ProcessDirStruct.FCMacro this is being retained and will be updated in the future

29/10/23

Latest version of GDML workbench https://github.com/KeithSloan/GDML supports 

   * Expansion
   * Expansion Max

of GDMLPartStep Objects as created by the ProcessDirStruct.FCMacro

26/10/23

Add ProcessDirStruct.FCMacro to process directory structure and create STEP files.
Needs to be copied to FreeCAD Macro directory.

Needs latest version of importGDML from GDML workbench.

Note: ProcessDirStruct.py part developed to be retained just in case.

30/09/23

Success in extracting Volume Dipole and loading into Geant4

![Image 30-09-2023 at 18 29](https://github.com/KeithSloan/CERN-Alice-MultiFile-gdml/assets/2291247/500367f2-5326-465a-bdb9-2046ea8a2daa)

run testDipole script to create extracted directory.

From Geant4 G01

./load_color_gdml $HOME/Downloads/CERN-Dipole/Dipole/Dipole.gdml


04/04/23

Fixes for volume and assembly structure

testAlice - ran to completion in 12 hours approx

CERN-Alice - 272.4 Mb


27/03/23

testAlice - ran. took several days but not to completion, not sure if resource or bug, need to try again.
            but seems to have created a good structure for what was processed.
            
GDML workbench https://github.com/KeithSloan/GDML/tree/Main/freecad/gdml has been updated such that on a scan,
     where before it would create a Part with Not_Expanded it now checks if the scan is on a directory structure
     and if a step files exits for the said Part. It then creats a new GDMLPartStep Object
     
The appropriate step files have been created in  Subdirectory Dipole/DCoil    

The next stage is to test if this approach might work for large directories/Volumes like B077

Note: B077_struct.xml exceeds github file size limit, so needs decompressing before use.


# CERN-Alice-MultiFile-gdml

One of the aims of this exercise/project is to provide a testing/proving ground for the the FreeCAD GDML workbench

https://github.com/KeithSloan/GDML. 

At present the workbench struggles with large GDML files, this is down to two reasons

1. Software Bugs
2. Slowness of the Python code.

In an attempt to address these isssues the Workbench offers a facility to **scan** rather than import a GDML file.

The scan just parses the file for first level GDML Volumes (Base Volumes) which it then indicates as **NOT Expanded**.
The workbench then offers two facilites to select an individual  **NOT Expanded** Volume and expand it.
Having expanded an individual Volume, if one then selects the root/world volume ( First / highlest level App::Part in FreeCAD ) and invoke the standard FreeCAD export facility, one then can create a GDML file for just the selected expanded volume. This can either be a single GDML file if the file extension used is lower case **gdml** or a multi files version. If an upper case **GDML** file extension is used then the path name without the **GDML** is used to create a directory which includes a gdml file that has includes for individual XML files for the various sections of a GDML file namely

* Constants
* Defines
* Materials
* Solids
* Structure

One can then deleted the expanded Volume and repeat the exercise for another base GDML Volume (First level FreeCAD App::Part) 

In addition it is possible to select the root/world volume and use the standard FreeCAD facility to export a STEP file version.

The idea being that having created such directories, then it should not be too arduous to create a gdml file that would recombine base volumes.
i.e. a GDML file with includes for the common sections and a number of individual files (Solids and Structure).

Obviously a combination of all base voumes would still be an issue for the Workbench, but should be loadable into Geant4. For ROOT that does
not support imbeded GDML files, then one should be able to use the supplied standalone python utility **CombineGDML.py** ( in the Workbenches **Utils** directory)
to process the Multi-file GDML version and produce a single file GDML version.

At the present time it is bugs in the workbench handling of GDML assemblies that is holding up this project/exercise

The plan is also to add the facility to the workbench to import XML files with solids and structure definitions so that one could work on the GDML
of a Base Volume whilst also having neighbouring base volumes loaded.
