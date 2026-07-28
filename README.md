# Alexander Lindt — Portfolio

### 🌐 Live: **[alexanderlindtwebdesign.com](https://alexanderlindtwebdesign.com)**

Personal portfolio website of **Alexander Lindt**, freelance web designer based in Ingolstadt, Germany.

A single-page, statically-served portfolio with a hand-crafted paper/collage visual style — layered paper textures, cut-out stickers, hand-drawn arrows and highlights — showcasing selected client and personal projects.

## ✨ Features

- **Single-page design** with a distinctive paper-collage aesthetic
- **Featured project showcase** (web apps, games, and client sites)
- **Responsive layout** for desktop and mobile
- **Custom typography** via Google Fonts (Bricolage Grotesque, Dancing Script, Sacramento, Kalam)
- **Legal pages** (Imprint / Privacy) rendered from the same page
- JavaScript-driven content rendering and interactive image slots

## 🛠️ Tech Stack

- **HTML5** — semantic page structure (`index.html`)
- **CSS** — inline/component styling with a custom collage design language
- **Vanilla JavaScript** — content rendering and interactions
  - `support.js` — page runtime and content data
  - `image-slot.js` — image slot handling
- **Google Fonts** — web typography

No build step required — it is a static site.

## 🚀 Getting Started

The site is live at **[alexanderlindtwebdesign.com](https://alexanderlindtwebdesign.com)** — no setup needed to view it.
It is also served straight from this repository via GitHub Pages:
**[alexlindt-arch.github.io/portfolio](https://alexlindt-arch.github.io/portfolio/)**

To run it locally instead, clone the repository:

```bash
git clone https://github.com/alexlindt-arch/portfolio.git
cd portfolio
```

Then either open `index.html` directly in a browser, or serve it with any static server:

```bash
# Python
python -m http.server 8000

# Node
npx serve .
```

Visit `http://localhost:8000`.

## 📁 Project Structure

```
portfolio/
├── index.html                 # Main portfolio page (entry)
├── Portfolio Desktop.dc.html  # Desktop layout (loaded by the page runtime)
├── Portfolio Mobile.dc.html   # Mobile layout (loaded by the page runtime)
├── scripts/
│   ├── support.js             # Page runtime + content data
│   └── image-slot.js          # Image slot handling
├── assets/
│   ├── images/                # Portraits, project shots, textures, stickers
│   └── icons/                 # Favicons
└── README.md
```

## 👤 Author

**Alexander Lindt** — Freelance Web Designer, Ingolstadt
📧 alexanderlindt16@outlook.de

---

© Alexander Lindt. All rights reserved.
