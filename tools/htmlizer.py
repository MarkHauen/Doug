#!/usr/bin/env python3
"""
DOUG Story HTMLizer
Converts .txt chapter files to styled HTML pages for the Doug website.

Usage:
    python htmlizer.py                    # Process all chapters
    python htmlizer.py --chapter 1        # Process specific chapter
    python htmlizer.py --update-index     # Also regenerate index.html nav
"""

import os
import re
import glob
import argparse
from pathlib import Path

# Configuration
CHAPTERS_DIR = Path(__file__).parent.parent / "chapters"
INDEX_FILE = Path(__file__).parent.parent / "index.html"

# Chapter metadata - add new chapters here
CHAPTER_META = {
    1: {"title": "The Arrival", "description": "Doug's mundane morning commute takes an unexpected turn into the depths of Hell Inc."},
    2: {"title": "The Situation", "description": "A bureaucratic nightmare unfolds as Hell's HR department discovers a critical filing error."},
    3: {"title": "The Meeting", "description": "Floor managers convene as Doug awaits his fate."},
    4: {"title": "TBD", "description": "The story continues..."},
    5: {"title": "TBD", "description": "The story continues..."},
}

# Scene break marker - a blank line in the txt will become this
SCENE_BREAK_HTML = '<div class="scene-break">◆ ◆ ◆</div>'


def get_chapter_html_template(chapter_num: int, title: str, content_html: str, total_chapters: int) -> str:
    """Generate the full HTML page for a chapter."""
    
    # Build navigation links
    nav_links = ['<li><a href="../index.html">HOME</a></li>']
    for i in range(1, total_chapters + 1):
        active = ' class="active"' if i == chapter_num else ''
        nav_links.append(f'<li><a href="chapter{i}.html"{active}>CHAPTER {i}</a></li>')
    nav_html = '\n            '.join(nav_links)
    
    # Previous/Next navigation
    if chapter_num == 1:
        prev_nav = '''<a href="../index.html" class="nav-btn">
                <span class="arrow">←</span>
                <span>HOME</span>
            </a>'''
    else:
        prev_nav = f'''<a href="chapter{chapter_num - 1}.html" class="nav-btn">
                <span class="arrow">←</span>
                <span>CHAPTER {chapter_num - 1}</span>
            </a>'''
    
    if chapter_num >= total_chapters:
        next_nav = '''<a href="#" class="nav-btn disabled">
                <span>NEXT CHAPTER</span>
                <span class="arrow">→</span>
            </a>'''
    else:
        next_nav = f'''<a href="chapter{chapter_num + 1}.html" class="nav-btn">
                <span>CHAPTER {chapter_num + 1}</span>
                <span class="arrow">→</span>
            </a>'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter {chapter_num}: {title} | DOUG</title>
    <link rel="stylesheet" href="../css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
</head>
<body>
    <div class="scanlines"></div>
    <div class="noise"></div>
    
    <nav class="navbar">
        <div class="nav-brand glitch" data-text="DOUG">DOUG</div>
        <ul class="nav-links">
            {nav_html}
        </ul>
    </nav>

    <main class="chapter-page">
        <header class="chapter-header">
            <span class="chapter-label">// CHAPTER_{chapter_num:02d}</span>
            <h1 class="chapter-title">{title.upper()}</h1>
        </header>

        <article class="chapter-content">
            <div class="story-text">
{content_html}
            </div>
        </article>

        <nav class="chapter-nav">
            {prev_nav}
            {next_nav}
        </nav>
    </main>

    <footer class="footer">
        <div class="footer-content">
            <p class="copyright">HELL INC. © ETERNITY | ALL SOULS RESERVED</p>
            <p class="footer-note">Employee Handbook Section 7.3.2: Unauthorized reproduction of company materials will result in additional torment.</p>
        </div>
    </footer>

    <script src="../js/effects.js"></script>
</body>
</html>
'''


def txt_to_html_content(txt_content: str) -> str:
    """Convert plain text to HTML paragraphs with scene breaks."""
    
    # Split into paragraphs (double newline or single newline with blank line)
    paragraphs = re.split(r'\n\s*\n', txt_content.strip())
    
    html_parts = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # Check if this is a scene break marker (just whitespace/dashes/asterisks)
        if re.match(r'^[\s\-\*~_=◆•]+$', para) or para in ['---', '***', '===', '* * *']:
            html_parts.append(f'                {SCENE_BREAK_HTML}')
        else:
            # Escape HTML entities
            para = para.replace('&', '&amp;')
            para = para.replace('<', '&lt;')
            para = para.replace('>', '&gt;')
            # Convert quotes for better typography
            para = para.replace('"', '"').replace('"', '"')
            para = para.replace(''', "'").replace(''', "'")
            
            html_parts.append(f'                <p>{para}</p>')
    
    return '\n\n'.join(html_parts)


def find_txt_chapters() -> list[int]:
    """Find all numbered .txt files in the chapters directory."""
    txt_files = glob.glob(str(CHAPTERS_DIR / "*.txt"))
    chapter_nums = []
    
    for txt_file in txt_files:
        filename = os.path.basename(txt_file)
        match = re.match(r'^(\d+)\.txt$', filename)
        if match:
            chapter_nums.append(int(match.group(1)))
    
    return sorted(chapter_nums)


