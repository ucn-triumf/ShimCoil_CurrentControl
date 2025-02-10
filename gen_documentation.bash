#!/bin/bash
# generate documentation with working links
# Derek Fujimoto
# Feb 2025

# note: requires handsdown (https://github.com/vemel/handsdown)

# generate the documentation
cd src/ShimCoil
handsdown -o ../../docs --theme readthedocs

# fix the broken links
cd ../../docs
for file in *;
do
    if [ -f "$file" ];  then

        # replace bad empty parentheses
        sed -i 's/()././' $file

        # replace broken table of contents links
        name=$(basename $file .md)
        sed -i "s/#${name}()/#${name}/i" $file
    fi
done