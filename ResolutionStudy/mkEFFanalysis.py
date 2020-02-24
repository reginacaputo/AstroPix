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
from importlib.machinery import SourceFileLoader
import scipy.integrate as integrate
import scipy.signal as signal
import matplotlib.pyplot as plt


__description__ = 'Creates the AstroPix geometry configurations'

formatter = argparse.ArgumentDefaultsHelpFormatter
PARSER = argparse.ArgumentParser(description=__description__, formatter_class=formatter)
PARSER.add_argument('-c', '--config', type=str, required=True,
                    help='the input configuration file')
PARSER.add_argument('--show', type=bool, required=False, default=True,
                    help='if true the images will be shown')
PARSER.add_argument('-ofl', '--outflabel', type=str, required=True,
                    help='label for fig file name')

def get_var_from_file(filename):
    f = open(filename)
    global data
    data = SourceFileLoader('data', filename).load_module()
    f.close()
    
def run_mkEFFanalysis(**kwargs):
	assert(kwargs['config'].endswith('.py'))
	get_var_from_file(kwargs['config'])
	
	passive = data.PASSIVE
	thickness = data.THICKNESS
	voxelsize = data.VOXELSIZE
	energy = data.ENERGY
	
	tot_listoflists, eff_listoflists, analyzed_events_listoflists = [], [], []
	for i, p in enumerate(passive):
		print('PASSIVE %i: %i%%' %(i, p*100))
		tot_evts_list, eff_list, analyzed_events_list = [], [], []
		for j, t in enumerate(thickness):	
			print('THICKNESS %i: %.2f cm' %(j, t/10000))
			for n, e in enumerate(energy):
				print('ENERGY: %i keV'%e)
				outlog_m = open('simres/mimrec-log_%.2f_%i_en%i.txt' %(p, t, e), 'r')
				for line in outlog_m:
					if 'Analyzed Compton and pair events' in line:
						analyzed_events = float(line.split(' ')[-1])
						print('Analyzed evts=', analyzed_events)
						analyzed_events_list.append(analyzed_events)
				for k, v in enumerate(voxelsize): 
					print('VOXEL SIZE %i: %.2f mm' %(k, v))
					outlog_r = open('simres/revan-log_%.2f_%i_%.2f_en%i.txt' %(p, t, v, e), 'r')
					for line in outlog_r:
						if 'passed event selections' in line:
							eff = float(line.split(' ')[-1].replace('%)', ''))
							print('EFF=', eff)
							eff_list.append(eff)
						if 'Number of events ...' in line:
							tot = float(line.split(' ')[-2])
							print('Tot evts=', tot)
							tot_evts_list.append(tot)	
		tot_listoflists.append(tot_evts_list)
		eff_listoflists.append(eff_list)
		analyzed_events_listoflists.append(analyzed_events_list)
		print('\n')
		
	plt.figure(figsize=(6,5))
	plt.title('Effective area and passive material')
	c = ['firebrick', 'peru', 'teal', 'darkolivegreen', 'rebeccapurple',  'orange',  '0.4', 'saddlebrown', 'lightcoral' ]
	for i, l in enumerate(tot_listoflists):
		l = np.array(l)
		ana_evts = np.array(analyzed_events_listoflists[i])[:]
		plt.plot(voxelsize, ana_evts/l, 'o--', label='passive %i%%' %(passive[i]*100), 
				color=c[i])
	plt.xlabel('Pixel Size [mm]', size=15)
	plt.ylabel('Selected events / Tot Events', size=15)
	plt.xscale('log')
	plt.ylim(-0.1, 0.5)
	plt.xlim(7e-3, 15)
	plt.legend(loc=4, fontsize=12)
	plt.savefig('figs/AEFF_%s.png'%kwargs['outflabel'], format='png')
	plt.savefig('figs/AEFF_%s.pdf'%kwargs['outflabel'], format='pdf')
	
	plt.figure(figsize=(6,5))
	plt.title('Effective area relative to %i%% passive material'%(passive[-1]*100))
	for i, l in enumerate(tot_listoflists[:-1]):
		l = np.array(l)
		ana_evts = np.array(analyzed_events_listoflists[i])
		ana_evts0 = np.array(analyzed_events_listoflists[-1])
		eff0 = (ana_evts0/tot_listoflists[-1])
		plt.plot(voxelsize, (eff0-ana_evts/l)/eff0*100, 'o--', label='passive %i%%' %(passive[i]*100), 
				color=c[i])
		plt.plot([0.01, 10.], [0, 0], '--', color='silver', linewidth=0.5)
	plt.xlabel('Pixel Size [mm]', size=15)
	plt.ylabel('(A$_{eff, 0}$ - A$_{eff}$)/A$_{eff,0}$ [%]', size=15)
	plt.xscale('log')
	plt.legend(loc=1, fontsize=12)
	plt.savefig('figs/AEFFrel_%s.png'%kwargs['outflabel'], format='png')
	plt.savefig('figs/AEFFrel_%s.pdf'%kwargs['outflabel'], format='pdf')
	
	if kwargs['show']:
		plt.show()
		
if __name__ == '__main__':
	args = PARSER.parse_args()
	
	print("--------------------")
	print("---- Start  Run ----")
	print("--------------------")
	print('\n')
	
	run_mkEFFanalysis(**args.__dict__)

	print("--------------------")
	print("----- End  Run -----")
	print("--------------------")