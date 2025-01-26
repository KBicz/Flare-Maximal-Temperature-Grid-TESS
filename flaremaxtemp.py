#! /usr/bin/python3

import numpy as np
from sys import argv
from scipy.interpolate import griddata


def helpf():
    pyfile = argv[0]
    if "/" in pyfile:
        pyfile = pyfile.split("/")[-1]
    print(f"\n  Program {pyfile} for Linux, MacOS, and Windows written by K. Bicz, ver. of Jul. 15, 2024.")
    print("  Estimate maximal temperature of the flare using it's amplitude and effective temperature of the star.\n")
    print(f"  Usage: {pyfile} <-teff=float> <-ampl=float>")
    print()
    print("         option -teff : effective temperature of the star.")
    print("                -ampl : amplitude of the stellar flare.")
    print()
    exit()


def interp2d(temperature, teff, logampl, flarea, tflaremax):
    if flarea <= 0:
        return np.nan

    flarea = np.log10(flarea)
    target_point = np.array([[temperature, flarea]])
    points = np.column_stack((teff.ravel(), logampl.ravel()))

    # Interpolate to find the y value
    y_value = griddata(points, tflaremax.ravel(), target_point, method='linear')
    return y_value[0]


def main(teffstar, flarea):
    data = np.load("ftempgrid.npz")

    amplerrint = 10**interp2d(teffstar, data['teff'], data['famplog'], flarea, data['famplerrlog'])
    interptemp = interp2d(teffstar, data['teff'], data['famplog'], flarea, data['tflaremax'])

    err1 = interptemp - interp2d(teffstar, data['teff'], data['famplog'], flarea-amplerrint, data['tflaremax'])
    err2 = interp2d(teffstar, data['teff'], data['famplog'], flarea+amplerrint, data['tflaremax']) - interptemp
    if str(err1) == 'nan' and str(err2) != 'nan':
        err = err2
    elif str(err1) !='nan' and str(err2) == 'nan':
        err = err1
    else:
        err = (np.abs(err1)+np.abs(err2))/2

    print(f" {interptemp*12000:.0f} ± {err*12000:.0f}")
    return 0


if __name__ == "__main__":
    flarea, teffstar = 0.5375194963665797, 3338

    if len(argv) == 3:
        for arg in argv[1:]:
            if "-teff=" in arg:
                teffstar = float(arg.split("=")[1])
            elif "-ampl=" in arg:
                flarea = float(arg.split("=")[1])
            elif arg == "-h" or arg == "--help":
                helpf()

        main(teffstar, flarea)
    else:
        helpf()
