#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-09 11:05:19
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$
import BitVector  
import os  
import sys  
  
class SimpleHash(): 
	def __init__(self, cap, seed):  
		self.cap = cap  
		self.seed = seed  
      
	def hash(self, value):  
		ret = 0  
		for i in range(len(value)):  
			ret += self.seed*ret + ord(value[i])  
		return (self.cap-1) & ret      
  
class BloomFilter():  
      
	def __init__(self, BIT_SIZE=1<<25):  
		self.BIT_SIZE = 1 << 25  
		self.seeds = [5, 7, 11, 13, 31, 37, 61]  
		self.bitset = BitVector.BitVector(size=self.BIT_SIZE)  
		self.hashFunc = []  
          
		for i in range(len(self.seeds)):  
			self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))  
          
	def insert(self, value):  
		for f in self.hashFunc:  
			loc = f.hash(value)  
			self.bitset[loc] = 1  
	def isContaions(self, value):  
		if value == None:  
			return False  
		ret = True  
		for f in self.hashFunc:  
			loc = f.hash(value)  
			ret = ret & self.bitset[loc]  
		return ret  

	def getHash(self):
		res = list()
		for f in self.hashFunc:
			res.append(self.bitset[loc])
		return res
  
# def main():  
# 	print('s')
# 	fd = open("QQ.txt",'r')  
# 	bloomfilter = BloomFilter()  
# 	while True:  
# 		#url = raw_input()  
# 		url = fd.readline()  
# 		if (url > '') - (url < '') == 0: #if url is equal exit break  
# 			break  
# 		if bloomfilter.isContaions(url) == False:  
# 			bloomfilter.insert(url)  
# 		else:  
# 			print ('url :%s has exist' % url  )

# 	print(bloomfilter.getHash())
              
# main()  
