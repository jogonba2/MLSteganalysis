#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image

from math import log
from numpy import fft

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
	
