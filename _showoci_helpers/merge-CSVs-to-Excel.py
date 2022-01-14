'''
#
# Copyright (c) 1982-2022 Oracle and/or its affiliates. All rights reserved.
# 
# Initial version : January, 2020
# Author: cetin.ardal@oracle.com
# Description: Looks for csv files in a directory, and merge them all into a single xlsx file with multiple workbook.
# It is optimized for showoci csv output files, but is commoditized enough to be used for other purpose.
# 
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
'''

import os # needed to filter files with a specific extension inside a folder (listdir) and tar file construction (path.sep)
import pandas as pd # needed to import and export excel files
import re # needed to work with regex
import tarfile # needed to tar and gzip original files after being merged
import datetime, sys

version = "0.1.0"
my_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

my_file_prefix = 'showoci_report'
my_working_dir = '.'
my_output_dir = '.'

if len(sys.argv) == 2:
    my_file_prefix = sys.argv[1] + '_' + my_file_prefix
elif len(sys.argv) == 3:
    my_file_prefix = sys.argv[1] + '_'  + my_file_prefix
    my_working_dir = sys.argv[2]
elif len(sys.argv) == 4:
    my_file_prefix = sys.argv[1] + '_'  + my_file_prefix
    my_working_dir = sys.argv[2]
    my_output_dir = sys.argv[3]
elif len(sys.argv) > 4:
    print(f'''
        {sys.argv[0]} arguments:
        $1 is the file prefix (optional argument)
        $2 is the working directory, where csv files are (optional argument)
        $3 is the working directory, where the xlsx file will be (optional argument)

        sample command:
        $./{sys.argv[0]} mytenant ./reports/csv ./reports
    ''')
    exit()

my_file_extension = '.csv'
output_merged_xslx = my_output_dir + '/' + my_date + '_' + my_file_prefix + '.xlsx'

def set_parser_arguments():
    '''
    Handle command line arguments. Not used for now.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)

    if len(sys.argv) < 2:
        parser.print_help()
        return None

    result = parser.parse_args()
    print(result)
    return result

def find_files_with_extension(working_dir, file_extension):
    '''
    Search a directory for files that match a specific file extension, and add them to a list
    Return the list of files in the filtered files.
    '''
    list_of_files = os.listdir(working_dir)
    return [ file for file in list_of_files if file.endswith( file_extension ) ]

def list_filtered_files(working_dir, file_extension):
    '''
    Call find_files_with_extension() and print the list of matched files
    '''
    filtered_files_list = find_files_with_extension(working_dir, file_extension)
    print(f'List of {file_extension} found in {working_dir} directory:')
    i = 0
    for file in filtered_files_list:
        i = i + 1
        print(f'- {file}')
    print(f'Total: {i} {file_extension} files\n')

def merge_csv_files_to_xlsx(working_dir, file_extension):
    '''
    Call find_files_with_extension() and merge all files into one xlsx
    '''
    csv_list = find_files_with_extension(working_dir, file_extension)
    writer = pd.ExcelWriter(output_merged_xslx, engine='xlsxwriter')
    print(f'Starting CSV files merge to {output_merged_xslx}:')
    i = 0
    for file in csv_list:
        current_csv = working_dir + '/' + csv_list[i] # get the current csv file
        worksheet_name = re.search(r'([a-z]*)_([a-z_]*).csv', f'{csv_list[i]}', re.IGNORECASE) # regex to cut anything before the first underscore and supress file extension
        worksheet_name = worksheet_name.group(2)[:31] # set the worksheet name & truncate if longer than 31 chars
        print(f'import {current_csv} to worksheet: {worksheet_name}')
        current_csv_dataframe = pd.read_csv(current_csv) # load the current csv file to pandas dataframe
        current_csv_dataframe.to_excel(writer, index=None, header=True, sheet_name=worksheet_name) # add the current pandas dataframe to excel on a new worksheet
        i = i +1
    # workbook = writer.book # not used at the moment. Needed to expose the pandas data frame to xlsxwriter and execute additionnal manipulations.
    writer.save()
    writer.close()
    print(f'{output_merged_xslx} generated. It contains {i} worksheets (one per imported csv file).')

def make_tarfile(output_filename, source_dir):
    '''
    Make a compressed tar archive of a folder
    '''
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.sep)

find_files_with_extension(my_working_dir, my_file_extension)
list_filtered_files(my_working_dir, my_file_extension)
merge_csv_files_to_xlsx(my_working_dir, my_file_extension)
