#!/bin/bash

directories=(../bolts ../bips)

for dir in "${directories[@]}"
do
    echo "Trimming markdown files in $dir directory..."
    find "$dir" -type f -name '*.md' -print0 | while IFS= read -r -d $'\0' file
    do
        sed -i '' -e 's/^[[:space:]]*//' "$file"
    done
done

echo "Done!"
