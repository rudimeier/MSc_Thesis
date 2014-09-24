#!/usr/bin/python2.7 
# -*- coding: utf-8 -*-

""" 
	visualizing the local dynamics of FitzHugh Nagumo model with 
	different parameters chosen from literature. 
	
	Literature ; 
	[PAN12] = D.Rosin, P.Hövel, E.Schöll, "Synchronization of 
	coupled neuronal oscillators with heterogenous delays", 2012
	
	[GHOS08a] = A.Ghosh, Y.Rho, A.R.McIntosh, R.Kötter, V.K.Jirsa,
	"Cortical Network Dynamics with time delays reveals functional
	connectivity in the resting brain", 2008
	
	[VUK13] = V.Vuksanovic, P.Hövel, "Large-scale neuronal network
	model for functional networks of the human cortex", 2013
	
	output : plotting activator(x) and inhibitor(y) over time(t)
	and in state space
"""

from __future__ import division
import numpy as np
import sys
import pylab as pl
from pydelay import dde23
from scipy.optimize import fsolve
from pylab import *

### [PAN12] local dynamics ################
#eqns = {r'x' : '(x - pow(x,3)/3 -y )/eps',
		#r'y' : 'x+a'}

#params = { 'eps' : 0.01,
		   #'a'   : 1.3}
	 
## nullclines of [PAN12]
#def nullcl_01(X):
  #return -(pow(X,3)/3 - X)
  ##make x minus
  
#def nullcl_02(X):
  #return (-params['a']  ) 

## intersection of nullclines [PAN12] : 
#X_int = -params['a']
#Y_int = nullcl_01(-params['a'])

###########################################
	 
### [GHOS08a] local dynamics	##
#eqns   = {r'x' : '(y + gamma*x - pow(x,3)/3.0) * TAU ',
	      #r'y' : '-(x - alpha + b*y  ) / TAU' }

#params = {'gamma' : 1.0, #0.9
		  #'alpha' : 1.05, #1.9
		  #'TAU'   : 1.25,
		  #'b'     : 0.2 }

## [VUK13] local dynamics ##
eqns   = {r'x' : '(y + gamma*x - pow(x,3)/3.0) * TAU ',
	      r'y' : '-(x - alpha + b*y  ) / TAU' }

params = {'gamma' : 1.0, #0.9
		  'alpha' : 0.85, #1.9
		  'TAU'   : 1.25,
		  'b'     : 0.2 }

# nullclines of [GHO08a] and [VUK13]
def nullcl_01(X):
  return -(pow(X,3)/3 - params['gamma']*X)
  #make x minus
  
def nullcl_02(X):
  return (params['alpha'] - X ) / params['b']

# calculate the intersection of nullclines [GHO08a], [VUK13]
def intersection(X):
 return nullcl_01(X) - nullcl_02(X)

# state a reasonable root for fsolve!!!
X0    = 0
X_int = fsolve(intersection,X0)
Y_int = nullcl_01(X_int)

###################################################

x_limit = 2.5
x_range = np.linspace(-x_limit,x_limit,500)

dde = dde23(eqns=eqns,params=params)

tfinal =100

dde.set_sim_params(tfinal)

dde.hist_from_funcs( {'x': lambda t : -0.05, 'y': lambda t: -0.75 })

dde.run()

# user defined sampling rate
dt = float(sys.argv[1])
# sampled solution
sol_sample = dde.sample(0,tfinal,dt)

t = sol_sample['t']
x = sol_sample['x']
y = sol_sample['y']

# adaptive step size method solution
sol_adap = dde.sol

print "FitzHugh Nagumo Local Dynamics"
print "equations: ", dde.eqns
print "parameters: ", dde.params
print "simulation time : ", tfinal
print "Sampling time interval : " , dt
print "intersection of nullclines (x_0, y_0): ", X_int, Y_int

fig = pl.figure(num=None, figsize=(13.5, 6), dpi=100, facecolor='w', edgecolor='k')

### [PAN12]
#fig.suptitle('FHN - Local Dynamics :  '+ 'a=' +str(params['a']) +
	      #r'  $\epsilon$ = ' +str(params['eps']) , 
	      #fontsize=14, fontweight='bold')

## [GHO08a], [VUK13]
fig.suptitle('FHN - Local Dynamics :  '+r'$\alpha$ = ' +str(params['alpha'])+
	      r'  $  \gamma$ = '+str(params['gamma']) + ' $   b$ = '+ 
	      str(params['b']) + r'  $\tau$ = '+str(params['TAU']),
	      fontsize=14, fontweight='bold')

pl.subplot(121, xlabel='t', ylabel='x(t) , y(t)')
pl.plot(t, x, 'r', label='$x(t)$')
pl.plot(t, y, 'b', label='$y(t)$')
#pl.plot(sol_adap['t'],sol_adap['x'],'.r',linewidth=0.2)
#pl.plot(sol_adap['t'],sol_adap['y'],'.b',linewidth=0.2)
pl.axis([0, tfinal, -3, 3])
lg = legend()
lg.draw_frame(False)

pl.subplot(122, xlabel='x', ylabel='y')
pl.plot(x, y, 'r', label='$x,y$')
pl.plot(x[0], y[0], '.r')
#pl.plot(x_, y_ , 'b',label='$x_{nullcline}$')
#pl.plot(xx,yy,'k',label='$y_{nullcline}$')
#pl.plot(-params['a'],(-params['a']+pow(params['a'],3)/3),'ok')
#pl.plot(sol_adap['x'],sol_adap['y'],'.r',linewidth=0.2)
pl.plot(x_range,nullcl_01(x_range),'b', label='$x_{nullcline}$')

##[GHO08a] and [VUK13] 
pl.plot(x_range,nullcl_02(x_range),'k',label='$y_{nullcline}$')

### [PAN12]
#pl.plot(nullcl_02(x_range)* np.ones(len(x_range)), x_range,'k',label='$y_{nullcline}$')

pl.plot(X_int,Y_int, 'ok', linewidth=3)
pl.axis([-2.3, 2.3, -2.5, 2.5])
lg = legend()
lg.draw_frame(False)
#pl.savefig("VUK13_local_dynamics.eps",format="eps")
#pl.savefig("GHO08_local_dynamics.eps",format="eps")
#pl.savefig("PAN12_local_dynamics.eps",format="eps")
pl.show()