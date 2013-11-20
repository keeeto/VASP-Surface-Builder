#! /usr/bin/env python

"""Convert a Crystallographic .cif file to VASP POSCAR"""

import ase
#from ase.io import read
from ase.io import write
from ase.io import vasp
from optparse import OptionParser
from ase.lattice import surface

parser = OptionParser()
parser.add_option("-f", "--file",
                  action="store", type="string", dest="file", default="POSCAR",
                  help="Path to input file [default: POSCAR]")
# Add further options here
(options, args) = parser.parse_args()
# Ensire that the input files exist
try:
 with open(options.file) as tmp: pass
 coordinates = ase.io.read(options.file,index=-1,format='vasp')
except IOError as e:
 print 'Could not find a coordinates file, this file is specified with the -f flag, default input.xyz'
tmp.close()

# Read the coordinates & lattice information
coordinates = ase.io.read(options.file,index=-1,format='vasp')

# Generate the surfaces
n_layers = 2           # The smallest surface
while n_layers < 8:
    surface = ase.lattice.surface.surface(coordinates,(1,0,0),n_layers,vacuum=10)
    ase.io.vasp.write_vasp('POSCAR.%s.vasp'%n_layers,surface,direct=False,sort=True)
    n_layers = n_layers + 1

