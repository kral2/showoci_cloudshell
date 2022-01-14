# Installer for showoci on OCI Cloud Shell

## Automatically Download, Extract and Install showoci on your cloudshell session

[![release](https://img.shields.io/github/v/release/kral2/showoci_cloudshell?colorB=2067b8)](https://github.com/kral2/)
[![license](https://img.shields.io/github/license/kral2/showoci_cloudshell?colorB=2067b8)](https://github.com/kral2/showoci_cloudshell)

---

The **showoci_cloudshell** script automates the process of downloading and installing showoci on your OCI Cloud Shell session and adds some handy helper tools.

- a shell script to generate a global extract tailored for execution on OCI Cloud Shell
- a ready to view XLSX file, merging each CSV files generated by show OCI
- archives of all CSV and JSON files

## Installation

Just run the command below on your terminal. This is the fastest and simplest way to get access to showoci and its helpers on OCI Cloud Shell.

``` shell
curl -L --silent https://raw.github.com/kral2/showoci_cloudshell/main/bootstrap.sh | bash
```

It will download the latest version of showoci and its helpers in the current user's home directory No sudo rights required. Tailored for [OCI Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro.htm).

## Run a report

Launch the reporting script and provide a label for your extract (e.g the tenant name).

``` shell
cd showoci_cloudshell
./showoci_report_to_xlsx.sh mytenant
```

At the end of showoci script execution, you will find in the `showoci_cloudshell/report/mytenant` folder:

- an excel file will the collected data loaded from the CSV files
- an archive containing all the csv files
- an archive containing all the json files
