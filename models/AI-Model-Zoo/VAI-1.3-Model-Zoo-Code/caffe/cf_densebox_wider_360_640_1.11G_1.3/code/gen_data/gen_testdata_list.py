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
    parser = ArgumentParser(description="generate FDDB list script")
    parser.add_argument('--oriListPath', type=str, 
            default='../../data/test/FDDB-folds/',
            help='The original Anno list path')
    parser.add_argument('--FDDB_anno', type=str,
            default='../../data/test/FDDB_annotations.txt',
            help='The groundtruth list file')
    parser.add_argument('--FDDB_list', type=str,
            default='../../data/test/FDDB_list.txt',
            help='Ths FDDB image list file')
    return parser.parse_args()

args = parse_args()

def gen_dataset_list(args):
    FDDB_anno = open(args.FDDB_anno,'w')
    FDDB_list = open(args.FDDB_list,'w')
    for listfile in os.listdir(args.oriListPath):
        if "ellipseList" in listfile:
            filepath = os.path.join(args.oriListPath, listfile)
            currentFile = open(filepath)
            lines = currentFile.readlines()
            for ln in lines:
                FDDB_anno.write('%s\n'%(ln.strip()))
                if 'img' in ln.strip():
                    FDDB_list.write('%s\n'%(ln.strip()))

    FDDB_anno.close()
    FDDB_list.close()
            
if __name__ == "__main__":
   gen_dataset_list(args)
