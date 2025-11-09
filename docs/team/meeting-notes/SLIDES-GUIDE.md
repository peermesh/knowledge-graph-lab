# Meeting Notes → Slides Quick Guide

Convert your meeting notes to browser-viewable slides automatically.

## Quick Start

### 1. Edit Your Meeting Notes

Your markdown file already has Marp formatting. Just edit it normally and save.

### 2. Auto-Update Mode (Recommended)

Start watch mode to auto-regenerate slides on every save:

```bash
.dev/scripts/watch-slides.sh docs/team/meeting-notes/2025-09-29/2025-09-29-standup.md
```

Keep this terminal open. Edit your markdown file and save - slides update automatically!

### 3. One-Time Conversion

```bash
cd docs/team/meeting-notes/2025-09-29/
marp 2025-09-29-standup.md -o 2025-09-29-standup-slides.html
open 2025-09-29-standup-slides.html
```

## Editing Your Slides

### Slide Breaks

Use `---` on its own line to create a new slide:

```markdown
# First Slide

Content here

---

# Second Slide

More content
```

### Adding Images

```markdown
## Module Overview

![Project Diagram](../../images/Knowledge-Graph-Lab.png)
```

### Image Sizing

```markdown
![width:600px](../../images/diagram.png)
![height:400px](../../images/chart.png)
```

### Split Screen

```markdown
![bg right:40%](../../images/diagram.png)

# Content on Left

Your content appears on the left, image on the right
```

## Navigation in Slides

- **Next slide**: Arrow right, Space, or Page Down
- **Previous slide**: Arrow left or Page Up  
- **Full screen**: F key
- **Export to PDF**: Cmd+P in Chrome

## Tips

1. **Keep watch mode running** while editing - slides update instantly
2. **Refresh browser** (Cmd+R) to see changes
3. **One idea per slide** - use `---` to break up long sections
4. **Use emojis** for visual interest (🤖 🛠️ 🎨 📢)
5. **Test before meeting** - open slides in browser to verify

## Front Matter (Already Added)

Your meeting notes already have this configuration at the top:

```markdown
---
marp: true
theme: default
paginate: true
size: 16:9
---
```

You can change:
- `theme:` - try `gaia` or `uncover` for different styles
- `size:` - use `4:3` for classic format
- Colors in the `style:` section

## Troubleshooting

**Slides not updating?**
- Make sure watch mode is still running
- Refresh your browser (Cmd+R)
- Check terminal for errors

**Images not showing?**
- Use relative paths from markdown file location
- Example: `../../images/filename.png`

**Slides look wrong?**
- Ensure `---` separators have blank lines before/after
- Check that front matter is at the very top

## More Examples

See `.dev/slides-output/GRAPHICS-GUIDE.md` for advanced image layouts and styling options.
