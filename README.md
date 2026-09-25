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
- **German / English** language toggle
- JavaScript-driven content rendering and interactive image slots

## 💼 Featured Projects

| Project | Description | Tech | Links |
|---|---|---|---|
| **Join** | Kanban task manager: create and organize tasks with drag and drop, assign users and categories. | Angular, TypeScript, Firebase | [Live](https://join-3175.developerakademie.net/index.html) · [GitHub](https://github.com/RudolfSchultz/Join-groupe) |
| **El Pollo Loco** | Object-oriented jump-and-run game: help Pepe collect coins and salsa to beat the crazy hen. | JavaScript (OOP), HTML, CSS | [Live](https://alexander-lindt.developerakademie.net/El-Pollo-Loco/) · [GitHub](https://github.com/alexlindt-arch/El-Pollo-Loco) |
| **DABubble** | Slack clone for teams: channels, direct messages, threads and reactions in real time, with a guest login. | Angular, TypeScript, Firebase | [Live](https://dabubble-3258.developerakademie.net/angular-projects/dabubble/login) · [GitHub](https://github.com/alexlindt-arch/DABubble) |

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
A mirror is served straight from this repository via GitHub Pages:
**[alexlindt-arch.github.io/Portfolio-Lindt-Alexander](https://alexlindt-arch.github.io/Portfolio-Lindt-Alexander/)**

To run it locally instead, clone the repository:

```bash
git clone https://github.com/alexlindt-arch/Portfolio-Lindt-Alexander.git
cd Portfolio-Lindt-Alexander
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
Portfolio-Lindt-Alexander/
├── index.html                 # Main portfolio page (entry)
├── Portfolio Desktop.dc.html  # Desktop layout (loaded by the page runtime)
├── Portfolio Mobile.dc.html   # Mobile layout (loaded by the page runtime)
├── scripts/
│   ├── support.js             # Page runtime + content data
│   └── image-slot.js          # Image slot handling
├── assets/
│   ├── images/                # Portraits, project shots, textures, stickers
│   └── icons/                 # Favicons
├── deploy/                    # Hostinger deploy script + .htaccess block
└── README.md
```

## 👤 Author

**Alexander Lindt** — Freelance Web Designer, Ingolstadt
📧 alexanderlindt16@outlook.de

---

© Alexander Lindt. All rights reserved.
