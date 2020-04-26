#!/bin/bash

VERSION=`echo $1 | cut -f 2 -d /`
echo "Using version ${VERSION}"

# check the version matches expected versioning e.g
# 0.6, 0.6b, 0.6b0, 0.6.0
if [[ ! "${VERSION}" =~ ^([0-9])(\.*[0-9]{1,5}[a-b]*){1,3}$ ]]; then
    echo "Version number invalid: $VERSION"
    exit 1
fi

function update_version_file() {
    errors=0
    for f in `find . -name version.py`; do
        # check if version is already in version.py
        grep -q ${VERSION} $f;
        rc=$?
        if [ $rc == 0 ]; then
            errors=1
            echo "${f} already contains ${VERSION}"
            continue
        fi
        # update version.py
        perl -i -pe "s/__version__.*/__version__ = \"${VERSION}\"/g" ${f};
        git add ${f};
    done
    if [ ${errors} != 0 ]; then
        exit 1
    fi
}

function update_changelog() {
    errors=0
    for f in `find . -name CHANGELOG.md`; do
        # check if version is already in CHANGELOG
        grep -q ${VERSION} $f;
        rc=$?
        if [ $rc == 0 ]; then
            errors=1
            echo "${f} already contains ${VERSION}"
            continue
        fi
        # check if changelog contains any new details
        changes=`sed -n '/## Unreleased/,/^##/p' ${f} | grep -v '^##'  | wc -w | awk '{$1=$1;print}'`
        if [ ${changes} != "0" ]; then
            # update CHANGELOG.md
            perl -i -pe 's/## Unreleased.*/## Unreleased\n\n## '${VERSION}'/' ${f};
            git add ${f};
        else
            echo "Skipping ${f}, no changes detected"
        fi
    done
    if [ ${errors} != 0 ]; then
        exit 1
    fi
}

update_version_file
update_changelog

git config --local user.email "action@github.com"
git config --local user.name "GitHub Action"
git commit -m "updating changelogs and version to ${VERSION}"
