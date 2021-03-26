#!/usr/bin/env python3

import hashlib, os
from os import path
from datetime import datetime
from deepdiff import DeepDiff

skip = ["/dev","/proc","/run","/sys","/tmp","/var/lib","/var/run"]

def main():
    #if the intialHash file exists, just compare a new hash file
    if path.exists("/tmp/hashed_values.csv"):
        print("Baseline file exists, comparing hashes")
        compareHashes()

        while True:
            value = input("Would you like the new hashed values to become the new baseline? (y/n)")
            if value == "y":
                switchFiles()
                break
            elif value == "n":
                print("Thank you for checking your hashes.")
                break
            else:
                print("Please enter a valid response.")
                continue
    else:
        print("Baseline file does not exist, completing initial hash")
        makeHashFile("/tmp/hashed_values.csv")


def makeHashFile(csvFilepath):
    #csvFilepath is a string filepath to where you want the initial hashed file to be stored
    #open a csv file to write files and hashes into
    csvFile = open(csvFilepath, "w")

    for root, dirs, files in os.walk("/"):
        if root in skip:
            dirs[:]=[]
            files[:]=[]
        path = root.split(os.sep)
        for file in files:
            filepath=os.path.join(root,file)
            #try to open each file to then hash
            try:
                openFile = open(filepath, "rb")
                readFile = openFile.read()
                openFile.close()

                #create the hash object
                sha = hashlib.sha256(readFile)
                fileHash = sha.hexdigest()

                #pull current date/time
                dateTime = datetime.now()

                #write to my csv file
                csvFile.write(filepath + "," + fileHash + "," + str(dateTime) + "\n")

#            except IsADirectoryError:
#                continue
            except:
                continue

    #close csv File
    csvFile.close()
    return

def compareHashes():
    #create another file of hashes and then compare the two
    makeHashFile("/tmp/hashed_values(1).csv")
    f0 = open("/tmp/hashed_values.csv", "r")
    f1 = open("/tmp/hashed_values(1).csv", "r")
    baseHash = f0.readlines()
    newHash = f1.readlines()

    #store paths and hashes in two separate dictionaries to then compare
    baseDict = {}
    for a in baseHash:
        oldList = a.split(",")
        path0 = oldList[0]
        hash0 = oldList[1]
        baseDict[path0] = hash0

    newDict = {}
    for b in newHash:
        newList = b.split(",")
        path1 = newList[0]
        hash1 = newList[1]
        newDict[path1] = hash1

    #compare the two dictionaries
    differences = DeepDiff(baseDict, newDict)

    try:
        added = differences["dictionary_item_added"]
        print("Files Added:")
        for c in added:
            array = c.split("'",1)
            addedFile = array[1]
            addedFile = addedFile[:-2]
            print(addedFile)
    except KeyError:
        print("No Files Added.")


    try:
        removed = differences["dictionary_item_removed"]
        print("Files Removed:")
        for d in removed:
            array1 = d.split("'",1)
            removedFile = array1[1]
            removedFile = removedFile[:-2]
            print(removedFile)
    except KeyError:
        print("No Files Removed.")


    try:
        changed = differences["values_changed"]
        print("Hashes Changed:")
        for e in changed:
            array2 = e.split("'",1)
            changedFile = array2[1]
            changedFile = changedFile[:-2]
            print(changedFile)
    except KeyError:
        print("No Hashes Changed.")


    return
def switchFiles():
    #If I want my new hashFile to be the new baseline I will switch the files, otherwise I will keep the current baseline
    os.remove("/tmp/hashed_values.csv")
    os.rename(r"/tmp/hashed_values(1).csv", r"/tmp/hashed_values.csv")
    return

if __name__=="__main__":
    main()
