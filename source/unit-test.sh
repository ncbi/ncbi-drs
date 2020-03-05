#!/bin/sh
docker run -v `pwd`:/source:ro --rm `docker build -qq .`
