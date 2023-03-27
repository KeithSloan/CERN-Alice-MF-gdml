import sys, os

if len(sys.argv) < 3 :
    print(f"Usage {sys.argv[0]} <directory> <volume>")
    sys.exit(1)

directory = sys.argv[1]
volume =  sys.argv[2]

print(f"Creating Brep for Volume{volume} in Directory{directory}")
