#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn import svm

class MachineLearning:
	
	def __init__(self,type=None,kernel=None,types=None): 
		if   type==None: self._classificator = svm.SVC(kernel="linear")
		# ... #	
	def _train(self,features,classes): 	self._classificator.fit(features,classes)
	def _test(self,features):  		  	return self._classificator.predict(features)
