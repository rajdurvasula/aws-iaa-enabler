#!/bin/bash
SCRIPT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd $SCRIPT_DIRECTORY > /dev/null

rm -rf .package enable_iaa_member.zip

zip enable_iaa_member.zip enable_iaa_member.py

popd > /dev/null
