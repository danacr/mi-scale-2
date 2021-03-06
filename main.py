#!/usr/bin/env python3

from bluepy.btle import Scanner
from dotenv import load_dotenv

import argparse
import os
import scan


def main():
    load_dotenv()
    if os.path.isfile('refresh_token'):
        f = open('refresh_token', 'r+')
        os.environ['refresh_token'] = f.read()

    parser = argparse.ArgumentParser(
        description="Get Xiaomi Mi Smart Scale 2 weight, upload to fitbit, and notify using OpsGenie")

    parser.add_argument('--verbose', '-v', action='count', default=0)
    scanner = Scanner().withDelegate(scan.ScanDelegate(parser.parse_args()))
    print("Started Get weight")

    while True:
        scanner.start()
        scanner.process(2)
        scanner.stop()


if __name__ == "__main__":
    main()
