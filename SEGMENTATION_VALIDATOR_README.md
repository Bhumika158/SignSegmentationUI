# Sign Segmentation Validator UI

A simple, user-friendly web interface for sign language community members to verify frame segmentation for atomic and composite signs.

## 🎯 Purpose

This tool allows non-technical sign language community members to:
- View sign language videos with frame-by-frame navigation
- See segmentation information (atomic signs, composite signs, total signs)
- Validate segmentation accuracy
- Provide feedback on segmentation quality

## 🚀 Quick Start

### Option 1: Using Python Server (Recommended)

1. **Start the server:**
   ```bash
   python run_validator_server.py
   ```

2. **Open your browser:**
   - The browser should open automatically
   - Or manually visit: `http://localhost:8000/segmentation_validator.html`

3. **Start validating:**
   - Select a video from the dropdown
   - Review the segmentation
   - Click validation buttons (Correct/Incorrect/Needs Review)
   - Add feedback if needed
   - Click "Save Validation" to download results

### Option 2: Direct File Opening

Simply double-click `segmentation_validator.html` in your file browser. However, this may have limitations loading JSON/video files due to browser security restrictions.

## 📋 Features

### 1. **Progress Table View** (New!)
- **Overview Dashboard**: See all videos at a glance
- **Status Tracking**: 
  - 🟡 Pending - Not yet validated
  - 🟢 Completed - Validated as correct
  - 🔴 Needs Review - Marked as incorrect
  - 🔵 In Progress - Needs review status
- **Statistics**: Shows total signs, atomic signs, and composite signs for each video
- **Comments Indicator**: Shows if feedback has been provided
- **Last Updated**: Timestamp of last validation
- **Search Functionality**: Quickly find videos by name
- **Click to Validate**: Click any row to jump to validation for that video

### 2. **Segmentation Logic Display** (New!)
- **Prominent Logic Section**: Shows the reasoning behind segmentation
- **Context Notes**: Displays notes explaining why segments were marked
- **Component Logic**: For composite signs, shows if components were estimated or verified

### 3. **Segmented Parts Display** (New!)
- **Frame Previews**: Shows key frames (start, middle, end) for each segment
- **Click to Play**: Click any frame preview to play video at that exact frame
- **Toggle View**: Switch between frame previews and full video player
- **Segment-Specific**: Only shows the relevant frames for each segment, not the full video

### 4. **Statistics Dashboard**
- **Total Signs**: Total number of sign segments
- **Atomic Signs**: Number of atomic (single) signs
- **Composite Signs**: Number of composite (multi-part) signs

### 5. **Detailed Segment Cards**
- **Visual Cards**: Each segment in its own card
- **Frame Information**: 
  - Start and end frame numbers
  - Time in seconds
  - Duration in frames and seconds
- **Type Indicators**: Clear visual distinction between atomic and composite
- **Component Breakdown**: For composite signs, shows all component parts with their frame ranges
- **Logic Indicators**: Shows if components were estimated or manually verified

### 6. **Validation Interface**
- Three validation options:
  - ✅ **Correct**: Segmentation is accurate
  - ❌ **Incorrect**: Segmentation has errors
  - ⚠️ **Needs Review**: Requires further attention
- Feedback text area for detailed comments
- **Auto-save**: Validation results saved to browser storage
- **Download Results**: Export all validations as JSON file
- **Progress Updates**: Table automatically updates after validation

### 7. **Tab Navigation**
- Switch between Progress Table and Validation views
- Easy navigation between overview and detailed validation

## 📁 File Structure

```
dhwani5.0/
├── segmentation_validator.html      # Main UI file
├── run_validator_server.py          # Server script
├── outputs/
│   └── manual_annotations_hierarchical.json  # Segmentation data
└── videos/
    └── *.mp4                        # Video files
```

## 💾 Validation Results

### Auto-Save Feature
- Validations are automatically saved to browser's local storage
- Progress persists even if you close the browser
- No need to manually save after each validation

### Export Results
When you click "Save Validation", a JSON file is downloaded with:
- Video ID
- Timestamp
- Validation status (correct/incorrect/needs_review)
- Feedback comments
- Validator identifier

Example output:
```json
{
  "My_Name_Is": [
    {
      "timestamp": "2024-01-15T10:30:00.000Z",
      "status": "correct",
      "feedback": "Segmentation looks accurate. The frame boundaries match the sign transitions perfectly.",
      "validator": "community_member"
    }
  ],
  "12_Twelve": [
    {
      "timestamp": "2024-01-15T11:00:00.000Z",
      "status": "needs_review",
      "feedback": "The transition between 'One' and 'Two' seems to start a bit early. Frame 30 might be better.",
      "validator": "community_member"
    }
  ]
}
```

### Progress Tracking
- The Progress Table shows validation status for all videos
- Status updates immediately after saving validation
- Multiple validations per video are tracked (shows latest status)

## 🎨 Design Principles

The UI is designed with non-technical users in mind:
- **Large, clear buttons** - Easy to click
- **Simple language** - No technical jargon
- **Visual indicators** - Color coding and icons
- **One-page interface** - Everything visible at once
- **Mobile-friendly** - Works on tablets and phones
- **Accessible** - High contrast, readable fonts

## 🔧 Troubleshooting

### Videos not loading?
- Make sure video files exist in the `videos/` directory
- Check that video filenames match the `video_id` in the JSON

### JSON not loading?
- Ensure `outputs/manual_annotations_hierarchical.json` exists
- Use the Python server instead of opening the file directly

### Server won't start?
- Check if port 8000 is already in use
- Make sure Python 3 is installed
- Try a different port by editing `PORT = 8000` in the server script

## 📝 Usage Tips for Validators

1. **Watch the full video first** - Get context before validating
2. **Use frame-by-frame navigation** - Check exact segment boundaries
3. **Check the timeline** - Visual overview helps spot issues
4. **Read the notes** - May contain important context
5. **Provide specific feedback** - Mention which frames or segments have issues
6. **Save frequently** - Don't lose your validation work

## 🤝 Contributing

This tool is designed to gather community feedback to improve sign language recognition. Your validation helps:
- Improve segmentation accuracy
- Better understand sign boundaries
- Enhance the overall recognition system

Thank you for your contribution! 🙏

## 📞 Support

If you encounter any issues or have suggestions for improvement, please contact the development team.
