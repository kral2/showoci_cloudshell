
# get the installer
echo ""
echo "*** Launching showoci_cloudshell_install"
git clone https://github.com/kral2/showoci_cloudshell.git showoci_cloudshell_install

# execute the installer
cd showoci_cloudshell_install/install_on_cloudshell || exit
ansible-playbook main_showoci.yml

# cleanup
cd || exit
rm -rf showoci_cloudshell_install