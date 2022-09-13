#!/bin/bash
SCRIPT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd $SCRIPT_DIRECTORY > /dev/null

rm -rf .package ou_member_accounts.zip

zip ou_member_accounts.zip ou_member_accounts.py

popd > /dev/null
