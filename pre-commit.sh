#!/bin/bash


read name version < <(poetry version)

read pversion < <(python -c  "from ${name} import __version__;print(__version__)")

init=${name}/__init__.py

if [[ "${pversion}" != "${version}" ]]; then
    (
cat <<-UPDATEINIT
"""Python ${name} package."""
__version__ = "${version}"
UPDATEINIT
    ) >$init
    git add $init
fi
