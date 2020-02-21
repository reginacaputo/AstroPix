#*******************************************************************#
#-------------------------------------------------------------------#
#---------------------------- AstroPix -----------------------------#
#-------------------------------------------------------------------#
#------------- Michela Negro - GSFC/UMBC - 2019/2020 ---------------#
#-------------------------------------------------------------------#
#*******************************************************************#

import os
import sys
import argparse
import numpy as np

__description__ = 'Creates the AstroPix geometry configurations'

formatter = argparse.ArgumentDefaultsHelpFormatter
PARSER = argparse.ArgumentParser(description=__description__, formatter_class=formatter)
PARSER.add_argument('-c', '--config', type=str, required=True,
                    help='the input configuration file')

if (sys.version_info > (3, 0)):
    from importlib.machinery import SourceFileLoader
    def get_var_from_file(filename):
        f = open(filename)
        global data
        data = SourceFileLoader('data', filename).load_module()
        f.close()
else:
    import imp
    def get_var_from_file(filename):
        f = open(filename)
        global data
        data = imp.load_source('data', '', f)
        f.close()

    
def run_mkGeometries(**kwargs):
	assert(kwargs['config'].endswith('.py'))
	get_var_from_file(kwargs['config'])
	
	passive = data.PASSIVE
	thickness = data.THICKNESS
	voxelsize = data.VOXELSIZE
	voxelnum = list((100./(np.array(voxelsize)/10)).astype('int'))
	geo_base = data.GEO_BASE
	det_base = data.DET_BASE
	
	line_thickness = 4
	line_passive = 5
	line_include_det = 9
	line_voxelnum = 1

	for i, p in enumerate(passive):
		print('PASSIVE %i: %i%%' %(i, p*100))
		for j, t in enumerate(thickness):	
			print('THICKNESS %i: %.2f cm' %(j, t/10000))
			for k, v in enumerate(voxelnum): 
				print('VOXEL SIZE %i: %.2f mm' %(k, voxelsize[k]))
				print('--> NUM. VOXELS: %ix%i' %(v, v))
				#___Create new folders and modify files___#
				folder_name = 'geo_%.2f_%i_%.2f'%(p, t, voxelsize[k])
				if not os.path.exists('geometry/%s' %folder_name):
					os.system('mkdir geometry/%s' %folder_name)
				geo_new = os.path.basename(geo_base).replace('base', '%.2f_%i_%.2f'%(p, t, voxelsize[k]))
				det_new = os.path.basename(det_base).replace('base', '%.2f_%i_%.2f'%(p, t, voxelsize[k]))
				os.system('cp %s geometry/%s/.' %(geo_base, folder_name))
				os.system('mv geometry/%s/%s geometry/%s/%s' \
					%(folder_name, os.path.basename(geo_base), folder_name, geo_new))
				geo_new_f = open('geometry/%s/%s'%(folder_name, geo_new), 'r')
				lines = geo_new_f.readlines()
				if 'Constant thickness' not in lines[line_thickness]:
					print('ATT: line number for the thickness parameter is not correct!')
					sys.exit()
				if 'Constant passive_thickness' not in lines[line_passive]:
					print('ATT: line number for the passive parameter is not correct!')
					sys.exit()
				if 'Include' not in lines[line_include_det] and '.det' not in lines[line_include_det]:
					print('ATT: line number  for the include is not correct!')
					sys.exit()
				line_list_t = lines[line_thickness].split()
				line_list_t[-1] = str(t/10000)+'\n'
				lines[line_thickness] = ' '.join(line_list_t)
				line_list_p = lines[line_passive].split()
				line_list_p[-1] = str(p)+'\n'
				lines[line_passive] = ' '.join(line_list_p)
				line_list_i = lines[line_include_det].split()
				line_list_i[-1] = det_new+'\n'
				lines[line_include_det] = ' '.join(line_list_i)
				with open('geometry/%s/%s'%(folder_name, geo_new), 'w') as f:
					for line in lines:
						f.write(line)
				geo_new_f.close()
				
				os.system('cp %s geometry/%s/.' %(det_base, folder_name))          
				os.system('mv geometry/%s/%s geometry/%s/%s' \
					%(folder_name, os.path.basename(det_base), folder_name, det_new))  
				det_new_f = open('geometry/%s/%s'%(folder_name, det_new), 'r')
				lines = det_new_f.readlines()
				if 'Constant voxel_num' not in lines[line_voxelnum]:
					print('ATT: line number for the voxel parameter is not correct!')
					sys.exit()
				line_list_v = lines[line_voxelnum].split()
				line_list_v[-1] = str(v)+'\n'
				lines[line_voxelnum] = ' '.join(line_list_v)
				with open('geometry/%s/%s'%(folder_name, det_new), 'w') as f:
					for line in lines:
						f.write(line)
				det_new_f.close()
		print('\n')
		
		
						
if __name__ == '__main__':
	args = PARSER.parse_args()
	
	print("--------------------")
	print("---- Start  Run ----")
	print("--------------------")
	print('\n')

	run_mkGeometries(**args.__dict__)
	
	print("--------------------")
	print("----- End  Run -----")
	print("--------------------")
