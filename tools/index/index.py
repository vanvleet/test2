##############################################################################
################################## IMPORTS ###################################
##############################################################################
import os
import re
import datetime
import argparse
import sys
import json

##############################################################################
############################## HELPER FUNCTIONS ##############################
##############################################################################
def parse_meta_table(meta_table):
    temp_dict = {}
    for line in meta_table[3:]:
        if len(line) != 0:
            elements = line.split("|")
            temp_dict[elements[1].strip()] = elements[2].strip()
    return temp_dict

def parse_proc_table(proc_table):
    procs={}
    for line in proc_table[3:]:
       if len(line) != 0:
           elements = line.split("|")
           procs[elements[1].split(".")[-1].strip()] = elements[2].strip()
    return procs

def parse_trr_meta(TRR_path):
    TRR_dict = {}  #dict to hold all the values parsed from the TRR meta
    
    #file_path = os.path.join(DID_path, "README.md")
    file = open(TRR_path, "r")

    #Parse the TRR README.md line by line
    for line in file:
        if line.strip().startswith("# "):
            #found the title
            TRR_dict['name'] = line.strip()[2:] #slice away the title markdown
                
        if line.strip() == "## Metadata":
            # found the start of the metadata section
            meta_table=[] #to hold the lines of the table for parsing
            meta_line=next(file) #get the next line
            while not meta_line.startswith("##"):   # loop till we reach the next header, reading in all metadata table lines
                # some elements will be links and enclosed in brackets, so we need to remove them
                meta_line = meta_line.replace("]","")
                meta_line = meta_line.replace("[","")
                meta_table.append(meta_line.strip())
                meta_line = next(file)

            meta_dict = parse_meta_table(meta_table) #load all the data from the meta table into the dict
            #need to do further processing to get the meta names right and formats right
            if 'ID' in meta_dict:
                TRR_dict['id'] = meta_dict['ID']
            else: 
                sys.exit("Parsing error: Metadata table is missing 'ID' field.")
            if 'Tactics' in meta_dict:
                TRR_dict['tactics'] = [item.strip() for item in meta_dict['Tactics'].split(",")]
            else: 
                sys.exit("Parsing error: Metadata table is missing 'Tactics' field.")
            if 'Contributors' in meta_dict:    
                TRR_dict['contributors'] = [item.strip() for item in meta_dict['Contributors'].split(",")]
            else: 
                sys.exit("Parsing error: Metadata table is missing 'Contributors' field.")
            if 'External IDs' in meta_dict:
                TRR_dict['external_ids'] = [item.strip() for item in meta_dict['External IDs'].split(",")]
            else: 
                sys.exit("Parsing error: Metadata table is missing 'External IDs' field.")
            if 'Platforms' in meta_dict:    
                TRR_dict['platforms'] = [item.strip() for item in meta_dict['Platforms'].split(",")]
            else: 
                sys.exit("Parsing error: Metadata table is missing 'Platforms' field.")

        if line.strip() == "## Procedures":
            # found the start of the procedures section
            proc_table=[]
            proc_line=next(file) #get the next line
            while not proc_line.startswith("##"):   # loop till we reach the next header, reading in all metadata table lines
                proc_table.append(proc_line.strip())
                proc_line = next(file)

            proc_dict = parse_proc_table(proc_table) #load all the data from the procedures table into the dict
            TRR_dict['procedures'] = proc_dict
    
    return(TRR_dict)

def update_index(trr_dict, index):
    #get timestamp for adding the creation/update time
    today = datetime.date.today()
    today_string = today.strftime("%Y-%m-%d")

    found_id = False
    for trr in index:
        if trr['id'] == trr_dict['id'] and trr['platforms'][0] == trr_dict['platforms'][0]:  #found the right one
            found_id = True
            trr['name'] = trr_dict['name']
            trr['contributors'] = trr_dict['contributors']
            trr['external_ids'] = trr_dict['external_ids']
            trr['platforms'] = trr_dict['platforms']
            trr['procedures'] = trr_dict['procedures']
            trr['tactics'] = trr_dict['tactics']

    if not found_id:  #ID isn't in index already, add it
        #add a publication date
        trr_dict['pub_date'] = today_string
        index.append(trr_dict) #add the new element to the index


##############################################################################
#################################### MAIN ####################################
##############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script will index a specified TRRs (merge mode) or the full repo (index mode). A merge test mode is available to ensure indexing will run successfully without updating the index. This script should be run from the root of the TRR repo.")
    parser.add_argument('mode', choices=['index', 'merge', 'merge_test'])
    parser.add_argument('-f', '--files', nargs='+', help="A list of files to parse (in 'merge' or 'merge_test' modes.")

    args = parser.parse_args()
    print(f"Running in {args.mode} mode.\n")


    #get the current index
    if args.mode != "merge_test":  #test mode won't make any changes to the index.json
        with open("index.json", "r") as f:
            content = f.read()
        if len(content) > 0:  #make sure there's data in the index.json
            index = json.loads(content) #parse the index as JSON
        else: 
            index = []  #if index.json is empty make it an empty JSON array.

    #get list of files to be parsed
    if args.mode == "merge" or args.mode == "merge_test":  #files will be provided as an argument
        if args.files:
            files = args.files
        else:
            sys.exit("Please provide list of files to parse in 'merge' or 'merge_test' modes.")
    elif args.mode == "index":  #make list of all TRR README.mds in the repo
        files = []
        for dirpath, dirnames, filenames in os.walk('reports'):
            for filename in filenames:
                if filename == "README.md":
                    full_path = os.path.join(dirpath, filename)
                    files.append(full_path)  
            
    #parse each file, updating the index if appropriate  
    for file in files:
        print(f"Parsing file: {file}")
        trr_dict = parse_trr_meta(file)
        if args.mode == "merge_test":
            print(f"Parsing test completed successfully, indexed TRR would be:")
            print("------------------")
            print(trr_dict)
            print("------------------\n")
        else: # merge or index mode - update index.json
            update_index(trr_dict, index)
            
            if args.mode == "merge":
                #add/update the last updated timestamp if we're merging. If we're reindexing everything, don't update the last_update timestamp.
                trr['last_update'] =  today_string
            
    # print(json.dumps(index, indent=2))
    
    if args.mode != "merge_test":  #test mode won't make any changes to the index.json
        with open("index.json", "w") as f:
            f.write(json.dumps(index, indent=2))

    sys.exit(0) #exit successfully    
