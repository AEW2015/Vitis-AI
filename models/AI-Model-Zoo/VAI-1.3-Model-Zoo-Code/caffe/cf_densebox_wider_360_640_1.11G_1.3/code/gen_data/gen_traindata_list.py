# Copyright 2019 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# PART OF THIS FILE AT ALL TIMES.

#coding=utf-8
import os
import sys
import numpy as np
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="generate widerface list script")
    parser.add_argument('--inputAnnoFile', type=str,
            default='wider_face_train_bbx_gt.txt',
            help='The original groundtruth list file ')
    parser.add_argument('--outputAnnoFile', type=str,
            default='wider_list.txt',
            help='The modified groundtruth list file')
    return parser.parse_args()

args = parse_args()

def gen_dataset_list(args):
    oldGT = open(args.inputAnnoFile)
    oldGTs = oldGT.readlines()
    newGT = open(args.outputAnnoFile, 'w')
    for ln in oldGTs:
        strs = ln.strip().split(' ')
        if len(strs) is not 1:
            newLabel = strs[0:4]
            newGT.write('%s %s %d %d\n'%(newLabel[0], newLabel[1], 
                    int(newLabel[2])+int(newLabel[0]), int(newLabel[3])+int(newLabel[1])))
        elif 'jpg' in ln.strip(): 
            newGT.write('%s\n'%(ln.strip()))
        elif int(strs[0])==0: 
            newGT.write('%d\n'%(1))
        else:
            newGT.write('%s\n'%(ln.strip()))            
    newGT.close()

            
if __name__ == "__main__":
   gen_dataset_list(args)
