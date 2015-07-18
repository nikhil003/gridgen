"""
    This script is for testing the use of gridgen from 
    octant where I am using the examples given by 
    Pavel Sakov.
"""
import sys
import os
try:
    from octant.grid import Gridgen
except ImportError:
    try:
        from prygridgen.grid import Gridgen
    except ImportError:
        if os.name is 'posix':
            os.system('clear')
        else:
            os.system('cls')
        print "=========================================="
        print ""
        print "Check where is your gridgen module located"
        print ""
        print "=========================================="
        print ""
        sys.exit()
import numpy as np
from matplotlib.pyplot import plot, show, xlabel, ylabel, title, clf, close, figure, tight_layout
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages



rcParams.update({'font.size':7})
with PdfPages('gridgen_python.pdf') as pdf:
    for i in xrange(6):
        params = {}
        #read the parameter files and store in a dictionary
        with open('prm.'+str(i)) as tempfile:
            for row in tempfile.readlines():
                if row.split()[0] in ['nx','ny','nnodes','newton']:
                    params[row.split()[0]] = int(row.split()[1])
                elif row.split()[0] == 'precision':
                    params[row.split()[0]] = float(row.split()[1])
                else:
                    params[row.split()[0]] = row.split()[1]
        #read the coordinates files and add them to lists
        coordinates = []
        beta = []
        with open(params['input']) as inputfile:
            for row in inputfile.readlines():
                if row.startswith('#'):
                    pass
                elif row == '\n':
                    pass
                else:
                    coordinates.append([float(row.split()[0]), float(row.split()[1])])
                    if len(row.split()) > 2:
                        if row.split()[-1][-1] == '*':
                            if len(row.split()[-1]) == 2:
                                beta.append(float(row.split()[-1][:1]))
                            else:
                                beta.append(float(row.split()[-1][:2]))
                        else:
                            beta.append(float(row.split()[-1]))
                    else:
                        beta.append(float(0))

        coordinates = np.array(coordinates)
        #print params['nx'], params['ny']
        #generate grid using gridgen class from octant
        #it should work similary with prygridgen,
        #by changing modifying the name above
        grid = Gridgen(coordinates[:,0], coordinates[:,1], beta, (params['ny'],\
            params['nx']), ul_idx=0, nnodes=params['nnodes'],\
            precision=params['precision'], verbose=True)

        #generate the figures and save them to the pdf file    
        fig = figure(figsize=(4, 4))
        if i == 0:
            marker1 = 'k.-'; marker2='b.-'
        else:
            marker1 = 'k-'; marker2='b-'
        ax = fig.add_subplot(111)
        ax.plot(coordinates[:,0], coordinates[:,1], marker1, lw=0.3, markersize=1.2)
        ax.plot(grid.x, grid.y, marker2, lw=0.3, markersize=1.2)
        ax.plot(grid.x.T, grid.y.T, marker2, lw=0.3, markersize=1.2)
        ax.scatter(coordinates[:,0], coordinates[:,1], 10, \
            c=beta, marker='o',facecolors='none')
        ax.set_xlim(coordinates[:,0].min() - 0.5, coordinates[:,0].max() + 0.5)
        ax.set_ylim(coordinates[:,1].min() - 0.5, coordinates[:,1].max() + 0.5)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_title('grid.'+str(i))
        tight_layout()
        #savefig('grid_'+str(i)+'.png', dpi=300, bbox_inches='tight')
        pdf.savefig()
        clf()
        close('all')



