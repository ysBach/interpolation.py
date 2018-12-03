import numpy as np
from numba import jit, generated_jit
from numpy import zeros
from numpy import floor

from numba import prange
from codegen import get_code_linear, get_code_cubic, source_to_function

#

Ad = np.array([
#      t^3       t^2        t        1
   [-1.0/6.0,  3.0/6.0, -3.0/6.0, 1.0/6.0],
   [ 3.0/6.0, -6.0/6.0,  0.0/6.0, 4.0/6.0],
   [-3.0/6.0,  3.0/6.0,  3.0/6.0, 1.0/6.0],
   [ 1.0/6.0,  0.0/6.0,  0.0/6.0, 0.0/6.0]
])
dAd = zeros((4,4))
for i in range(1,4):
    dAd[:,i] = Ad[:,i-1]*(4-i)

# @generated_jit(nopython=True)
# def v_eval_cubic(grid,C,points,out):
#     d = len(grid.types)
#     vector_valued = (C.ndim==d+1)
#     context = {'floor': floor,'Cd': Ad, 'dCd': dAd}
#     code = ( templ_vec.substitute(d=d, vector_valued=vector_valued, get_values=get_values) )
#     f = source_to_function(code, context=context)
#     return f

from numba import njit
from numba.extending import overload

def _eval_cubic():
    pass

@overload(_eval_cubic)
def __eval_cubic(grid,C,points,out):
    d = len(grid)
    n_x = len(grid.types)
    vector_valued = (C.ndim==d+1)
    vec_eval = (points.ndim==2)
    from math import floor
    from numpy import zeros
    context = {'floor': floor, 'zeros': zeros, 'Cd': Ad, 'dCd': dAd}

    code = get_code_cubic(d, vector_valued=vector_valued, vectorized=vec_eval, allocate=False)
    print(code)
    f = source_to_function(code, context)
    return f


@overload(_eval_cubic)
def __eval_cubic(grid,C,points):
    d = len(grid)
    n_x = len(grid.types)
    vector_valued = (C.ndim==d+1)
    vec_eval = (points.ndim==2)
    from math import floor
    from numpy import zeros
    context = {'floor': floor, 'zeros': zeros, 'Cd': Ad, 'dCd': dAd}

    code = get_code_cubic(d, vector_valued=vector_valued, vectorized=vec_eval, allocate=True)

    print(code)
    f = source_to_function(code, context)
    return f

@njit
def eval_cubic(*args):
    return _eval_cubic(*args)

import numba
import numpy as np
from numba import njit
from numba.extending import overload

def _eval_linear():
    pass
from codegen import get_code_linear

@overload(_eval_linear)
def __eval_linear(grid,C,points,out):
    d = len(grid)
    n_x = len(grid.types)
    vector_valued = (C.ndim==d+1)
    vec_eval = (points.ndim==2)
    grid_types = ['nonuniform' if isinstance(tt, numba.types.Array) else 'uniform' for tt in grid.types]

    context = {'floor': floor, 'zeros': zeros, 'np': np} #, 'Cd': Ad, 'dCd': dAd}

    print(dict(d=d, vector_valued=vector_valued, vectorized=vec_eval, allocate=False, grid_types=grid_types))

    code = get_code_linear(d, vector_valued=vector_valued, vectorized=vec_eval, allocate=False, grid_types=grid_types)

    print(code)
    f = source_to_function(code, context)
    return f


@overload(_eval_linear)
def __eval_linear(grid,C,points):
    d = len(grid)
    n_x = len(grid.types)
    vector_valued = (C.ndim==d+1)
    vec_eval = (points.ndim==2)
    from math import floor
    from numpy import zeros

    grid_types = ['nonuniform' if isinstance(tt, numba.types.Array) else 'uniform' for tt in grid.types]

    context = {'floor': floor, 'zeros': zeros, 'np': np} #, 'Cd': Ad, 'dCd': dAd}
    print(dict(d=d, vector_valued=vector_valued, vectorized=vec_eval, allocate=False, grid_types=grid_types))

    code = get_code_linear(d, vector_valued=vector_valued, vectorized=vec_eval, allocate=True, grid_types=grid_types)
    print(code)

    f = source_to_function(code, context)
    return f

@njit
def eval_linear(*args):
    """Do I get a docstring ?"""
    return _eval_linear(*args)


# print(templ.substitute(d=2, vector_valued=2, get_values=get_values, allocate=True))
# print(templ.substitute(d=2, vector_valued=2, get_values=get_values, allocate=False))
# print(templ.substitute(d=2, vector_valued=False, get_values=get_values, allocate=False))
#
#
# print(templ_vec.substitute(d=2, vector_valued=False, get_values=get_values, allocate=False))
# print(templ_vec.substitute(d=2, vector_valued=False, get_values=get_values, allocate=True))
#
# print(templ_vec.substitute(d=2, vector_valued=True, get_values=get_values, allocate=True))
