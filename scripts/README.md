# Script Library

Drop `.fdx` or `.epub` files in this folder and push to GitHub — a workflow will automatically regenerate `index.json` with the files' metadata, and they'll appear in the app's "Script Library" section on the landing page.

## Automatic updates

A GitHub Action (`.github/workflows/update-library.yml`) watches this folder and runs `scripts/build-index.py` on every push that adds, removes, or modifies a `.fdx` or `.epub` file. The script:

1. Scans the folder for supported files
2. Extracts **title** and **author** metadata from each file:
   - FDX: parses the `TitlePage` centered paragraphs
   - EPUB: reads `dc:title` and `dc:creator` from the OPF
3. Falls back to a humanized filename if no title is found
4. Writes the result back to `index.json`
5. Commits and pushes the updated file

**To add a script:**
1. Drop the file in this folder
2. `git add`, `git commit`, `git push`
3. Wait ~30 seconds for the Action to run
4. Refresh the app — the new script appears in the library

**To remove a script:**
1. Delete the file from this folder
2. Commit and push — the Action removes it from `index.json` automatically

## Manual overrides

If you want to customize the display title, author, or episode for a file, you can hand-edit `index.json`. The build script preserves any existing fields on entries whose files still exist, so your overrides won't be lost on the next run.

## Running the build script locally

```bash
python3 scripts/build-index.py
```

Requires only the Python 3 standard library — no dependencies.

## index.json format

```json
{
  "scripts": [
    {
      "title": "My Script",
      "file": "my_script.fdx",
      "author": "Jonah",
      "episode": "Pilot"
    }
  ]
}
```

- **title** (required): Display name shown in the library
- **file** (required): Filename relative to this `scripts/` folder
- **author** (optional): Byline shown on the library card
- **episode** (optional): Subtitle shown below the author
