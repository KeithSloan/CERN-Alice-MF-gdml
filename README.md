### Latest Status

22/10/23

Work on FreeCAD Macro ProcessDirStruct.FCMacro to process directory and create relevanet STEP file is progressing see branch buildSteps.

Next stage ( GDML workbench branch BrepStep ) is to update importGDML to

 * Be able to pass type of import as an option rather than prompt.
 * If import option is Step for Volumes where a step file exist create GDMLPartStep where Shape is created by importing the Step

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
