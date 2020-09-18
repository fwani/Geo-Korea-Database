#!/bin/bash

OS=`uname`
case $OS in
  'Linux')
    source_file=${BASH_SOURCE[0]}
    ;;
  'Darwin')
    source_file=${0}
    ;;
  *)
    exit 1
    ;;
esac
export GEO_KR_DATABASE=`cd $(dirname ${source_file}) && pwd`
