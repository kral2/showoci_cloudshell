import tarfile, os, sys

my_output_filename = ""
my_source_dir = ""

if len(sys.argv) == 3:
    my_output_filename = sys.argv[1]
    my_source_dir = sys.argv[2]
else:
    print(f'''
        {sys.argv[0]} arguments:
        $1 is the archive file name (mandatory argument)
        $2 is the source directory to archive (mandatory argument)

        sample command:
        $./{sys.argv[0]} myarchive.tar.gz my_folder/
    ''')
    exit()

def folder_to_archive(output_filename, source_dir, delete_source_dir=False):
    # TODO : add kwarg to handle file format and compression
    '''
    Make a tar archive of a folder. Currently, compressed with gzip.
    '''
    
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.sep)
    return tar

my_archive = folder_to_archive(my_output_filename,my_source_dir, delete_source_dir=True)
print(f'{my_output_filename} ({round(os.path.getsize(my_output_filename)/(1024*1024), 3)} MB)')

