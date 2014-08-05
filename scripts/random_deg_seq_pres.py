#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# Creating a random network by different methhods

import networkx as nx
import numpy as np
from math import factorial 
import math
import random
import matplotlib.pyplot as pl	
import random as rnd
import sys  
import glob
import os


def load_matrix(file):
	A = np.loadtxt(file, unpack=True)
	AT = np.transpose(A)
	# check the symmetry				
	if A.shape[0] != A.shape[1] or not (A == AT).all():
		print "error: loaded matrix is not symmetric"
		raise ValueError
	return AT

# create adjacency matrix, ones and zeros according to r
def threshold_matrix(A, r):
	B = np.zeros(A.shape)
	for row in range(A.shape[0]):
		for col in range(A.shape[1]):
			if row != col and A[row, col] >= r:
				B[row, col] = 1
	return B

def plot_graph(B):
	G   = nx.from_numpy_matrix(B)
	pos = nx.shell_layout(G)
	nx.draw(G, pos)
	pl.show()
	
def degre_pres(R , ITER):

   
	#R = randmio_und_connected(W,ITER);

	#[R eff] = randmio_und_connected(W, ITER);

	#Input:  W,      undirected (binary/weighted) connection matrix
	       #ITER,   rewiring parameter
	#Output:     R,      randomized network
				#eff,    number of actual rewirings carried out
	
	
	n_col   = np.shape(R)[1]		# number of columns in array
	new_R   = np.triu(R)			# upper triangle of array	
	(j , i) = new_R.nonzero()		# (row,col) index of non-zero elem.
	
	i.setflags(write=True)
	j.setflags(write=True)
	
	K       = len(i)				# total number of non-zero elements
	ITER    = K*ITER				# total iteration number 
	
	maxAttempts = int(K/(n_col-1))  # max attempts per iteration
	
	eff     = 0  
	for iter in range(1 , ITER+1 ):
		att = 0
		while att<=maxAttempts:
			rewire = 1
			while 1:
				e1 = int(math.floor(K*random.random()))
				e2 = int(math.floor(K*random.random()))
				while e1==e2:
					e2 = int(math.floor(K*random.random()))
				
				a = i[e1]          # chose a col number from i
				b = j[e1]		   # chose a row number from j		
				c = i[e2]		   # chose another col number from i	
				d = j[e2]		   # chose another row number from j		
				
				
				if ( ( (a!=c) & (a!=d) ) & ( (b!=c) & (b!=d)) ) :
					break          # make sure that a,b,c,d differ
			
			


			# flipping edge c-d with 50% probability	
			if random.random() > 0.5 :
				i[e2]  = d
				j[e2]  = c
				c      = i[e2]
				d      = j[e2]		
			
			#if  int(not(bool( R[a,d] or R[b,d] ))):
			print  int(not(bool( R[a,d] or R[b,d] )))
			
			att = att + 1
			
	
	
	#print maxAttempts

if __name__ == '__main__':
	usage = 'Usage: %s method correlation_matrix [threshold]' % sys.argv[0]
	try:
		input_name = sys.argv[1]
	except:
		print usage
		sys.exit(1)

data_matrix = load_matrix(input_name)	
#adja_matrix = threshold_matrix(data_matrix, r=0)
#plot_graph(data_matrix)

degre_pres(data_matrix , ITER = 10)
