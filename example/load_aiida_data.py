

import os, sys
from os import listdir
from os.path import isfile, join
from aiida.orm.data.structure import StructureData
from ase.io import read, write
from aiida.common.exceptions import UniquenessError
from aiida.orm.data.singlefile import SinglefileData

UpfData = DataFactory('upf')

mypath = os.getcwd()
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if 'Pd.cif' not in files or 'Pd_isolated-atom.cif' not in files or 'Wien2k.txt' not in files:
    raise Exception("Files are missing in the current directory! You need to have: 'Pd.cif', 'Pd_isolated-atom.cif' and 'Wien2k.txt' (to be taken from calcDelta package)")


# Store structure of elemental Pd
atoms = read('{}/Pd.cif'.format(mypath))
structure = StructureData(ase=atoms)
n = structure.store()

print 'StructureData of elemental Pd obtained from Pd.cif has pk = {}'.format(str(n.pk))

# Add structure of Pd atom in AiiDA group
g = Group.get_or_create(name='Isolated_atoms')
atoms = read('{}/Pd_isolated-atom.cif'.format(mypath))
structure = StructureData(ase=atoms)
n = structure.store()
g.add_nodes(n)

print "Added structure (pk = {}) obtained from Pd_isolated-atom.cif to AiiDA group 'Isolated_atoms'".format(n.pk)


# Add SinglefileData with Wien2k results for the equations of states
f = SinglefileData()
f.set_file('{}/Wien2k.txt'.format(mypath))
f.store()

print 'SinglefileData obtained from text file Wien2k.txt has pk = {}'.format(str(f.pk))




#from aiida.orm.data.singlefile import SinglefileData
#try:
#    g = Group.get_or_create(name='pslib.0.3.1_PBE_PAW', type_string='UpfData')
#except UniquenessError:
#    g = Group.get(name='pslib.0.3.1PBE_PAW', type_string='UpfData')
#u = UpfData()
#u.set_file('{}/Pd.pbe-n-kjpaw_psl.0.3.0.UPF'.format(mypath))
#u.store()
#g.add

