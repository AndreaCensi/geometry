from contracts.main import contract
import numpy as np
from string import ljust


def printm(*args):
    print(formatm(*args))
    
def formatm(*args):
    #name_len = 10
    assert len(args) > 0
    assert len(args) % 2 == 0
    cols = []
    for i in range(len(args) / 2):
        name = args[i * 2]
        matrix = args[i * 2 + 1]
        assert isinstance(name, str)
        assert isinstance(matrix, np.ndarray)
#        varname = '  %s:' % rjust(name, name_len)
        varname = '  %s:' % name
        if matrix.ndim > 1:
            varname = '\n' + varname 
        cols.append(varname) 
        cols.append(format_matrix(matrix))
        
    cols = add_spacer(cols)
    return join_columns(cols)

def add_spacer(cols, spacer=' '):
    r = []
    for c in cols:
        r.append(c)
        r.append(spacer)
    return r[:-1]

@contract(cols='list(str)')
def join_columns(cols): 
    # split lines
    cols = [x.split('\n') for x in cols]
    # count max number of rows
    nrows = max([len(col) for col in cols])
    # get row of one column or empty string
    get_cell = lambda col, i: col[i] if len(col) > i else ''
    # get maximum length of column
    col_width = lambda col: max([len(cell) for cell in col])
    col_widths = [col_width(col) for i, col in enumerate(cols)]
    s = ''
    for j in range(nrows):
        srow = ''
        for i, col in enumerate(cols):
            cell = get_cell(col, j) 
            cell = ljust(cell, col_widths[i])
            srow += cell
        s += srow + '\n'
    return s
    
def format_matrix(matrix, fsize=8):
    if matrix.ndim == 2:
        nrows, ncols = matrix.shape
        cols = [ [] for i in range(ncols) ] #@UnusedVariable
        for j in range(ncols):
            for i in range(nrows):
                s = ' %g' % matrix[i, j]
                cols[j].append(s)
        cols = [ "\n".join(col) for col in cols]
        borders = "\n".join(["|" for i in range(nrows)])
        bcols = []
        bcols.append(borders)
        bcols.extend(cols)
        bcols.append(borders)
        return join_columns(bcols)
    return "%s" % matrix

if __name__ == '__main__':
    
    A = np.eye(3)
    B = np.random.randn(3, 4)
    printm('A (identity):', A, 'B (random):', B)
    
    
    
