import matplotlib.pyplot as plt
import math
import numpy as np

def plotAeffvsZenith(zenith, aeff, doshow=True, dosave=False):

	plt.figure(figsize=(8,6))

	#plt.title(r'Effective Area vs. Zenith')

	plt.scatter(zenith, aeff, color='blue')
	plt.plot(zenith, aeff, color='blue', alpha=0.5, linestyle='--', lw=2, label="PixEye")

	plt.xlabel('Zenith angle ($^{\circ}$)', fontsize=16)
	plt.ylabel('Effective Area (cm$^2$)', fontsize=16)

	plt.xlim(0.0,65.0)
	plt.ylim(2.0,15.0)

	plt.legend(loc='lower center', prop={'size': 16}, numpoints=1,
               frameon=False)

	if dosave:
		plt.savefig("PixEye_Aeff_vs_zenith.png")

	if doshow: 
		plt.show()

	

def plotAeffvsEnergy(energy, aeff, doshow=True, dosave=False):

	plt.figure(figsize=(8,6))

	plt.scatter(energy, aeff, color='green')
	plt.plot(energy, aeff, color='green', alpha=0.5, linestyle='--', lw=2, label="PixEye")

	plt.xlabel('Energy (keV)', fontsize=16)
	plt.ylabel('Effective Area (cm$^2$)', fontsize=16)

	plt.xlim(500,3500)
	plt.ylim(2.0,35.0)

	plt.legend(loc='lower center', prop={'size': 16}, numpoints=1,
               frameon=False)

	if dosave:
		plt.savefig("PixEye_Aeff_vs_energy.png")

	if doshow: 
		plt.show()


def calculateAeff(ntriggers, ngenerated):

	aeff=np.zeros(len(ngenerated))

	for i in range(len(ngenerated)):
		aeff[i] = ntriggers*4*math.pi*50.0*50.0/ngenerated[i]

	return aeff