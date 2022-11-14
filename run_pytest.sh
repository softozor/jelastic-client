#! /bin/sh

poetry run pytest "$@" -s -v --teamcity || [ $? = 1 ]