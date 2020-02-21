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
PARSER.add_argument('-lf', '--logfiles', type=str, required=True, nargs='*',
                    help='the log files saved from mkARM.py run')
PARSER.add_argument('-lab', '--labels', type=str, required=True, nargs='*',
                    help='the lables for the plot legend')
PARSER.add_argument('-t', '--title', type=str, required=True,
                    help='title of the plot')
PARSER.add_argument('-ofl', '--outflabel', type=str, required=True,
                    help='label for fig file name')
PARSER.add_argument('--show', type=bool, required=False, default=True,
                    help='if true the images will be shown')

def get_var_from_file(filename):
    f = open(filename)
    global data
    data = SourceFileLoader('data', filename).load_module()
    f.close()
    
def log_file_parsing(log_file):
	passive, thickness, energy = 0, 0, 0
	pixsize = []
	ARM_fwhm = []
	ARM_rms = []
	ARM_centroid = []
	ARM_integral = []	
	analyzed_events = []
	f = open(log_file)
	for line in f:
		if 'Analyzed Compton and pair events' in line:
			analyzed_events.append(float(line.split(' ')[-1]))
		if 'FWHM' in line:
			ARM_fwhm.append(float(line.split(' ')[-2]))
		if 'Maximum of fit (x position)' in line:
			ARM_centroid.append(float(line.split(' ')[17]))
			std = ARM_fwhm[-1]*0.6
			m = ARM_centroid[-1]
			int, interr = integrate.quad(lambda x: 1/(std*(2*np.pi)**0.5)*np.exp((x-m)**2/(-2*std**2)), 
								-ARM_fwhm[-1]/2, ARM_fwhm[-1]/2)
			ARM_integral.append(int)
		if 'PASSIVE' in line:
			passive = float(line.split(' ')[-1].replace('%', ''))
		if 'ENERGY' in line:
			energy = float(line.split(' ')[-2])
		if 'THICKNESS' in line:
			thickness = float(line.split(' ')[-2])
		if 'VOXEL SIZE' in line:
			pixsize.append(float(line.split(' ')[-2]))
			
	label_params = (passive, thickness, energy)
	value_labels = (pixsize, ARM_fwhm, ARM_integral, ARM_centroid, analyzed_events)
	return label_params, value_labels
    
def run_mkARManalysis(**kwargs):
	c = ['firebrick', 'peru', 'teal', 'darkolivegreen', 'rebeccapurple',  'orange',  '0.4', 
		 'saddlebrown', 'lightcoral' ]
	
	print('---> Centroid plot')
	plt.figure(figsize=(6,8))
	for i, log_f in enumerate(kwargs['logfiles']):
		assert(log_f.endswith('.txt'))
		lab = kwargs['labels'][i]
		offset = i*0.1+1
		lparams, vlists = log_file_parsing(log_f)
		print('---> Simulations parameters: (passive, thickness, energy)=', lparams)
		plt.errorbar(vlists[3], np.array(vlists[0])*offset, xerr=np.array(vlists[1])/2, yerr=None, 
		fmt='.', color=c[i], mew=0, alpha=0.3, linewidth=3, label=lab)
		plt.plot(vlists[3], np.array(vlists[0])*offset, '.', color='0.3')
	plt.title (kwargs['title'], size=16)
	plt.plot([0, 0],[0.001,50], '--', color='silver', linewidth=0.5)
	plt.xlabel('ARM Centroid [deg]', size=15)
	plt.ylabel('Pixel Size [mm]', size=15)
	plt.xlim(-8, 8)
	plt.ylim(1e-3, 20)
	plt.yscale('log')
	plt.legend(loc=3, fontsize=15)
	plt.savefig('figs/ARMcntr_%s.png'%kwargs['outflabel'], format='png')
	plt.savefig('figs/ARMcntr_%s.pdf'%kwargs['outflabel'], format='pdf')
	
	print('\n')
	print('---> FWHM plot')
	plt.figure(figsize=(6,5))
	for i, log_f in enumerate(kwargs['logfiles']):
		assert(log_f.endswith('.txt'))
		lab = kwargs['labels'][i]
		offset = i*0.1+1
		lparams, vlists = log_file_parsing(log_f)
		print('---> Simulations parameters: (passive, thickness, energy)=', lparams)
		plt.plot(vlists[0], vlists[1], 'o--', label=lab, color=c[i])
	plt.title (kwargs['title'], size=16)
	plt.ylabel('ARM FWHM [deg]', size=15)
	plt.xlabel('Pixel Size [mm]', size=15)
	plt.ylim(0, 8)
	plt.xscale('log')
	plt.legend(loc=2, fontsize=15)
	plt.savefig('figs/ARMfwhm_%s.png'%kwargs['outflabel'], format='png')
	plt.savefig('figs/ARMfwhm_%s.pdf'%kwargs['outflabel'], format='pdf')
	
	for i, log_f in enumerate(kwargs['logfiles']):
		lparams, vlists = log_file_parsing(log_f)
		print('Analyzed events (p %i%%)): '%lparams[0], vlists[-1])
	if kwargs['show']:
		plt.show()
	
if __name__ == '__main__':
	args = PARSER.parse_args()
	
	print("--------------------")
	print("---- Start  Run ----")
	print("--------------------")
	print('\n')
	
	run_mkARManalysis(**args.__dict__)

	print("--------------------")
	print("----- End  Run -----")
	print("--------------------")