def process_chapter(chapter_num: int, total_chapters: int) -> bool:
    """Process a single chapter txt file into HTML."""
    
    txt_path = CHAPTERS_DIR / f"{chapter_num}.txt"
    html_path = CHAPTERS_DIR / f"chapter{chapter_num}.html"
    
    if not txt_path.exists():
        print(f"  ✗ Chapter {chapter_num}: {txt_path} not found")
        return False
    
    # Read txt content
    with open(txt_path, 'r', encoding='utf-8') as f:
        txt_content = f.read()
    
    # Get chapter metadata
    meta = CHAPTER_META.get(chapter_num, {"title": f"Chapter {chapter_num}", "description": "..."})
    title = meta["title"]
    
    # Convert to HTML
    content_html = txt_to_html_content(txt_content)
    full_html = get_chapter_html_template(chapter_num, title, content_html, total_chapters)
    
    # Write HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"  ✓ Chapter {chapter_num}: {title} → {html_path.name}")
    return True


def update_index_nav(chapter_nums: list[int]):
    """Update the index.html navigation and chapter cards."""
    
    if not INDEX_FILE.exists():
        print("  ✗ index.html not found, skipping nav update")
        return
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Build new nav links
    nav_links = ['<li><a href="index.html" class="active">HOME</a></li>']
    for num in chapter_nums:
        nav_links.append(f'<li><a href="chapters/chapter{num}.html">CHAPTER {num}</a></li>')
    
    new_nav = '\n            '.join(nav_links)
    
    # Replace nav links section
    nav_pattern = r'(<ul class="nav-links">)\s*.*?\s*(</ul>)'
    new_nav_section = f'\\1\n            {new_nav}\n        \\2'
    index_content = re.sub(nav_pattern, new_nav_section, index_content, flags=re.DOTALL)
    
    # Build chapter cards
    cards_html = []
    for num in chapter_nums:
        meta = CHAPTER_META.get(num, {"title": f"Chapter {num}", "description": "..."})
        cards_html.append(f'''<a href="chapters/chapter{num}.html" class="chapter-card">
                <div class="chapter-number">{num:02d}</div>
                <div class="chapter-info">
                    <h3>{meta["title"]}</h3>
                    <p>{meta["description"]}</p>
                    <div class="chapter-meta">
                        <span class="read-time">~10 min read</span>
                        <span class="chapter-status online">ACCESSIBLE</span>
                    </div>
                </div>
                <div class="card-decoration"></div>
            </a>''')
    
    # Add "coming soon" card
    next_chapter = max(chapter_nums) + 1 if chapter_nums else 1
    cards_html.append(f'''<div class="chapter-card locked">
                <div class="chapter-number">{next_chapter:02d}</div>
                <div class="chapter-info">
                    <h3>Coming Soon</h3>
                    <p>The story continues...</p>
                    <div class="chapter-meta">
                        <span class="read-time">??? min read</span>
                        <span class="chapter-status offline">LOCKED</span>
                    </div>
                </div>
                <div class="card-decoration"></div>
            </div>''')
    
    new_cards = '\n            \n            '.join(cards_html)
    
    # Replace chapters grid content
    grid_pattern = r'(<div class="chapters-grid">)\s*.*?\s*(</div>\s*</section>)'
    new_grid_section = f'\\1\n            {new_cards}\n        \\2'
    index_content = re.sub(grid_pattern, new_grid_section, index_content, flags=re.DOTALL)
    
    # Update chapter count stat
    index_content = re.sub(
        r'(<span class="stat-value">)\d+ AVAILABLE(</span>)',
        f'\\g<1>{len(chapter_nums)} AVAILABLE\\2',
        index_content
    )
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"  ✓ Updated index.html with {len(chapter_nums)} chapters")


def main():
    parser = argparse.ArgumentParser(description='Convert Doug story .txt files to HTML')
    parser.add_argument('--chapter', '-c', type=int, help='Process only this chapter number')
    parser.add_argument('--update-index', '-i', action='store_true', help='Also update index.html navigation')
    args = parser.parse_args()
    
    print("\n🔥 DOUG HTMLizer - Converting stories to hellish HTML\n")
    
    # Find all chapter txt files
    chapter_nums = find_txt_chapters()
    
    if not chapter_nums:
        print("  ✗ No chapter .txt files found in chapters/ directory")
        print("    Expected files like: 1.txt, 2.txt, 3.txt, etc.")
        return 1
    
    print(f"  Found {len(chapter_nums)} chapter(s): {', '.join(map(str, chapter_nums))}\n")
    
    # Process chapters
    if args.chapter:
        if args.chapter not in chapter_nums:
            print(f"  ✗ Chapter {args.chapter} not found")
            return 1
        process_chapter(args.chapter, len(chapter_nums))
    else:
        for num in chapter_nums:
            process_chapter(num, len(chapter_nums))
    
    # Update index if requested or processing all
    if args.update_index or not args.chapter:
        print()
        update_index_nav(chapter_nums)
    
    print("\n✨ Done! Your souls are ready for deployment.\n")
    return 0


if __name__ == '__main__':
    exit(main())
