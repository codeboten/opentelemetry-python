#!/bin/sh

# This script builds wheels for the API, SDK, and extension packages in the
# dist/ dir, to be uploaded to PyPI.

set -ev

# Get the latest versions of packaging tools
python3 -m pip install --upgrade pip setuptools wheel

BASEDIR=$(dirname $(readlink -f $(dirname $0)))
DISTDIR=dist


if [ -z $1 ]; then
  echo "missing argument"
  echo "./build.sh [prerelease|ga]"
  exit 1
fi

if [ $1 == "ga" ]; then
  PACKAGES=$(cat <<DIRS
  opentelemetry-api/
  opentelemetry-sdk/
  opentelemetry-proto/
  exporter/*/
  propagator/*/
DIRS
)
elif [ $1 == "prerelease" ]; then
  PACKAGES=$(cat <<DIRS
  opentelemetry-instrumentation/
  opentelemetry-distro/
  shim/*/
DIRS
)
fi

(
  cd $BASEDIR
  mkdir -p $DISTDIR
  rm -rf $DISTDIR/*

 for d in $PACKAGES; do
   (
     echo "building $d"
     cd "$d"
     # Some ext directories (such as docker tests) are not intended to be
     # packaged. Verify the intent by looking for a setup.py.
     if [ -f setup.py ]; then
      python3 setup.py sdist --dist-dir "$BASEDIR/dist/" clean --all
     fi
   )
 done
 # Build a wheel for each source distribution
 (
   cd $DISTDIR
   for x in *.tar.gz ; do
     pip wheel --no-deps $x
   done
 )
)
