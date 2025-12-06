# DOUG: A Descent Into Corporate Hell

A static website hosting a short story about Doug, an ordinary guy who accidentally ends up in Hell's bureaucratic nightmare.

## 🔥 Live Site

Once deployed, the site will be available at: `https://[your-username].github.io/Doug/`

## 📁 Project Structure

```
Doug/
├── index.html              # Landing page
├── css/
│   └── style.css           # Cyberpunk + Hellfire themed styles
├── js/
│   └── effects.js          # Visual effects (glitch, typing, parallax)
├── chapters/
│   ├── chapter1.html       # The Arrival
│   └── chapter2.html       # The Situation
└── README.md
```

## 🚀 Deploying to GitHub Pages

### Option 1: Deploy from main branch

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Doug website"
   git branch -M main
   git remote add origin https://github.com/[your-username]/Doug.git
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under "Source", select **Deploy from a branch**
   - Choose **main** branch and **/ (root)** folder
   - Click **Save**

3. **Wait a few minutes** for the site to build and deploy

4. **Access your site** at `https://[your-username].github.io/Doug/`

### Option 2: Using GitHub Actions (automatic)

GitHub Pages will automatically build and deploy when you push to main.

## ✏️ Adding New Chapters

1. Create a new HTML file in the `chapters/` folder (e.g., `chapter3.html`)
2. Copy the structure from an existing chapter file
3. Update the chapter content, title, and navigation links
4. Add a link to the new chapter in:
   - `index.html` (navbar and chapters grid)
   - Previous chapter's "next" navigation button
5. Commit and push your changes

## 🎨 Theme

The site features a **Cyberpunk meets Fire & Brimstone** aesthetic:
- Dark charcoal backgrounds with blood-red accents
- Neon cyan highlights for UI elements
- Glitch effects on titles
- Scanline overlay for retro CRT feel
- Custom fonts: Orbitron (display), Rajdhani (body), Share Tech Mono (code/UI)

## 📜 Story Synopsis

Doug was just a regular guy on his way to work when a freak accident sends him straight to Hell Inc. — a corporate nightmare of eternal bureaucracy. But there's a problem: he arrived with a halo. Now Hell's HR department has a situation on their hands, and Doug is stuck in the middle of an interdimensional filing error.

---

*HELL INC. © ETERNITY | ALL SOULS RESERVED*
