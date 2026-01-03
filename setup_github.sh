#!/bin/bash
# Setup script for GitHub repository

echo "Setting up SignSegmentationUI GitHub repository..."

# Initialize git (if not already done)
if [ ! -d .git ]; then
    git init
fi

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Sign Segmentation Validation UI"

# Set main branch
git branch -M main

# Add remote repository
git remote remove origin 2>/dev/null  # Remove if exists
git remote add origin https://github.com/Bhumika158/SignSegmentationUI.git

echo ""
echo "✅ Repository setup complete!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "2. Deploy to Render.com (see SETUP_GITHUB.md for details)"
echo ""

