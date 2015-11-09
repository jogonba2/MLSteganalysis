#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import sqrt,e,pi

class ImageStatistics:
	
	def __init__(self,histogram):
		self.histogram = histogram
	
	def _get_histogram(self): 			return self.histogram
	def _set_histogram(self,histogram): self.histogram = histogram
	
	def _get_mean(self):
		mean_red,mean_green,mean_blue,l = 0,0,0,len(self.histogram["R"])
		red_data,green_data,blue_data = self.histogram["R"],self.histogram["G"],self.histogram["B"]
		for i in xrange(l): mean_red,mean_green,mean_blue = mean_red+red_data[i],mean_green+green_data[i],mean_blue+blue_data[i]
		return (float(mean_red)/l,float(mean_green)/l,float(mean_blue)/l)
	
	def _get_standard_desviation(self,variance):
		(variance_red,variance_green,variance_blue) = (variance[0],variance[1],variance[2])
		return (sqrt(variance_red),sqrt(variance_green),sqrt(variance_blue))
		
	def _get_variance(self,mean):
		variance_red,variance_green,variance_blue,l = 0,0,0,len(self.histogram["R"])
		mean_red,mean_green,mean_blue = mean[0],mean[1],mean[2]
		red_data,green_data,blue_data = self.histogram["R"],self.histogram["G"],self.histogram["B"]
		for i in xrange(l): variance_red,variance_green,variance_blue = variance_red+(red_data[i]-mean_red)**2,variance_green+(green_data[i]-mean_green)**2,variance_blue+(blue_data[i]-mean_blue)**2
		return (float(variance_red)/l,float(variance_green)/l,float(variance_blue)/l)
	
	def _get_curtosis(self,mean,desviation):
		curtosis_red,curtosis_green,curtosis_blue,l = 0,0,0,len(self.histogram["R"])
		red_data,green_data,blue_data = self.histogram["R"],self.histogram["G"],self.histogram["B"]
		mean_red,mean_green,mean_blue = mean[0],mean[1],mean[2]
		desviation_red,desviation_green,desviation_blue = desviation[0],desviation[1],desviation[2]
		for i in xrange(l): curtosis_red,curtosis_green,curtosis_blue = curtosis_red+(red_data[i]-mean_red)**4,curtosis_green+(green_data[i]-mean_green)**4,curtosis_blue+(blue_data[i]-mean_blue)**4
		return ((float(curtosis_red)/l)/desviation_red**4,(float(curtosis_green)/l)/desviation_green**4,(float(curtosis_blue)/l)/desviation_blue**4)
		
	def _get_skewness(self,mean,desviation): 
		skewness_red,skewness_green,skewness_blue,l = 0,0,0,len(self.histogram["R"])
		red_data,green_data,blue_data = self.histogram["R"],self.histogram["G"],self.histogram["B"]
		mean_red,mean_green,mean_blue = mean[0],mean[1],mean[2]
		desviation_red,desviation_green,desviation_blue = desviation[0],desviation[1],desviation[2]
		for i in xrange(l): skewness_red,skewness_green,skewness_blue = skewness_red+(red_data[i]-mean_red)**3,skewness_green+(green_data[i]-mean_green)**3,skewness_blue+(blue_data[i]-mean_blue)**3
		return ((float(skewness_red)/l)/desviation_red**3,(float(skewness_green)/l)/desviation_green**3,(float(skewness_blue)/l)/desviation_blue**3)
