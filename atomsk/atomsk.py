import os
import shutil
import numpy as np

def CreateAtomFile(structure, a0, at, filename, duplicate="1 1 1", silence=False):
	CheckAtom(at)
	if os.path.isfile(filename):
		os.remove(filename)
	if duplicate != "1 1 1":
		command = "atomsk --create " + structure + " " + a0 + " " + at + " -duplicate " + duplicate + " " + filename
	else:
		command = "atomsk --create " + structure + " " + a0 + " " + at + " " + filename
	if silence == True:
		command += " > output.lmp"
	os.system(command)
	if silence != True:
		print("Created file for " + at + " " + structure + " in " + filename)

def MergeBoxes(files, destination, rep="",  direction="z", silence=False): # atomsk --merge z 2 data1.lmp data2.lmp interface.xyz

	if os.path.isfile(destination):
		os.remove(destination)

	command = "atomsk --merge " + direction + " " + str(len(files)) + " " + " ".join(files) + " " + destination
	if silence == True:
		command += " > output.lmp"
	os.system(command)
	if rep != "":
		shutil.copyfile(destination, rep + destination)
		os.remove(destination)
	if silence != True:
		print("Merged " + str(files) + " in " + destination)

def AddAtomTetra(startFile, finalFile, a0, boxSize, atom="H", atomCoor=[0, 0, 0], dirx=[1,0,0], diry=[0,1,0], dirz=[0,0,1], dirNeigh=1, silence=False):
	CheckAtom(atom)
	a = a0 / 4
	# Convert directions to [001] base
	x, y, z = ConvertDirectionsTo001([dirx, diry, dirz], atomCoor)
	# Direction from atom
	if dirNeigh == 1 or dirNeigh == "xyz":
		px, py, pz = [x * a0 + a, y * a0 + a, z * a0 + a]
	elif dirNeigh == 2 or dirNeigh == "-xyz":
		px, py, pz = [x * a0 - a, y * a0 + a, z * a0 + a]
	elif dirNeigh == 3 or dirNeigh == "-x-yz":
		px, py, pz = [x * a0 - a, y * a0 - a, z * a0 + a]
	elif dirNeigh == 4 or dirNeigh == "x-yz":
		px, py, pz = [x * a0 + a, y * a0 - a, z * a0 + a]
	elif dirNeigh == 5 or dirNeigh == "xy-z":
		px, py, pz = [x * a0 + a, y * a0 + a, z * a0 - a]
	elif dirNeigh == 6 or dirNeigh == "-xy-z":
		px, py, pz = [x * a0 - a, y * a0 + a, z * a0 - a]
	elif dirNeigh == 7 or dirNeigh == "-x-y-z":
		px, py, pz = [x * a0 - a, y * a0 - a, z * a0 - a]
	elif dirNeigh == 8 or dirNeigh == "x-y-z":
		px, py, pz = [x * a0 + a, y * a0 - a, z * a0 - a]
	else:
		raise ValueError("Wrong coordinates for neighbor. Try 1-8 or xyz.")
	
	Lx, Ly, Lz = np.multiply(boxSize, a0)
	# Periodic boundaries
	if px > Lx:
		px -= Lx
	if py > Ly:
		py -= Ly
	if pz > Lz:
		pz -= Lz
	if px < 0:
		px += Lx
	if py < 0:
		py += Ly
	if pz < 0:
		pz += Lz
	pos = str(px) + " " + str(py) + " " + str(pz)
	if os.path.isfile(finalFile):
		os.remove(finalFile)

	command = "atomsk " + startFile + " -add-atom " + atom + " at " + pos + " " + finalFile
	if silence == True:
		command += " > atomsk.out"
	os.system(command)
	if silence != True:
		print("Added " + atom + " atom at position " + pos)

