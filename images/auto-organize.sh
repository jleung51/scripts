#!/bin/sh

SCRIPTS_DIR="$(dirname "$0")"

# Modify extensions and filetypes
echo "Lowercasing extensions..."
$SCRIPTS_DIR/lowercase-extensions
echo "Standardizing JPG extensions..."
$SCRIPTS_DIR/standardize-jpg
echo "Converting PNG files to JPG..."
$SCRIPTS_DIR/png-to-jpg

# Modify filenames
echo "Re-labeling images in sequential order..."
$SCRIPTS_DIR/number-img

# Modify image sizes
echo "Resizing images to be approximately under 1 MB..."
$SCRIPTS_DIR/resize-img-auto

echo ""
echo "____________________________________"
echo ""
echo "Auto-organization complete. Image files:"
$SCRIPTS_DIR/summary