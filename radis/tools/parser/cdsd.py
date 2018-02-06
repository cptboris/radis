# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:58:40 2017

@author: erwan

"""

# TODO: remove wangl2  after loading database (wangl is enough, with 1=e and 2=f)

from __future__ import print_function, absolute_import, division, unicode_literals

import pandas as pd
import numpy as np
from collections import OrderedDict
import os
from os.path import exists, splitext
from radis.tools.parser.hiparser import _cast_to_dtype, _format_dtype
import sys
from six.moves import zip

columns_hitemp = OrderedDict([ (
               # name    # format # type  # description                                 # unit 
               'id',     ('a2',   int,   'Molecular number'                               ,''                      )),(
               'iso',    ('a1',   int,   'isotope number'                                 ,''                      )),(
               'wav',    ('a12',  float, 'vacuum wavenumber'                              ,'cm-1'                  )),(
               'int',    ('a10',  float, 'intensity at 296K'                              ,'cm-1/(molecule/cm-2)', )),(
               'A',      ('a10',  float, 'Einstein A coefficient'                         ,'s-1'                   )),(
               'airbrd', ('a5',   float, 'air-broadened half-width at 296K'               ,'cm-1.atm-1'            )),(
               'selbrd', ('a5',   float, 'self-broadened half-width at 296K'              ,'cm-1.atm-1'            )),(
               'El',     ('a10',  float, 'lower-state energy'                             ,'cm-1'                  )),(
               'Tdpair', ('a4',   float, 'temperature-dependance exponent for Gamma air'  ,''                      )),(
               'Pshft',  ('a8',   float,  'air pressure-induced line shift at 296K'       ,'cm-1.atm-1'            )),(
                       # skip 1 columns   . WARNING. They didn't say that in the doc. But it doesn't make sense if i don't
               'Tdpsel', ('a5',   float, 'temperature dependance exponent for gamma self' ,''                      )),(
               'v1u',    ('a3',   int,   'upper state vibrational number v1'              ,''                      )),(
               'v2u',    ('a2',   int,   'upper state vibrational number v2'              ,''                      )),(
               'l2u',    ('a2',   int,   'upper state vibrational number l2'              ,''                      )),(
               'v3u',    ('a2',   int,   'upper state vibrational number v3'              ,''                      )),(
               'ru',     ('a1',   int,   'upper state vibrational number r'               ,''                      )),(
                       # skip 5 columns (v1l format becomes 3+5)
               'v1l',    ('a8',   int, 'lower state vibrational number v1'                ,''                      )),(
               'v2l',    ('a2',   int,   'lower state vibrational number v2'              ,''                      )),(
               'l2l',    ('a2',   int,   'lower state vibrational number l2'              ,''                      )),(
               'v3l',    ('a2',   int,   'lower state vibrational number v3'              ,''                      )),(
               'rl',     ('a1',   int,   'lower state vibrational number r'               ,''                      )),(
               'polyu',  ('a3',   int,   'upper state polyad'                             ,''                      )),(
               'wangu',  ('a2',   int,   'upper state Wang symmetry'                      ,''                      )),(
               'ranku',  ('a4',   int,   'upper state ranking number'                     ,''                      )),(
               'polyl',  ('a3',   int,   'lower state polyad'                             ,''                      )),(
               'wangl',  ('a2',   int,   'lower state Wang symmetry'                      ,''                      )),(
               'rankl',  ('a4',   int,   'lower state ranking number'                     ,''                      )),(
                       # skip 2 columns (PQR format becomes 1+2)
               'branch',    ('a3',   str,   'O, P, Q, R, S branch symbol'                                        ,''                      )),(
               'jl',     ('a3',   int,   'lower state rotational quantum number'          ,''                      )),(
               'wangl2', ('a1',   str,   'lower state Wang symmetry'                      ,'(e or f)'              )),(
               'lsrc',   ('a5',   int,   'line source'                                    ,''                      ))
                ])

columns_4000 = OrderedDict([ (
               # name    # format # type  # description                                 # unit 
               'id',     ('a2',   int,   'Molecular number'                               ,''                      )),(
               'iso',    ('a1',   int,   'isotope number'                                 ,''                      )),(
               'wav',    ('a12',  float, 'vacuum wavenumber'                              ,'cm-1'                  )),(
               'int',    ('a10',  float, 'intensity at 296K'                              ,'cm-1/(molecule/cm-2)', )),(
               'A',      ('a10',  float, 'Einstein A coefficient'                         ,'s-1'                   )),(
               'airbrd', ('a5',   float, 'air-broadened half-width at 296K'               ,'cm-1.atm-1'            )),(
               'selbrd', ('a5',   float, 'self-broadened half-width at 296K'              ,'cm-1.atm-1'            )),(
               'El',     ('a10',  float, 'lower-state energy'                             ,'cm-1'                  )),(
               'Tdpair', ('a4',   float, 'temperature-dependance exponent for Gamma air'  ,''                      )),(
               'Pshft',  ('a8',   float,  'air pressure-induced line shift at 296K'       ,'cm-1.atm-1'            )),(
                       # skip 1 columns   . WARNING. They didn't say that in the doc. But it doesn't make sense if i don't
               'Tdpsel', ('a5',   float, 'temperature dependance exponent for gamma self' ,''                      )),(
               'v1u',    ('a3',   int,   'upper state vibrational number v1'              ,''                      )),(
               'v2u',    ('a2',   int,   'upper state vibrational number v2'              ,''                      )),(
               'l2u',    ('a2',   int,   'upper state vibrational number l2'              ,''                      )),(
               'v3u',    ('a2',   int,   'upper state vibrational number v3'              ,''                      )),(
               'ru',     ('a2',   int,   'upper state vibrational number r'               ,''                      )),(
                       # skip 5 columns (v1l format becomes 3+5)
               'v1l',    ('a6',   int, 'lower state vibrational number v1'                ,''                      )),(
               'v2l',    ('a2',   int,   'lower state vibrational number v2'              ,''                      )),(
               'l2l',    ('a2',   int,   'lower state vibrational number l2'              ,''                      )),(
               'v3l',    ('a2',   int,   'lower state vibrational number v3'              ,''                      )),(
               'rl',     ('a2',   int,   'lower state vibrational number r'               ,''                      )),(
               'polyu',  ('a3',   int,   'upper state polyad'                             ,''                      )),(
               'wangu',  ('a2',   int,   'upper state Wang symmetry'                      ,''                      )),(
               'ranku',  ('a4',   int,   'upper state ranking number'                     ,''                      )),(
               'polyl',  ('a3',   int,   'lower state polyad'                             ,''                      )),(
               'wangl',  ('a2',   int,   'lower state Wang symmetry'                      ,''                      )),(
               'rankl',  ('a4',   int,   'lower state ranking number'                     ,''                      )),(
                       # skip 2 columns (PQR format becomes 1+2)
               'branch', ('a3',   str,   'O, P, Q, R, S branch symbol'                    ,''                      )),(
               'jl',     ('a3',   int,   'lower state rotational quantum number'          ,''                      )),(
               'wangl2', ('a1',   str,   'lower state Wang symmetry'                      ,'(e or f)'              ))
                ])

def cdsd2df(fname, version='hitemp', count=-1, cache=False, verbose=True):
    ''' Convert a CDSD-HITEMP file to a Pandas dataframe 
    
    Input
    ----------
    
    fname: str
        CDSD file name 
        
    version: str ('4000', 'hitemp')
        CDSD version
        
    count: int
        number of items to read (-1 means all file)
        
    cache: boolean, or 'regen'
        if True, a pandas-readable HDF5 file is generated on first access, 
        and later used. This saves on the datatype cast and conversion and
        improves performances a lot (but changes in the database are not 
        taken into account). If False, no database is used. If 'regen', temp
        file are reconstructed. Default True. 
    
    Reference
    -----------
    
    CDSD-HITEMP / CDSD-4000 doc 
    
    
    Performance
    ----------
    
    I had huge performance trouble with this function, because the files are 
    huge (500k lines) and the format is to special (no space between numbers...)
    to apply optimized methods such as pandas's. A line by line reading isn't
    so bad, using struct to parse each line. However, we waste typing determining
    what every line is. I ended up using the fromfiles functions from numpy,
    not considering '\n' as a special character anymore, and a second call
    to numpy to cast the correct format. That ended up being twice as fast. 
    
    - initial:                      20s / loop
    - with mmap:                    worse 
    - w/o readline().rstrip('\n'):  still 20s
    - numpy fromfiles:              17s
    - no more readline, 2x fromfile 9s
    
    Think about using cache mode too:
    - no cache mode                 9s
    - cache mode, first time        22s
    - cache mode, then              2s
    
    Moving to HDF5:
    --------
    
    On cdsd_02069_02070 (56 Mb)
    
    Reading:
        
    >>> cdsd2df(): 9.29 s
    >>> cdsd2df(cache=True [old .txt version]): 2.3s 
    >>> cdsd2df(cache=True [new h5 version, table]): 910ms
    >>> cdsd2df(cache=True [new h5 version, fixed]): 125ms
    
    Storage:
        
    >>> %timeit df.to_hdf("cdsd_02069_02070.h5", "df", format="fixed")  337ms
    >>> %timeit df.to_hdf("cdsd_02069_02070.h5", "df", format="table")  1.03s

    '''
    
    if version == 'hitemp':
        columns = columns_hitemp
    elif version == '4000':
        columns = columns_4000
    else:
        raise ValueError('Unknown CDSD version: {0}'.format(version))
    
    if cache: # lookup if cached file exist. 
#        fcache = fname+'.cached'
        fcache = splitext(fname)[0]+'.h5'
        if exists(fcache):
            if cache == 'regen':
                os.remove(fcache)
                if verbose: print('Deleted h5 cache file : {0}'.format(fcache))
            else:
                if verbose: print('Using h5 file: {0}'.format(fcache))
    #            return pd.read_csv(fcache)
                return pd.read_hdf(fcache, 'df')

    # Create a dtype with the binary data format and the desired column names
    dtype = [(k, c[0]) for (k, c) in columns.items()]+[('_linereturn','a2')]
    try:
        dt = np.dtype([(str(k), c) for k, c in dtype])
        # Note: dtype names cannot be `unicode` in Python2. Hence the str()
    except TypeError:
        # Cant read database. Try to be more explicit for user
        print('Data type')
        print('-'*30)
        for (k, c) in dtype:
            print(str(k), '\t', c)
        print('-'*30)
        raise
        
    data = np.fromfile(fname, dtype=dt, count=count)
    
    # %% Cast to new type
    
    # get format of line return
    if sys.platform in ['linux', 'darwin']:
        linereturnformat = 'a1'
    elif sys.platform in ['win32']:
        linereturnformat = 'a2'
    else:
        raise ValueError('Line return format not defined for this OS: please update neq')  
    
    newtype = [c[0] if (c[1]==str) else c[1] for c in columns.values()]
    dtype = list(zip(list(columns.keys()), newtype))+[('_linereturn',linereturnformat)]
    data2 = _cast_to_dtype(data, dtype)

    # %% Create dataframe    
    df = pd.DataFrame(data2.tolist(), columns=list(columns.keys())+['_linereturn'])
    
    for k, c in columns.items():
        if c[1] == str:
            df[k] = df[k].str.decode("utf-8")
    
    # Strip whitespaces around PQR columns (due to 2 columns jumped)
    df.branch = df.branch.str.strip()
    
    # Delete dummy column than handled the line return character
    del df['_linereturn']
    
    if cache: # cached file mode but cached file doesn't exist yet (else we had returned)
        if verbose: print('Generating cached file: {0}'.format(fcache))
        try:
#            df.to_csv(fcache)
            df.to_hdf(fcache, 'df', format='fixed')
        except:
            if verbose: print('An error occured in cache file generation. Lookup access rights')
            pass
        
    return df 


def _test(verbose=True, warnings=True, **kwargs):
    ''' Analyse some default files to make sure everything still works'''
    from neq.test.utils import getTestFile
    from time import time
    
    t0 = time()
    df = cdsd2df(getTestFile('cdsd_hitemp_09.txt'))
    print('File loaded in {0:.1f}s'.format(time()-t0))
    if verbose: print(df.head())
    return df.wav[3] == 2250.00096


if __name__ == '__main__':
    print('Testing cdsd: ', _test())
