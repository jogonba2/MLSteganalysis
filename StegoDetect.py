#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://hal.archives-ouvertes.fr/file/index/docid/754001/filename/04.pdf
from PIL import Image
from sklearn import svm
from math import sqrt,e,pi,log
from numpy import fft
import warnings
warnings.filterwarnings("ignore")

class Config:
	def __init__(self,train_hidden_path=None,train_no_hidden_path=None,test_path=None):
		self.train_hidden_path    = "./Train/Hidden/" if train_hidden_path==None else train_hidden_path
		self.train_no_hidden_path = "./Train/NoHidden/" if train_hidden_path==None else train_hidden_path
		self.test_path			  = "./Test/" if test_path==None else test_path
	
	def _get_train_hidden_path(self):    return self.train_hidden_path
	def _get_train_no_hidden_path(self): return self.train_no_hidden_path
	def _get_test_path(self):			 return self.test_path
	
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
	
	def _get_standard_desviation(self,mean,variance):
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

class ProcessImage:
	
	def __init__(self,image_path): 
		self.image     = Image.open(image_path)
		self.histogram_rgb = {"R":[],"G":[],"B":[]}
		self.histogram_dft = {"R":[],"G":[],"B":[]}
		
	def _get_image(self): 	  		 	return self.image
	def _get_histogram_rgb(self): 		return self.histogram_rgb
	def _get_histogram_dft(self):		return self.histogram_dft
	
	def _set_image(self,image_path): 			self.image     = Image.open(image_path)
	def _set_histogram_rgb(self,histogram_rgb): self.histogram_rgb = histogram_rgb
	def _set_histogram_dft(self,histogram_dft): self.histogram_dft = histogram_dft
	
	def _calc_histogram_rgb(self,rgb_image):
		for i in xrange(rgb_image.size[0]): 
			for j in xrange(rgb_image.size[1]):
				r,g,b = rgb_image.getpixel((i,j))
				self.histogram_rgb["R"].append(r); self.histogram_rgb["G"].append(g); self.histogram_rgb["B"].append(b)
			
	def _get_rgb_image(self): return self.image.convert("RGB")
	
	def _get_fourier_transformation(self): 
		self.histogram_dft["R"] = fft.fftn(self.histogram_rgb["R"])
		self.histogram_dft["G"] = fft.fftn(self.histogram_rgb["G"])
		self.histogram_dft["B"] = fft.fftn(self.histogram_rgb["B"])
		return self.histogram_dft
	
	def _get_fourier_energy(self): 
		energy_red,energy_green,energy_blue = 0,0,0
		dft_red,dft_green,dft_blue = self.histogram_dft["R"],self.histogram_dft["G"],self.histogram_dft["B"]
		for i in xrange(len(self.histogram_dft["R"])): energy_red,energy_green,energy_blue = energy_red+float(dft_red[i]),energy_green+float(dft_green[i]),energy_blue+float(dft_blue[i])
		return (energy_red,energy_green,energy_blue)
	
	def _get_histogram_dft_mean_difference(self): 
		difference_red,difference_green,difference_blue,l = 0,0,0,len(self.histogram_rgb["R"])
		rgb_red_data,rgb_green_data,rgb_blue_data = self.histogram_rgb["R"],self.histogram_rgb["G"],self.histogram_rgb["B"]
		dft_red_data,dft_green_data,dft_blue_data = self.histogram_dft["R"],self.histogram_dft["G"],self.histogram_dft["B"]
		for i in xrange(l): difference_red,difference_green,difference_blue = difference_red+(rgb_red_data[i]-dft_red_data[i]),difference_green+(rgb_green_data[i]-dft_green_data[i]),difference_blue+(rgb_blue_data[i]-dft_blue_data[i])
		return (float(difference_red)/l,float(difference_green)/l,float(difference_blue)/l)

	def _get_feature_vector(self,*args):
		feature_vector = []
		for arg in args:
			for elem in arg:  feature_vector.append(log(elem,2) if elem>0 else elem)
		return feature_vector
	
	def _feature_scaling(self,feature_vector):
		min_elem,max_elem = min(feature_vector),max(feature_vector)
		for i in xrange(len(feature_vector)): feature_vector[i] = float((feature_vector[i]-min_elem))/(max_elem-min_elem)
		return feature_vector
		
class MachineLearning:
	
	def __init__(self): pass
	def _train(self): pass
	def _test(self):  pass
	def _cross_validation(self): pass

class ParseArgs:
	
	def __init__(self): pass
	
class StegoDetect:
	
	def __init__(self):
		self.confg = Config()
		
p = ProcessImage("dados.png")

## RGB Statistics ##
p._calc_histogram_rgb(p._get_rgb_image())
ps 				= ImageStatistics(p._get_histogram_rgb())
mean_rgb 		= ps._get_mean()
variance_rgb 	= ps._get_variance(mean_rgb)
#desviation_rgb  = ps._get_standard_desviation(mean_rgb,variance_rgb)
#skewness_rgb 	= ps._get_skewness(mean_rgb,desviation_rgb)
#curtosis_rgb 	= ps._get_curtosis(mean_rgb,desviation_rgb)
## DFT Statistics ##
dft             = p._get_fourier_transformation()
ps._set_histogram(dft)
mean_dft        = ps._get_mean()
variance_dft    = ps._get_variance(mean_dft)
desviation_dft  = ps._get_standard_desviation(mean_dft,variance_dft)
skewness_dft    = ps._get_skewness(mean_dft,desviation_dft)
curtosis_dft    = ps._get_curtosis(mean_dft,desviation_dft)
dft_energy      = p._get_fourier_energy()
mean_difference = p._get_histogram_dft_mean_difference()
feature_vector  = p._get_feature_vector(mean_rgb,variance_rgb,mean_dft,variance_dft,desviation_dft,skewness_dft,curtosis_dft,dft_energy,mean_difference)
feature_vector  = p._feature_scaling(feature_vector)
print feature_vector
