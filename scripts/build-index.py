#!/usr/bin/env python3
"""
Scans the scripts/ directory for .fdx and .epub files and regenerates
scripts/index.json with extracted metadata (title, author, episode).

Preserves manual overrides: if an existing entry already has a custom
title/author/episode, those are kept. Removes entries for files that
no longer exist.
"""

import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(SCRIPTS_DIR, 'index.json')


def parse_fdx(path):
    """Extract title/author/episode from an FDX (Final Draft) file."""
    meta = {'title': '', 'author': '', 'episode': ''}
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        title_page = root.find('.//TitlePage')
        if title_page is not None:
            centered = []
            for para in title_page.iter('Paragraph'):
                if para.get('Alignment') == 'Center':
                    texts = [t.text.strip() for t in para.iter('Text') if t.text]
                    if texts:
                        centered.append(' '.join(texts))
            for line in centered:
                if not meta['title']:
                    meta['title'] = line
                elif line.lower().startswith('written by'):
                    continue
                elif not meta['author']:
                    meta['author'] = line
                elif not meta['episode']:
                    meta['episode'] = line
    except Exception as e:
        print(f'  ! FDX parse warning for {os.path.basename(path)}: {e}', file=sys.stderr)
    return meta


def parse_epub(path):
    """Extract title/author from an EPUB file's OPF metadata."""
    meta = {'title': '', 'author': '', 'episode': ''}
    try:
        with zipfile.ZipFile(path) as z:
            # Locate the OPF via container.xml
            container_data = z.read('META-INF/container.xml')
            container_root = ET.fromstring(container_data)
            ns = {'c': 'urn:oasis:names:tc:opendocument:xmlns:container'}
            rootfile = container_root.find('.//c:rootfile', ns)
            if rootfile is None:
                return meta
            opf_path = rootfile.get('full-path')
            opf_data = z.read(opf_path)
            opf_root = ET.fromstring(opf_data)
            dc_ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
            title_el = opf_root.find('.//dc:title', dc_ns)
            creator_el = opf_root.find('.//dc:creator', dc_ns)
            if title_el is not None and title_el.text:
                meta['title'] = title_el.text.strip()
            if creator_el is not None and creator_el.text:
                meta['author'] = creator_el.text.strip()
    except Exception as e:
        print(f'  ! EPUB parse warning for {os.path.basename(path)}: {e}', file=sys.stderr)
    return meta


def humanize_filename(filename):
    """Convert a filename like 'my_script.fdx' into 'My Script'."""
    stem = os.path.splitext(filename)[0]
    cleaned = re.sub(r'[_\-]+', ' ', stem).strip()
    return cleaned.title() if cleaned else filename


def main():
    # Load existing index.json to preserve manual overrides
    existing = {}
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry in data.get('scripts', []):
                    if 'file' in entry:
                        existing[entry['file']] = entry
        except Exception as e:
            print(f'! Could not read existing index.json: {e}', file=sys.stderr)

    # Scan the directory for .fdx and .epub files
    found_files = []
    for name in sorted(os.listdir(SCRIPTS_DIR)):
        lower = name.lower()
        if lower.endswith('.fdx') or lower.endswith('.epub'):
            found_files.append(name)

    print(f'Found {len(found_files)} script file(s) in scripts/')

    # Build updated list
    new_scripts = []
    for filename in found_files:
        full_path = os.path.join(SCRIPTS_DIR, filename)
        prev = existing.get(filename, {})

        # Extract metadata from the file
        if filename.lower().endswith('.fdx'):
            meta = parse_fdx(full_path)
        else:
            meta = parse_epub(full_path)

        # Fall back to humanized filename if no title was extracted
        title = meta['title'] or prev.get('title') or humanize_filename(filename)
        author = meta['author'] or prev.get('author', '')
        episode = meta['episode'] or prev.get('episode', '')

        # Build entry in stable key order
        entry = {'title': title, 'file': filename}
        if author:
            entry['author'] = author
        if episode:
            entry['episode'] = episode
        new_scripts.append(entry)
        print(f'  + {filename} -> "{title}"' + (f' by {author}' if author else ''))

    # Write index.json if content changed
    new_data = {'scripts': new_scripts}
    new_json = json.dumps(new_data, indent=2, ensure_ascii=False) + '\n'

    old_json = ''
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            old_json = f.read()

    if new_json == old_json:
        print('index.json is already up to date.')
        return 0

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_json)
    print(f'Updated index.json with {len(new_scripts)} entr{"y" if len(new_scripts) == 1 else "ies"}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
