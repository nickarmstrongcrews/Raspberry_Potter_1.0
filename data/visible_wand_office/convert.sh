# record of commands I used to reduce file size before commit by cropping and converting to jpg
files=$(ls visible_wand*.bmp) ; for f in $files ; do convvert $f -crop 652x366+26+172 $(basename $f .bmp)_cropped.bmp ; done
for f in $(ls *.bmp) ; do convert -quality 95 $f $(basename $f .bmp).jpg ; done
