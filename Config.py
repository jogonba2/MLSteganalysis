#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config:
	def __init__(self,train_hidden_path=None,train_no_hidden_path=None,test_path=None,dest_data_path=None,dest_classes_path=None,process=None):
		self.train_hidden_path    = "./Train/Hidden/" if train_hidden_path==None else train_hidden_path
		self.train_no_hidden_path = "./Train/NoHidden/" if train_hidden_path==None else train_hidden_path
		self.test_path			  = "./Test/" if test_path==None else test_path
		self.dest_data_path       = "./Train/train.bin" if dest_data_path==None else dest_data_path
		self.dest_classes_path    = "./Train/classes.bin" if dest_classes_path==None else dest_classes_path
		# Process -> 0 (preprocess images, saving them in binary representation) 1 (charge binary representation and clasification of test samples) #
		self.process			  = 0 if process==None else process

	def _get_train_hidden_path(self):    return self.train_hidden_path
	def _get_train_no_hidden_path(self): return self.train_no_hidden_path
	def _get_test_path(self):			 return self.test_path
	def _get_dest_data_path(self):		 return self.dest_data_path
	def _get_dest_classes_path(self):	 return self.dest_classes_path
	def _get_process(self):				 return self.process
	
