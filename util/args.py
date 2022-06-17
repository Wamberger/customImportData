
import argparse


def getArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument('importFile')

    args = parser.parse_args()

    return args