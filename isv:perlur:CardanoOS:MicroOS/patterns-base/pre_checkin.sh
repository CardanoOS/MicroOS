#!/bin/sh
 
./create_32bit-patterns_file.pl -p base -s apparmor_opt -s basesystem -s console -s documentation -s enhanced_base_opt -s readonly_root_tools -s transactional_base -s update_test -s x11_opt -s x11_raspberrypi > pattern-definition-32bit.txt

