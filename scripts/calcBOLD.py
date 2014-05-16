#!/usr/bin/python2.7 

# -*- coding: utf-8 -*-

import numpy as np
import sys
import pylab as pl
	  
def BOLD(T,r):
	
	# T : total simulation time [s]
	# r : neural time series to be simulated
	
	params = {
			'taus'   : 0.65,    
			'tauf'   : 0.41,   
			'tauo'   :  0.98,    
			'alpha'  :  0.32,
			'dt' : 0.01,	 ## change it to 0.001
			'Eo' : 0.34
			}

	itaus = float(1/params['taus'])
	itauf = float(1/params['tauf'])
	itauo = float(1/params['tauo'])
	ialpha = float(1/params['alpha'])
	dt = float(params['dt'])    
	Eo = float(params['Eo'])
	
	vo     = 0.02;
	k1     = 7 * params['Eo'] 
	k2     = 2; 
	k3     = 2 * params['Eo']-0.2

	ch_int = 0

	t0 = np.array(np.arange(0,(T+params['dt']),params['dt']))
	
	n_t = len(t0)
	
	t_min = 1		#t_min = 20 #use this one!

	n_min = round(t_min / params['dt'])

	r_max = max(r)
	# initial conditions
	x0 = np.array([0 , 1, 1, 1])

	if ch_int==0:
		
		# Euler's Method
		
		t = t0		
		x = np.zeros((n_t,4))
		x[0,:] = x0
		for n in range(0,n_t-1):
			x[n+1 , 0] = x[n ,0] + dt * (r[n] - itaus * x[n,0] - itauf * (x[n,1] -float(1.0))) 
			x[n+1 , 1] = x[n, 1] + dt * x[n,0]
			x[n+1 , 2] = x[n, 2] + dt * itauo * (x[n, 1] - pow(x[n, 2] , ialpha))
			x[n+1 , 3] = x[n, 3] + dt * itauo * ( x[n, 1] * (1.-pow((1- Eo),(1./x[n,1])))/Eo - pow(x[n,2],ialpha) * x[n,3] / x[n,2])
			
		print x
		
		t_new = t[n_min -1 : -1]
		t_new = np.append(t_new , t[-1])
		
		print np.shape(t_new)


def calcBOLD(simfile):
	print "input huge time series u's and v's: ", simfile 
	# load simfile as numpy matrix
	simout = np.transpose(np.loadtxt(simfile, unpack=True))
	# extract first column of simout as time vector
	Tvec = simout[:,[0]]
	# length of time time vector
	n_Tvec = len(Tvec) 
	# dt of time vector
	dt_Tvec = Tvec[1] - Tvec[0] 
	# total number of excitators: u's 
	N = (np.shape(simout)[1] -1 ) /2
	
	# extract time series of u's from simout
	timeseries = np.zeros((n_Tvec, N))
	print "size of timeseries : ", np.shape(timeseries)
	for row in range(0,N):
		timeseries[:,[row]] = simout[:,[2*row +1]]
	# store timeseries as .dat
	np.savetxt(simfile[:-4] + '_timeseries.dat',timeseries)	
	print (timeseries)
	
	# plotting time series in a specific time interval
	t_start = 600;
	t_range = 400;
	
	fig = pl.figure(1)
	pl.plot(timeseries[t_start : (t_start + t_range) , :])
	pl.xlabel('t [ms]')
	pl.ylabel('$u_i(t)$')
	pl.savefig(simfile[:-4]+"_timeseries.eps",format="eps")
	#pl.show()

	# apply Balloon Windkessel model in fuction BOLD
	BOLD(10,timeseries[:,[0]])
		
input_name = sys.argv[1]	
calcBOLD(input_name)

























