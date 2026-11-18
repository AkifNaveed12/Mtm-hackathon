# -*- coding: utf-8 -*-
"""
HackPlan AI — Single Command CLI Runner for Mind to Machine Hackathon
Usage: python run.py [message_pack.txt]
"""
import sys
import os

def main():
    pack_file = sys.argv[1] if len(sys.argv) > 1 else 'sample_pack.txt'
    print("="*56)
    print(" HackPlan AI — Mind to Machine Hackathon CLI Runner")
    print(f" Ingesting Message Pack: {pack_file}")
    print("="*56)
    if not os.path.exists(pack_file):
        print(f"Error: File not found: {pack_file}")
        sys.exit(1)
    print("Pipeline ready for full implementation in Session 2.")
    print("Run status: Initialized.")

if __name__ == '__main__':
    main()
