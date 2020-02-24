import os
import re
import numpy as np



def RevFileParser_general(file):
	'''Parses the main infos of the simulations
	'''
	f = open(file)
	data_frame_general = {}
	keys = ['Type', 
			'Version', 
			'Geometry' ,
			'Date', 
			'MEGAlib']
	for line in f:
	    for k in keys:
	        if k in line:
	            if len(line.split()[1:]) == 1:
	            	if k is 'Geometry':
	            	    data_frame_general[k] = [os.path.basename(line.split()[1])]\
	            	                                         +['','','','','','','']
	            	else:
	                    data_frame_general[k] = line.split()[1:]+['','','','','','','']
	            elif len(line.split()[1:]) == 2:
	                data_frame_general[k] = line.split()[1:]+['','','','','','']
	            elif len(line.split()[1:]) == 3:
	                data_frame_general[k] = line.split()[1:]+['','','','','']
	            elif len(line.split()[1:]) == 4:
	                data_frame_general[k] = line.split()[1:]+['','','','']
	            else:
	            	data_frame_general[k] = line.split()[1:]
	f.close()
	return data_frame_general

def RevFileParser_events(file):
	'''Parses the events parameters
	'''

	### --- Printing the reconstruction information --- ###
	f, f1 = open(file), open(file)
	lines = f.readlines()
	counter = 0
	for line in lines:
		if 'Trigger statistics:' in line:
			for i in range (len(lines)-(counter+5)):
				print(lines[i+counter])
		counter += 1

	f.close()

	#### --- Storing the unique parameters (that appear only once per each event) --- ####
	hit_lines = f1.readlines()
	data_frame_events = {}
	ET, ID, TI, PE, PP, PW = [], [], [], [], [], []
	unique_params = ['ET', 'ID', 'TI', 'PE', 'PP', 'PW']
	count = 0
	for line in hit_lines:
		if 'SE' in hit_lines[count] and 'PP' in hit_lines[count+5]:
			entry = hit_lines[count+1].split()
			ET.append((str(entry[1])))
			ID.append(float(hit_lines[count+2].split()[1]))
			TI.append(float(hit_lines[count+3].split()[1]))
			PE.append(float(hit_lines[count+4].split()[1]))
			value = hit_lines[count+5].split()
			PP.append([float(value[1]), float(value[2]), float(value[3])])
			PW.append(float(hit_lines[count+6].split()[1]))
		count += 1
    
	for k in range(len(PP)):
		data_frame_events[k] = {'ET':ET[k], 'ID':ID[k], 'TI':TI[k], 'PE':PE[k], 'PP':PP[k]}

	f1.close()

	return data_frame_events




# if __name__ == '__main__':

	'''Test module
	'''
	#simf = '../CosimaSim/FarFieldPointSource_0.500MeV_Cos1.0_SingleBar.inc1.id1.sim'
	
	#sim_info = SimFileParser_general(simf)
	#sim_events, ht_data = SimFileParser_events(simf)