def AddAtomOcta(startFile, finalFile, a0, boxSize, atom="H", atomCoor=[0, 0, 0], dirx=[1,0,0], diry=[0,1,0], dirz=[0,0,1], dirNeigh=1, silence=False):
	CheckAtom(atom)
	a = a0 / 2
	# Convert directions to [001] base
	x, y, z = ConvertDirectionsTo001([dirx, diry, dirz], atomCoor)
	# Direction from atom
	if dirNeigh == 1 or dirNeigh == "x":
		px, py, pz = [x * a0 + a, y * a0, z * a0]
	elif dirNeigh == 2 or dirNeigh == "y":
		px, py, pz = [x * a0, y * a0 + a, z * a0]
	elif dirNeigh == 3 or dirNeigh == "z":
		px, py, pz = [x * a0, y * a0, z * a0 + a]
	elif dirNeigh == 4 or dirNeigh == "-x":
		px, py, pz = [x * a0 - a, y * a0, z * a0]
	elif dirNeigh == 5 or dirNeigh == "-y":
		px, py, pz = [x * a0, y * a0 - a, z * a0]
	elif dirNeigh == 6 or dirNeigh == "-z":
		px, py, pz = [x * a0, y * a0, z * a0 - a]
	elif dirNeigh == 7 or dirNeigh == "xyz":
		px, py, pz = [x * a0 + a, y * a0 + a, z * a0 + a]
	elif dirNeigh == 8 or dirNeigh == "-xyz":
		px, py, pz = [x * a0 - a, y * a0 + a, z * a0 + a]
	elif dirNeigh == 9 or dirNeigh == "-x-yz":
		px, py, pz = [x * a0 - a, y * a0 - a, z * a0 + a]
	elif dirNeigh == 10 or dirNeigh == "x-yz":
		px, py, pz = [x * a0 + a, y * a0 - a, z * a0 + a]
	elif dirNeigh == 11 or dirNeigh == "xy-z":
		px, py, pz = [x * a0 + a, y * a0 + a, z * a0 - a]
	elif dirNeigh == 12 or dirNeigh == "-xy-z":
		px, py, pz = [x * a0 - a, y * a0 + a, z * a0 - a]
	elif dirNeigh == 13 or dirNeigh == "-x-y-z":
		px, py, pz = [x * a0 - a, y * a0 - a, z * a0 - a]
	elif dirNeigh == 14 or dirNeigh == "x-y-z":
		px, py, pz = [x * a0 + a, y * a0 - a, z * a0 - a]
	else:
		raise ValueError("Wrong coordinates for neighbor. Try 1-14 or xyz.")
	
	Lx, Ly, Lz = np.multiply(boxSize, a0)
	# Periodic boundaries
	if px > Lx:
		px -= Lx
	if py > Ly:
		py -= Ly
	if pz > Lz:
		pz -= Lz
	if px < 0:
		px += Lx
	if py < 0:
		py += Ly
	if pz < 0:
		pz += Lz
	pos = str(px) + " " + str(py) + " " + str(pz)
	if os.path.isfile(finalFile):
		os.remove(finalFile)

	command = "atomsk " + startFile + " -add-atom " + atom + " at " + pos + " " + finalFile
	if silence == True:
		command += " > atomsk.out"
	os.system(command)
	if silence != True:
		print("Added " + atom + " atom at position " + pos)

def AddVoid(filename, destination):
	if os.path.isfile(destination):
		os.remove(destination)
	os.system("atomsk " + filename + " -cell add 4 z " + destination)

def ConvertDirectionsTo001(iDir, iCoor):
	invDir = np.linalg.inv(iDir)
	coor = np.matmul(invDir, iCoor)
	return coor

def CheckAtom(atom):
	perTable = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na",
				"Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti",
				"V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As",
				"Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru",
				"Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs",
				"Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
				"Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir",
				"Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra",
				"Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es",
				"Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
				"Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
	if atom not in perTable:
		raise ValueError("Atom type not found in periodic table. Please use existing atoms.")

