
import re
import json
import numpy as np
import xml.etree.ElementTree as ET
import os
from .lib import get_slope

def parse(file:str,step:int=10):
    return _execparse(file, step)

def parse_dir(dir:str, step:int=10):
    grids = []
    slopes = []
    paths = os.listdir(dir) 
    for path in paths:
        res = _execparse(os.path.join(dir, path), step)
        grids.append(res['grid'])
        slopes += res['slopes']
    return dict(grids=grids, slopes=slopes) 


def _execparse(file:str, step:int):   
    demtree = ET.parse(file) 
    demroot = demtree.getroot()

    
    ns = { 'xml': 'http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema',
        'gml': 'http://www.opengis.net/gml/3.2' }
    demdem = demroot.find( 'xml:DEM', ns )
    
  
        
    demcoverage = demdem.find( 'xml:coverage', ns )

    dembounded_by = demcoverage.find( 'gml:boundedBy', ns )
    dem_envelope = dembounded_by.find( 'gml:Envelope', ns )
    
    lat_sw, lon_sw = [float(token) for token in re.split('\s+',dem_envelope.find( 'gml:lowerCorner', ns ).text.strip())]
    lat_ne, lon_ne = [float(token) for token in re.split('\s+', dem_envelope.find('gml:upperCorner', ns).text.strip())]
     
    dem_grid_domain = demcoverage.find( 'gml:gridDomain', ns )
    dem_grid = dem_grid_domain.find( 'gml:Grid', ns )
    demlimits = dem_grid.find( 'gml:limits', ns )
    dem_grid_envelope = demlimits.find( 'gml:GridEnvelope', ns )
   
    max_x, max_y = [int(token) + 1 for token in re.split('\s+', dem_grid_envelope.find('gml:high', ns).text.strip())]
    dem_range_set = demcoverage.find( 'gml:rangeSet', ns )
    dem_data_block = dem_range_set.find( 'gml:DataBlock', ns )
    alt_list = dem_data_block.find( 'gml:tupleList', ns ).text.strip().splitlines()
    dem_coverage_function = demcoverage.find( 'gml:coverageFunction', ns )
    dem_grid_function = dem_coverage_function.find( 'gml:GridFunction', ns )
    start_x,start_y = [float(token) for token in  re.split('\s+', dem_grid_function.find( 'gml:startPoint', ns ).text.strip())]
 
   


    i = 0.0
    y = start_y
    lat_step = (lat_ne - lat_sw) / (max_y - start_y)
    lon_step = (lon_ne - lon_sw) / (max_x - start_x)
    
    grid_coord = []
    grid_coord_row = []
    alts = []
    alts_row = []

    for line in alt_list:
        if not line:
            continue
    
        alt = float(line.strip().split(',')[1])
       
        x = (start_x + i)
        lat_grid = lat_ne - lat_step * (y + 0.5)
        lon_grid = lon_sw +  lon_step * (x  + 0.5)
        grid_coord_row.append(lon_grid + lat_grid * 1j)
        alts_row.append(alt)

        i += 1.0
        if i == max_x:
            y += 1.0
            i = 0.0
            grid_coord.append(grid_coord_row)
            grid_coord_row = []
            alts.append(alts_row)
            alts_row = []
    if grid_coord_row:
        grid_coord.append(grid_coord_row)
    if alts_row:
        alts.append(alts_row)
    grid_coord_np = np.array(grid_coord)
    alts_np = np.array(alts)
    slope = get_slope(alts_np)
    slope_list = []
    
    step_v = slope.shape[0] / step
    step_h = slope.shape[1] / step
    for slope_v, grid_coord_v in zip(np.array_split(slope, step_v, 0), np.array_split(grid_coord_np, step_v, 0)):
        for slope_vh, grid_coord_vh in zip(np.array_split(slope_v, step_h, 1), np.array_split(grid_coord_v, step_h, 1)):
            slope_avg = np.average(slope_vh)
            grid_coord_avg = np.average(grid_coord_vh)
            slope_dict = {
                'vector':{
                    'lat':slope_avg.imag,
                    'lon':slope_avg.real
                },
                'coord':{
                    'lat':grid_coord_avg.imag,
                    'lon':grid_coord_avg.real
                }

            }
            slope_list.append(slope_dict)
    grid = {
        'ne':{
            'lat':lat_ne,
            'lon':lon_ne
        },
        'sw':{
            'lat':lat_sw,
            'lon':lon_sw
        }
    }
    data = {
        'grid':grid,
        'slopes':slope_list,

    
    }

    return data

    
    
            









        
        

        


    
    



      
    







