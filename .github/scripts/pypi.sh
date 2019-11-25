#!/bin/bash
set -ex

if [ -d "./libgraphqlparser/" ]; then
	rm -rf "./libgraphqlparser/"
fi

make init

set_version_if_not_master() {
	cat /github/workflow/event.json | jq -e '. | select(.ref=="refs/heads/master")'
	return_code=$?

	if [ $return_code -ne 0 ]; then
		export TWINE_REPOSITORY_URL="https://test.pypi.org/legacy/"
		make set-version
	fi
} 

check_if_setup_file_exists() {
	if [ ! -f setup.py ]; then
		echo "setup.py must exist in the directory that is being packaged and published."
		exit 1
	fi
}

upload_package() {
	python setup.py sdist bdist_wheel
    # cibuildwheel --output-dir dist
    echo listing_files
    ls dist
    pip3 install "wheel<0.32.0" # cause auditwheel is pretty shit
    for whl in dist/*.whl; do
        auditwheel repair "$whl" -w dist || echo "skipping wheel repair for linux"
    done
    rm dist/*-linux_x86_64.whl || echo "skiping rm"
	twine upload --skip-existing dist/*
}

set_version_if_not_master

make get-version

check_if_setup_file_exists
upload_package