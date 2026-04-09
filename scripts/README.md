# Script Library

Drop `.fdx` or `.epub` files in this folder and register them in `index.json` to make them available from the app's "Script Library" section on the landing page.

## index.json format

```json
{
  "scripts": [
    {
      "title": "My Script",
      "file": "my_script.fdx",
      "author": "Jonah",
      "episode": "Pilot"
    },
    {
      "title": "Another Episode",
      "file": "another.epub",
      "author": "Jonah"
    }
  ]
}
```

- **title** (required): Display name shown in the library
- **file** (required): Filename relative to this `scripts/` folder
- **author** (optional): Byline shown in the library card
- **episode** (optional): Subtitle shown below the author

Supported file types: `.fdx` (Final Draft) and `.epub` (EPUBs exported by this app).
