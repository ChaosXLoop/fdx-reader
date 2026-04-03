# FDX Script Reader — PWA Deployment

A reflowable screenplay reader with stylus annotations and sticky notes.
Single HTML file, runs entirely in the browser, works offline after first load.

## Quick Deploy to GitHub Pages (Free, 2 minutes)

1. Go to https://github.com/new and create a new repository
   - Name it something like `fdx-reader`
   - Make it **Public** (required for free GitHub Pages)

2. Upload all the files from this folder:
   - `index.html`
   - `manifest.json`
   - `sw.js`
   - `icons/icon-192.png`
   - `icons/icon-512.png`

3. Go to **Settings → Pages** in your repo
   - Source: **Deploy from a branch**
   - Branch: **main** / root
   - Click **Save**

4. After ~60 seconds your app will be live at:
   `https://YOUR-USERNAME.github.io/fdx-reader/`

## Install on iPad / Tablet

1. Open the URL above in **Safari** on your iPad
2. Tap the **Share** button (box with arrow)
3. Scroll down and tap **Add to Home Screen**
4. Name it "FDX Reader" and tap **Add**
5. The app icon appears on your home screen

It will now launch full-screen like a native app, work offline,
and you can use Apple Pencil or any stylus for annotations.

## Install on Android / Kindle

1. Open the URL in **Chrome**
2. Tap the three-dot menu → **Install app** (or **Add to Home screen**)
3. The app installs and works offline

## File Structure

```
fdx-reader/
├── index.html       ← The entire app (single file)
├── manifest.json    ← PWA manifest (name, icons, display mode)
├── sw.js            ← Service worker (offline caching)
├── icons/
│   ├── icon-192.png ← App icon (home screen)
│   └── icon-512.png ← App icon (splash screen)
└── README.md        ← This file
```

## How It Works

- **Reading**: Open .fdx files, reflowable text, adjustable font size
- **Drawing**: Stylus annotations anchored to paragraphs (D key)
- **Notes**: Word-level sticky notes, collapsible to dots (N key)
- **Save/Load**: Annotations export as .json sidecar files
- **Offline**: Works without internet after first load
