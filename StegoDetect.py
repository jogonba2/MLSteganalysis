#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://hal.archives-ouvertes.fr/file/index/docid/754001/filename/04.pdf

from ProcessImage import ProcessImage
from ParseArgs import ParseArgs
from MachineLearning import MachineLearning
from ImageStatistics import ImageStatistics
from Config import Config

from os import listdir
try: from cPickle import dump,load,HIGHEST_PROTOCOL
except: from pickle import dump,load,HIGHEST_PROTOCOL
import warnings
warnings.filterwarnings("ignore")

class StegoDetect:
	
	def __init__(self,train_hidden_path=None,train_no_hidden_path=None,test_path=None,dest_data_path=None,dest_classes_path=None,process=None):
		self._config = Config(train_hidden_path,train_no_hidden_path,test_path,dest_data_path,dest_classes_path,process)
		self._image_processor  = None
		self._image_statistics = None
		self._classificator    = MachineLearning()
		
	def _make_process(self):
		if self._config._get_process()==0: self.__preprocess_corpus()
		else:							   self.__detect_message()
		
	def __preprocess_corpus(self):
		f_data    = open(self._config._get_dest_data_path(),"w")
		f_classes = open(self._config._get_dest_classes_path(),"w")
		for fd in listdir(self._config._get_train_hidden_path()): 
			print fd
			dump(self.__preprocess_file(self._config._get_train_hidden_path()+fd),f_data)
			dump(1,f_classes)
		for fd in listdir(self._config._get_train_no_hidden_path()): 
			print fd
			dump(self.__preprocess_file(self._config._get_train_no_hidden_path()+fd),f_data)
			dump(0,f_classes)
		f_data.close()
		f_classes.close()
		
	def __preprocess_file(self,fd):
		if self._image_processor  == None: self._image_processor = ProcessImage(fd)
		else:						       self._image_processor._set_image(fd)
		self._image_processor._calc_histogram_rgb(self._image_processor._get_rgb_image())
		histogram_rgb = self._image_processor._get_histogram_rgb()
		if self._image_statistics == None: self._image_statistics = ImageStatistics(histogram_rgb)
		else:							   self._image_statistics._set_histogram(histogram_rgb)
		mean_rgb 	  = self._image_statistics._get_mean()
		variance_rgb  = self._image_statistics._get_variance(mean_rgb)
		dft_histogram = self._image_processor._get_fourier_transformation()
		self._image_statistics._set_histogram(dft_histogram)
		mean_dft        = self._image_statistics._get_mean()
		variance_dft    = self._image_statistics._get_variance(mean_dft)
		desviation_dft  = self._image_statistics._get_standard_desviation(variance_dft)
		skewness_dft	= self._image_statistics._get_skewness(mean_dft,desviation_dft)
		curtosis_dft    = self._image_statistics._get_curtosis(mean_dft,desviation_dft)
		energy_dft      = self._image_processor._get_fourier_energy()
		mean_difference = self._image_processor._get_histogram_dft_mean_difference()
		feature_vector  = self._image_processor._get_feature_vector(mean_rgb,variance_rgb,mean_dft,variance_dft,skewness_dft,curtosis_dft,energy_dft,mean_difference)
		feature_vector  = self._image_processor._feature_scaling(feature_vector)
		return feature_vector
	
	def __unpickle(self,fd):
		res = []
		while 1:
			try: 
				res.append(load(fd))
			except EOFError: break
		return res
		
	def __detect_message(self): 
		f_data     = open(self._config._get_dest_data_path(),"rb")
		f_classes  = open(self._config._get_dest_classes_path(),"rb")
		features   = self.__unpickle(f_data)
		classes    = self.__unpickle(f_classes)
		f_data.close()
		f_classes.close()
		## Train ml #
		self._classificator._train(features,classes)
		features = []
		for fd in listdir(self._config._get_test_path()):
			res = self._classificator._test(self.__preprocess_file(self._config._get_test_path()+fd))
			if res==[1]: print "File",fd,"has a hidden message"
			else:        print "File",fd,"has not got any hidden message"
			
if __name__ == "__main__": s = StegoDetect(None,None,None,None,None,1)._make_process()
