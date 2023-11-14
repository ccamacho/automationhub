#!/bin/bash
set -ex

#############################################################################
#                                                                           #
# Copyright automationhub contributors.                                          #
#                                                                           #
# Licensed under the Apache License, Version 2.0 (the "License"); you may   #
# not use this file except in compliance with the License. You may obtain   #
# a copy of the License at:                                                 #
#                                                                           #
# http://www.apache.org/licenses/LICENSE-2.0                                #
#                                                                           #
# Unless required by applicable law or agreed to in writing, software       #
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
# License for the specific language governing permissions and limitations   #
# under the License.                                                        #
#                                                                           #
#############################################################################

if [ -z "$GALAXY_KEY" ]; then
    echo "GALAXY_KEY is not set";
    exit 1;
fi

#
# Initial variables
#

namespace=ccamacho
name=automationhub

all_published_versions=$(curl -s "https://galaxy.ansible.com/api/v3/plugin/ansible/content/published/collections/index/$namespace/$name/versions/?format=json&limit=1000&offset=0" | jq -r '.data' | jq -c '.[].version')
current_galaxy_version=$(cat $namespace/$name/galaxy.yml | shyaml get-value version)
current_galaxy_namespace=$(cat $namespace/$name/galaxy.yml | shyaml get-value namespace)
current_galaxy_name=$(cat $namespace/$name/galaxy.yml | shyaml get-value name)
publish="1"

#
# Check all the current published versions and if the
# packaged to be created has a different version, then
# we publish it to Galaxy Ansible
#

for ver in $all_published_versions; do
    echo "--"
    echo "Published: "$ver
    echo "Built: "$current_galaxy_version
    echo ""
    if [[ $ver == \"$current_galaxy_version\" ]]; then
        echo "The current version $current_galaxy_version is already published"
        echo "Proceed to update the galaxy.yml file with a newer version"
        echo "After the version change, when the commit is merged, then the package"
        echo "will be published automatically."
        publish="0"
    fi
done

if [ "$publish" == "1" ]; then
    echo 'This version is not published, publishing!...'

    echo 'Building and pushing the Ansible collection to Ansible Galaxy...'
    cd ./$namespace/$name/
    mkdir -p releases
    ansible-galaxy collection build -v --force --output-path releases/
    ansible-galaxy collection publish \
        releases/$current_galaxy_namespace-$current_galaxy_name-$current_galaxy_version.tar.gz \
        --server https://galaxy.ansible.com \
        --ignore-certs \
        --verbose \
        --api-key $GALAXY_KEY
fi
