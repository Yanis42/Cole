#!/usr/bin/env python3

from os import name as osName
from sys import executable
from subprocess import run, PIPE


def getInstalledModules():
    """Returns a string containing installed pip modules"""
    return run([executable, "-m", "pip", "freeze"], stdout=PIPE).stdout.decode("UTF-8")


def getExcludedModules():
    """Returns a list of useless modules to exclude when building"""
    modules = getInstalledModules().split("\n")
    excludeList = []
    for module in modules:
        if not "pyqt6" in module.lower() and (module != ""):
            module = module.replace("\r", "").split("==")[0]
            excludeList.append(f"--exclude-module {module}")
    return excludeList


def main():
    # Probably not needed, excludes modules not needed by Cole
    # just in case they get included, which increase the size of the executable
    excludedModules = " ".join(getExcludedModules())

    # Windows seems to use a capitalized name for the PyInstaller module
    try:
        import pyinstaller

        pyInstaller = "pyinstaller"
    except ModuleNotFoundError:
        pyInstaller = "PyInstaller"

    dataArg = "--add-data=res:res"
    if osName == "nt":
        # Windows needs a ``;``
        dataArg = dataArg.replace(":", ";")

    # -w: no console, -F: single file, -n: name of the generated file
    args = f'-w -F --icon=res/logo.png -n "Cole" {dataArg} "src/main.py"'
    command = f"{executable} -m {pyInstaller} {args} {excludedModules}"
    run(f"{command}".split(" "))


if __name__ == "__main__":
    main()
