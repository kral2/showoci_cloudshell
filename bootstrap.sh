
# get the installer
echo ""
echo "*** Launching showoci_cloudshell_install"
git clone https://github.com/kral2/showoci_cloudshell.git showoci_cloudshell_install --quiet

# Checkout to the latest release tag
# see https://blog.markvincze.com/download-artifacts-from-a-latest-github-release-in-sh-and-powershell/
LATEST_RELEASE=$(curl -L -s -H 'Accept: application/json' https://github.com/kral2/showoci_cloudshell/releases/latest)
LATEST_RELEASE_TAG=$(echo $LATEST_RELEASE | sed -e 's/.*"tag_name":"\([^"]*\)".*/\1/')

# execute the installer
cd showoci_cloudshell_install/install_on_cloudshell || exit
git checkout "$LATEST_RELEASE_TAG" --quiet
ansible-playbook main_showoci.yml

# cleanup
cd || exit
rm -rf showoci_cloudshell_install