from pygtail import Pygtail
import re

def main():
    myDict = {
        "Chaos Orb-Chromatic Orb":["1","2"]
    }
    k = "Chaos Orb"
    p = "Chromatic Orb"
    print(myDict[k+"-"+p])
if __name__ == "__main__":
    main()