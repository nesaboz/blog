# brew install imagemagick
for file in *.HEIC; do
    magick "$file" "${file%.HEIC}.png"
done
