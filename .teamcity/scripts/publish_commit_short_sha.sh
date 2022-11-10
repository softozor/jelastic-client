#! /bin/bash

GIT_COMMIT_SHA=%build.vcs.number%
GIT_COMMIT_SHORT_SHA=${GIT_COMMIT_SHA:0:7}

echo "##teamcity[setParameter name='build.vcs.number' value='${GIT_COMMIT_SHORT_SHA}']"