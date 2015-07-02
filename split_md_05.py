# python3
# split_md_05.py

# 2014-05-06 18:15 

# Script for Splitting Markdown files into smaller files and folders
# based on header levels: # Header 1 becomes numbered sub folders (groups),
# and ## Header 2 becomes numbered markdown files (sheets).
# Main folder can then be draged into Ulysses archive, either "iCloud" or "On My Mac")
# Handy when importing big projects from other Markdown sources.
# Also generates combined .marked file to be opened in Marked 2.1

# 2014 (cl) RoyRogers56

import re
import os
# import shutil
import sys

num_files = True
path = ""
md_file_name = "test.md"

if len(sys.argv) > 1:
    if sys.argv[1] != "":
        md_file_name = sys.argv[1]

if not os.path.exists(md_file_name):
    print("File missing:", md_file_name)
    quit()

path = md_file_name[:-3] + "/"


def make_dir(proc_path):
    if not os.path.exists(proc_path):
        os.makedirs(proc_path)


def clean_file_name(fname):
    fname = fname.replace(":", "-")
    fname = fname.replace("/", "_")
    fname = fname.replace("\\", "_")
    fname = fname.replace("?", "-")
    fname = fname.replace("|", "-")
    fname = fname.replace("—", "-")
    return fname


def print_file(subpath, fname, text):

    fname = clean_file_name(fname)
    subpath = clean_file_name(subpath)
    make_dir(path + subpath)
    subpath += "/"

    text_file = open(path + subpath + fname, "w", encoding='utf-8')
    text_file.write(text)
    text_file.close()
    print(str(subpath.encode("utf-8"))[2:-1], str(fname.encode("utf-8"))[2:-1])

    return "<<[" + subpath + fname + "]\n"
#end_def print_file


# Main program:

if os.path.exists(path):
    # Be careful with rmtree, in case you have and existing folder with same name,
    # everything will be deleted without warning!
    # shutil.rmtree(path)

    # Safer with manual rename or delete:
    print("*** Path already exists, please delete or rename:", path)
    quit()

if not os.path.exists(path):
    make_dir(path)

md_text = ""
md_file = open(md_file_name, "r", encoding='utf-8')
md_text = md_file.read()
md_file.close()

md_combined = ""

lines = md_text.split("\n")

file_num = 1
path_num = 1
file_prefix = ""
path_prefix = ""
if num_files:
    file_prefix = str(file_num).zfill(2) + " - "
    path_prefix = str(path_num).zfill(2) + " - "

subpath = path_prefix + "Front matter"
fname = subpath + ".md"

sect_text = ""
for line in lines:
    if line.strip().startswith("###"):  # - h3 - h6
        # Any header of h3, h4 etc. will be included in same file
        # (File split is done on h2, and sub folders made on h1)
        # (change to #### to split on lower level h3)
        sect_text += line + "\n"
    elif line.strip().startswith("#"):  # - h1 and h2
        file_num += 1
        if num_files:
            file_prefix = str(file_num).zfill(2) + " - "
        if sect_text != "":
            md_combined += print_file(subpath, fname, sect_text)
        elif path_num == 1:
            path_num = 0
        if line.startswith("# "):  # h1
            path_num += 1
            file_num = 1
            if num_files:
                path_prefix = str(path_num).zfill(2) + " - "
                file_prefix = str(file_num).zfill(2) + " - "

            subpath = path_prefix + re.sub(r"^(#+) ?(.+?) ?#*$", r"\2",
                                           line.strip())

        fname = file_prefix + re.sub(r"^(#+) ?(.+?) ?#*$", r"\2_\1",
                                     line.strip()) + ".md"
        sect_text = ""
        sect_text += line + "\n"

    else:
        sect_text += line + "\n"
#end_for line in lines

md_combined += print_file(subpath, fname, sect_text)

text_file = open(path + "split-combined.marked", "w")
text_file.write(md_combined)
text_file.close()

print()
print("================================================================================")
print("*** Markdown split completed to folder:", path)
print("================================================================================")
