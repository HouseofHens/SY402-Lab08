# SY402-Lab08
Repository containing Lab 08 for MIDN Henry and MIDN Hoang

## Functions within hash.py

- ### main()
  main() is our function that runs through the program flow and will run our other functions if necessary.
  Within main() we check if our baseline file already exists, if it does then we proceed to create a new hash file and compare them with our compareHashes() function.
  After our compareHashes() function runs we ask if the user wants to switch the baseline file.

- ### makeHashFile(csvFilepath)
  makeHashFile() is our function that handles the bulk of our work. Within makeHashFile() we pass the argument csvFilepath which is the filepath that we will create to store our hashes of the file system. We then use os.path to walk through the file system. We then skip any directories that we don't want to hash such as /dev. We then take every file and hash the contents. We accomplish this by opening each file and reading them into a sha256 object from the hashlib object. Once the file is hashed, we then pull the current date and time and write everything to our csv file that we created. 

- ### compareHashes()
  compareHashes() is our function that checks every hash of our files and will print out those that are different. We accomplished this by opening both files and storing their filepaths and respective hashes into a dictionary with each filepath being a key in the dictionary. We then used the python library DeepDiff to compare both dictionaries. This library will do the work and gives us a deepdiff object that contains important information such as if any files were added, if files were removed, or if the hashes of each file changed. From this deepdiff object, we print out the information we need and return out of the function.

- ### switchFiles()
  switchFiles() is a simple function that gives one small functionality to the hash.py program. After the csv files have been compared and the differences have been printed out for the user we proceed to ask if the user would like to switch the baseline to be the new hashed file that we created. If they do then we use the os library to remove our original baseline file and then rename our new file to hashed_values.csv so that it becomes our new baseline. 
