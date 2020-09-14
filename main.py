#!~/miniconda3/envs/ih/bin/python
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Show book summary data")
    parser.add_argument('-y', dest='year',
                        default=2015,
                        type=onlyYears(minYear,maxYear),
                        help="Año seleccionado")
                        
    args = parser.parse_args()

if __name__ == "__main__":
    main()