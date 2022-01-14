
# get the installer
echo ""
echo "*** Launching showoci_cloudshell_install"
git clone https://github.com/kral2/showoci_cloudshell.git

# execute the installer
cd showoci_cloudshell/install_on_cloudshell || exit
ansible-playbook main_showoci.yml

# cleanup
cd || exit
rm -rf showoci_cloudshell