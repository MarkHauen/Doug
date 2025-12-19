#!/usr/bin/env python3
"""
DOUG Story HTMLizer v2
Converts full.txt to styled HTML chapter pages for the Doug website.

Usage:
    python htmlizer.py                    # Process all chapters from full.txt
    python htmlizer.py --chapter 1        # Process specific chapter only
"""

import re
import argparse
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent
CHAPTERS_DIR = BASE_DIR / "chapters"
FULL_TXT = CHAPTERS_DIR / "full.txt"
INDEX_FILE = BASE_DIR / "index.html"

# Chapter metadata - add new chapters here
CHAPTER_META = {
    1: {"title": "The Arrival", "description": "Doug's mundane morning commute takes an unexpected turn into the depths of Hell Inc."},
    2: {"title": "The Situation", "description": "A bureaucratic nightmare unfolds as Hell's HR department discovers a critical filing error."},
    3: {"title": "The Confrence Call", "description": "Floor managers convene as Doug awaits his fate."},
    4: {"title": "The First Meeting", "description": "Doug settles into his temporary accommodations, and has a one-on-one with his new boss."},
    5: {"title": "TBD", "description": "The story continues..."},
    6: {"title": "TBD", "description": "The story continues..."},
}

# Special tag replacements
SCENE_BREAK_HTML = '<div class="scene-break">◆ ◆ ◆</div>'

GNOTE_HTML = '''<div class="gnote-container">
    <div class="gnote">
        <div class="gnote-border"></div>
        <div class="gnote-inner">
            <div class="gnote-left">Love,</div>
            <div class="gnote-right">G</div>
        </div>
        <div class="gnote-shimmer"></div>
    </div>
</div>'''


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
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;700&family=Share+Tech+Mono&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
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
            <p class="copyright">© 2024-2025 Mark Hauenstein. All Rights Reserved.</p>
            <p class="footer-note">This work is protected by copyright. Unauthorized reproduction or distribution is prohibited.</p>
        </div>
    </footer>

    <script src="../js/effects.js"></script>
