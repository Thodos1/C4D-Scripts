"""
Copyright (c) <2023> <Maksym Vysokolov>

Website: cataclysm-vfx.com

Description: 
Situational rework of Save Incremental.
Some studios require initials at the end of the file, but C4D doesn't get it.
This script saves everything correctly with dynamic numbering and non-destructive. Respects other initials in the same folder and file name

"""
import c4d
import os
import re

FILLING_DIGITS = 4  # Define the number of digits you want to use for counter filling eg. 4 means 0001

SUFFIX = "_TH"  # Define the suffix with Artist Name


def get_max_counter(path, base_name, UNDERSCORE_CHANGE, SUFFIX):

    # Regular expression to match the counter
    counter_pattern = re.compile(rf'{base_name}_0*(\d+){re.escape(SUFFIX)}')


    # Get all files in the directory
    files = os.listdir(path)

    max_counter = 0

    # Go through all files
    for file in files:
        if UNDERSCORE_CHANGE is True:
            file = file.replace(" ", "_")
            #print(f"HERE IS A COUNTER_STUFF {file}")
        match = counter_pattern.fullmatch(os.path.splitext(file)[0])
        if match:
            # If a file with a counter is found, update max_counter if necessary
            counter = int(match.group(1))
            if counter > max_counter:
                max_counter = counter

    return max_counter

def save_incremental():
    global SUFFIX

    UNDERSCORE_CHANGE = False # DO NOT CHANGE! Works as a marker for underscores

    doc = c4d.documents.GetActiveDocument()  # Get the active document
    path = doc.GetDocumentPath()  # Get the document path
    name = doc.GetDocumentName()  # Get the document name
    base_name_or, ext = os.path.splitext(name)  # Separate the base name and extension
    c4d.documents.SaveDocument(doc, os.path.join(path, name), c4d.SAVEDOCUMENTFLAGS_NONE, c4d.FORMAT_C4DEXPORT)  # Save the document
    base_name = base_name_or.replace(" ", "_")
    if base_name != base_name_or:
        UNDERSCORE_CHANGE = True
        #print("FOUND SPACES")

    #else:
        #pass

    if not base_name.endswith(SUFFIX):
        # Split the base_name into parts using underscore as separator
        parts = base_name.split('_')

        # Check if the last part of the name is exactly 2 letters
        if len(parts[-1]) == 2 and parts[-1].isalpha():
            # If it is, then use this as new suffix (with underscore)
            SUFFIX = f"_{parts[-1]}"
            


    # Remove existing counter and _TH from base_name, if any
    if re.search(rf'_(\d{{{FILLING_DIGITS}}}){re.escape(SUFFIX)}$', base_name):
        base_name = re.sub(rf'_(\d{{{FILLING_DIGITS}}}){re.escape(SUFFIX)}$', '', base_name)

    elif base_name.endswith(SUFFIX):
        base_name = base_name[:-len(SUFFIX)]



    # Get highest existing counter
    max_counter = get_max_counter(path, base_name, UNDERSCORE_CHANGE, SUFFIX)

    # Start from the next counter
    counter = max_counter + 1

    new_name = f"{base_name}_{str(counter).zfill(FILLING_DIGITS)}{SUFFIX}{ext}"  # New name with counter before _TH

    if UNDERSCORE_CHANGE is True:
        new_name = new_name.replace("_", " ")



    new_path = os.path.join(path, new_name)  # New path
    doc.SetDocumentName(new_name)
    result = c4d.documents.SaveDocument(doc, new_path, c4d.SAVEDOCUMENTFLAGS_NONE, c4d.FORMAT_C4DEXPORT)  # Save the document

    if not result:
        print("Failed to save document.")
    else:
        print(f"Document saved as {new_name}.")


def main():
    save_incremental()

if __name__=='__main__':
    main()
