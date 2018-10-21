# coding=utf-8
import numpy as np
from contracts import contract, describe_type, describe_value


def printm(*args):
    print(formatm(*args))


def formatm(*args, **kwargs):
    # name_len = 10
    assert len(args) > 0
    assert len(args) % 2 == 0
    cols = []
    for i in range(int(len(args) / 2)):
        name = args[i * 2]
        matrix = args[i * 2 + 1]
        if not isinstance(name, str):
            raise ValueError('I expect a string for label, not %s.'
                             % describe_type(name))
        #        varname = '  %s:' % rjust(name, name_len)
        varname = '  %s:' % name

        if isinstance(matrix, np.ndarray):
            #            raise ValueError('I expect a numpy array for value, not %s.' %
            #                             describe_type(matrix))
            value = format_matrix(matrix, **kwargs)
            if matrix.ndim > 1:
                varname = '\n' + varname
        else:
            value = describe_value(matrix)

        cols.append(varname)
        cols.append(value)

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
            cell = cell.ljust(col_widths[i])
            srow += cell
        s += srow + '\n'
    return s


def format_matrix(matrix, fsize=8, format_str='%g'):  # @UnusedVariable
    if matrix.ndim == 2:
        nrows, ncols = matrix.shape
        cols = [[] for _ in range(ncols)]
        for j in range(ncols):
            for i in range(nrows):
                s = (' ' + format_str) % matrix[i, j]
                cols[j].append(s)
        cols = ["\n".join(col) for col in cols]
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