</body>
</html>
'''


# Allowed inline HTML tags that should be preserved
ALLOWED_INLINE_TAGS = ['strong', 'em', 'b', 'i', 'u', 'mark', 'small', 'sub', 'sup']


def process_line(line: str) -> str | None:
    """Process a single line and return HTML or None if it's a chapter marker."""
    line = line.strip()
    
    if not line:
        return None
    
    # Check for chapter marker - return None to signal chapter break
    if re.match(r'^<Chapter\s+\d+>$', line, re.IGNORECASE):
        return None
    
    # Check for section break
    if line == '<SECTION BREAK>':
        return f'                {SCENE_BREAK_HTML}'
    
    # Check for GNOTE
    if line == '<GNOTE>':
        # Indent each line of the GNOTE HTML
        gnote_lines = GNOTE_HTML.strip().split('\n')
        indented = '\n'.join('                ' + l for l in gnote_lines)
        return indented
    
    # Preserve allowed inline HTML tags by temporarily replacing them
    placeholders = {}
    placeholder_count = 0
    
    for tag in ALLOWED_INLINE_TAGS:
        # Match opening and closing tags
        for pattern in [f'<{tag}>', f'</{tag}>']:
            while pattern in line:
                placeholder = f'__PLACEHOLDER_{placeholder_count}__'
                placeholders[placeholder] = pattern
                line = line.replace(pattern, placeholder, 1)
                placeholder_count += 1
    
    # Escape HTML entities
    line = line.replace('&', '&amp;')
    line = line.replace('<', '&lt;')
    line = line.replace('>', '&gt;')
    
    # Restore allowed tags
    for placeholder, original in placeholders.items():
        line = line.replace(placeholder, original)
    
    # Convert smart quotes to regular quotes
    line = line.replace('"', '"').replace('"', '"')
    line = line.replace(''', "'").replace(''', "'")
    
    return f'                <p>{line}</p>'


def parse_full_txt() -> dict[int, list[str]]:
    """Parse full.txt and return dict of chapter_num -> list of lines."""
    
    if not FULL_TXT.exists():
        raise FileNotFoundError(f"Could not find {FULL_TXT}")
    
    with open(FULL_TXT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by chapter markers
    chapters = {}
    current_chapter = 0
    current_lines = []
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check for chapter marker
        match = re.match(r'^<Chapter\s+(\d+)>$', line, re.IGNORECASE)
        if match:
            # Save previous chapter if exists
            if current_chapter > 0 and current_lines:
                chapters[current_chapter] = current_lines
            
            current_chapter = int(match.group(1))
            current_lines = []
        else:
            current_lines.append(line)
    
    # Don't forget the last chapter
    if current_chapter > 0 and current_lines:
        chapters[current_chapter] = current_lines
    
    return chapters


def count_words(lines: list[str]) -> int:
    """Count words in chapter content (excluding special tags)."""
    word_count = 0
    for line in lines:
        line = line.strip()
        # Skip special tags
        if not line or line.startswith('<'):
            continue
        word_count += len(line.split())
    return word_count


def estimate_read_time(word_count: int, wpm: int = 200) -> str:
    """Estimate reading time based on word count. Average reading speed is ~200-250 wpm."""
    minutes = max(1, round(word_count / wpm))
    return f"~{minutes} min read"


def process_chapter(chapter_num: int, lines: list[str], total_chapters: int) -> int:
    """Process a single chapter into HTML. Returns word count."""
    
    html_path = CHAPTERS_DIR / f"chapter{chapter_num}.html"
    
    # Get chapter metadata
    meta = CHAPTER_META.get(chapter_num, {"title": f"Chapter {chapter_num}", "description": "..."})
    title = meta["title"]
    
    # Count words for read time estimate
    word_count = count_words(lines)
    
    # Convert lines to HTML
    html_parts = []
    for line in lines:
        processed = process_line(line)
        if processed:
            html_parts.append(processed)
    
    content_html = '\n\n'.join(html_parts)
    full_html = get_chapter_html_template(chapter_num, title, content_html, total_chapters)
    
    # Write HTML file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    read_time = estimate_read_time(word_count)
    print(f"  ✓ Chapter {chapter_num}: {title} ({word_count} words, {read_time}) → {html_path.name}")
    return word_count


def update_index_nav(chapter_nums: list[int], word_counts: dict[int, int]):
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
        read_time = estimate_read_time(word_counts.get(num, 0))
        cards_html.append(f'''<a href="chapters/chapter{num}.html" class="chapter-card">
                <div class="chapter-number">{num:02d}</div>
                <div class="chapter-info">
                    <h3>{meta["title"]}</h3>
                    <p>{meta["description"]}</p>
                    <div class="chapter-meta">
                        <span class="read-time">{read_time}</span>
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
    parser = argparse.ArgumentParser(description='Convert Doug story full.txt to HTML chapters')
    parser.add_argument('--chapter', '-c', type=int, help='Process only this chapter number')
    args = parser.parse_args()
    
    print("\n🔥 DOUG HTMLizer v2 - Converting stories to hellish HTML\n")
    
    try:
        chapters = parse_full_txt()
    except FileNotFoundError as e:
        print(f"  ✗ {e}")
        return 1
    
    if not chapters:
        print("  ✗ No chapters found in full.txt")
        print("    Expected format: <Chapter 1> followed by paragraph lines")
        return 1
    
    chapter_nums = sorted(chapters.keys())
    print(f"  Found {len(chapter_nums)} chapter(s): {', '.join(map(str, chapter_nums))}\n")
    
    # Process chapters and collect word counts
    word_counts = {}
    if args.chapter:
        if args.chapter not in chapters:
            print(f"  ✗ Chapter {args.chapter} not found in full.txt")
            return 1
        word_counts[args.chapter] = process_chapter(args.chapter, chapters[args.chapter], len(chapter_nums))
    else:
        for num in chapter_nums:
            word_counts[num] = process_chapter(num, chapters[num], len(chapter_nums))
    
    # Update index
    if not args.chapter:
        print()
        update_index_nav(chapter_nums, word_counts)
    
    print("\n✨ Done! Your souls are ready for deployment.\n")
    return 0


if __name__ == '__main__':
    exit(main())