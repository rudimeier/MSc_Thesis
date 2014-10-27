#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
from math import factorial 
import matplotlib.pyplot as pl	
from matplotlib.pyplot import FormatStrFormatter
import random as rnd
import sys  
import glob
import os
import scipy.stats as sistat
import collections

# check the loaded matrix if it is symmetric
def load_matrix(file):
	A  = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	# check the symmetry				
	if A.shape[0] != A.shape[1] or not (A == AT).all():
		print "error: loaded matrix is not symmetric"
		raise ValueError
	return AT

def corr_histo(corr_matrix, simfile):
	# merge 2D corr_matrix into 1D numpy array by flatten
	corr_flat = np.ndarray.flatten(corr_matrix) 
	corr_max  = 1.0
	corr_min  = -1.0
	bin_nu    = 20
	# a normalized histogram is obtained
	hist = pl.hist(corr_flat, bins=bin_nu, range=[corr_min, corr_max], normed =True, histtype='bar')
	# type(hist) = <type 'tuple'> and len(hist) = 3
	# y_axis : hist[0] , normalized hist values
	# x_axis : hist[1] , start points of bins 
	return hist

# intersection method to compare two histograms
def intersec_hists(HA, HB):
	y_axis    = 0
	HA_norm = HA[y_axis]
	HB_norm = HB[y_axis]
	minsum  = 0
	for i in range(0, len(HA_norm)) :
		minsum = minsum + min(HA_norm[i], HB_norm[i])
	# normalize minsum 
	minsum  = float(minsum) /  sum(HB_norm) 
	return minsum

def chi2_distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
	for (a, b) in zip(histA, histB)])
 
	# return the chi-squared distance
	return d
		
if __name__ == '__main__':
	usage = 'Usage: %s method correlation_matrix [threshold]' % sys.argv[0]
	try:
		input_empiri = sys.argv[1]
		input_simuli = sys.argv[2]
	except:
		print usage
		sys.exit(1)
		
# fMRI-BOLD input matrix load , this is a correlation matrix already
mtx_empiri = load_matrix(input_empiri)
HistA      = corr_histo(mtx_empiri, input_empiri)

# loading correl. mtx. of fhn time series (output of correlation_fhn.py)
name       = 'A_aal_0_ADJ_thr_0.54_sigma=0.2_D=0.05_v=90.0_tmax=45000_FHN_corr.dat'

thr_array = np.array([54, 56, 58, 60, 62, 63, 64, 65, 66])					                        

vel_array = np.array([30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150])

sig_array = np.array([0.1, 0.3, 0.5, 0.9])

R_thr =  {}


for THR in thr_array :
	R_temp = []
	
	for VEL in vel_array :
		local_path   = '../data/jobs_corr/'
 		input_simuli = name[0:18] + str(THR) + name[20:40] + str(VEL) + name[42:]		
		
		try:
			mtx_simuli = load_matrix(local_path + input_simuli)
			HistB      = corr_histo(mtx_simuli, input_simuli)
		except :
			R_vel      = np.nan
		else :
			R_vel      = intersec_hists(HistA, HistB)
			
		R_temp     = np.append(R_temp, R_vel)
	R_thr[THR] 	   = np.array(R_temp)	
	
Ordered_R   = collections.OrderedDict(sorted(R_thr.items()))	
#print "Ordered dict"
#print Ordered_R

datam 		= np.array(Ordered_R.values())

#print "check its numpy array version"
#print datam

# PLOTTING BEGINS ! 
fig, ax = pl.subplots()
cmap    = pl.cm.jet
pl.imshow(np.transpose(datam), interpolation='nearest', cmap='jet', vmin=0.0, vmax=0.48, aspect='auto')
cbar = pl.colorbar()

## PLOT PA OVER SIGMA
#a = thr_array
#b = sig_array
## title for fhn....
#pl.title('A_aal_0...' + ' , FHN , ' + '  v = 7 [m/s] '+' T = 450 [s]',
		 #fontsize=20)
## title for bold...
##pl.title('A_aal_0...' + ' , BOLD , ' + '  v = 7 [m/s]', fontsize=20)
#pl.ylabel('$\sigma$ ', fontsize=20)

# PLOT PA OVER VELOCITY
a = thr_array
b = vel_array
# title for fhn....
#pl.title('acp_w_0_...' + ' , FHN , ' + '$\sigma$ = 0.5 '+' T = 450 [s]',
#		 fontsize=20)
# title for bold...
#pl.title('A_aal_0...' + ' , BOLD , ' + '$\sigma$ = 0.2', fontsize=20)
pl.ylabel('v [m/s]', fontsize=20)

pl.setp(ax , xticks=np.arange(0,len(a),1), xticklabels = a)
pl.setp(ax , yticks=np.arange(0,len(b),1), yticklabels = b)
pl.xlabel('thr', fontsize = 20)
for t in cbar.ax.get_yticklabels():
	t.set_fontsize(15)
pl.xticks(fontsize = 15)
pl.yticks(fontsize = 15)
pl.show()		

#mtx_empiri			= 		load_matrix(input_empiri)		
#mtx_simuli			= 		load_matrix(input_simuli)
#pl.figure(1)
#HistA = corr_histo(mtx_empiri, input_empiri)
#pl.figure(2)
#HistB = corr_histo(mtx_simuli, input_simuli)
#intersec_hists(HistA, HistB)
#chi2_distance(HistA, HistB, eps = 1e-10)