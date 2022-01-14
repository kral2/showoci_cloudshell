#!/bin/sh

# Execute showoci.py to extract tenancy information to CSV files
#   showoci predefined parameters:
#   -a: print all resources
#   -mc: Compartment 'ManagedCompartmentForPaaS' is excluded
#   -csv: export to CSV files
#
#   showoci_report_to_xlsx.sh arguments:
#   $1 is the prefix for CSV files naming (mandatory argument)
#
#   sample command:
#   $./showoci_report_to_xlsx.sh mytenant

DATE=`date '+%Y-%m-%d_%H-%M'`
APPDIR=${HOME}/showoci_cloudshell
REPORT_DIR=${APPDIR}/report/${1}
CSV_DIR=${REPORT_DIR}/csv
JSON_DIR=${REPORT_DIR}/json

OUTPUT_FILE=${REPORT_DIR}/${DATE}_${1}_showoci_report.txt
JSON_FILE=${JSON_DIR}/${DATE}_${1}_showoci_report.json
CSV_FILE=${CSV_DIR}/${DATE}_${1}

# using delegation token authentication for OCI API
SHOWOCI_PARAM="-dt -mc -a"

# ensure a tenant name is provided
if [ "$#" -eq 0 ]; then
    echo "Please provide script arguments:"
    echo "1st argument (mandatory): CSV filenames prefix"
    echo "sample command:"
    echo "./showoci_report_to_xlsx.sh mytenant"
    exit 1
fi

# create report folder structure
mkdir -p ${REPORT_DIR}
mkdir -p ${CSV_DIR}
mkdir -p ${JSON_DIR}

# start extract job
echo "###################################################################################"
echo "# Start running showoci at `date`"
echo "# Job Run Output File = $OUTPUT_FILE"
echo "# CSV    File Prefix = $CSV_FILE"
echo "# csv output files created in $CSV_DIR for each service (csv_compute, csv_database, etc.)"
echo "# xlsx output file created in ${REPORT_DIR}"
echo "###################################################################################"
echo "Please Wait ..."

if [ "$#" -eq 1 ]; then
    $APPDIR/showoci.py $SHOWOCI_PARAM -sjf $JSON_FILE -csv $CSV_FILE > $OUTPUT_FILE 2>&1
fi

# Print Errors on screen
grep -i Error $OUTPUT_FILE

# Print Status
ERROR=""
WARNING=""
if [ `grep -i Error $OUTPUT_FILE | wc -l` -gt 0 ]; then
    ERROR=", with **** Errors ****"
fi

if [ `grep -i "Service Warning" $OUTPUT_FILE | wc -l` -gt 0 ]; then
    WARNING=", with **** Warnings ****"
fi

echo ""
echo "###################################################################################"
echo "# Finished at `date` $ERROR $WARNING "
echo "###################################################################################"

# merge CSV files to a single xlsx
echo ""
echo "###################################################################################"
echo "# Merge csv files to xlsx file and compress raw data (/csv and /json)"
echo "###################################################################################"

python3 $APPDIR/merge-CSVs-to-Excel.py $1 ${CSV_DIR} ${REPORT_DIR} >> $OUTPUT_FILE 2>&1
python3 $APPDIR/folder_to_archive.py ${CSV_DIR}.tgz ${CSV_DIR} >> $OUTPUT_FILE 2>&1
python3 $APPDIR/folder_to_archive.py ${JSON_DIR}.tgz ${JSON_DIR} >> $OUTPUT_FILE 2>&1

rm -rf ${CSV_DIR} ${REPORT_DIR}/json # ! quick/dirty hack : dont keep any log locally after archive is generated

#####################################################
## Cleanup - Gzip after 30 days, delete after 90 days
#####################################################
#/usr/bin/find ${REPORT_DIR} -type d -empty -prune -exec rm -rf '{}' \;
#/usr/bin/find ${REPORT_DIR} -mmin 1 -prune -exec rm -rf '{}' \; # ! quick/dirty hack : remove last archive (must run under 1Min O_O)
