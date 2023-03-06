#!/bin/bash

# Recursively find all .mediawiki files in the bips directory
find ../bips -type f -name "*.mediawiki" -execdir sh -c '
    for filename do
        # Replace the .mediawiki extension with .md
        output_file="${filename%.mediawiki}.md"

        # Use pandoc to convert the file to Markdown
        pandoc -f mediawiki -t markdown "$filename" -o "$output_file"

        echo "Converted $filename to $output_file"
    done
' sh {} +
