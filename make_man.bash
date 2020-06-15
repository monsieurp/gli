#!/usr/bin/env bash
pod2man gli.pod | \
    sed "s#User Contributed Perl Documentation#Gentoo Linux User Command#; s#perl v5.30.3#Gentoo Linux#;" > gli.1 
