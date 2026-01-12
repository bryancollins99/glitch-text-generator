# 🎨 Brand Guidelines - Glitch Text Generator

This document outlines the official brand and styling guidelines for the Glitch Text Generator project. The goal is to maintain a cohesive, professional, and memorable brand identity with a strong **glitch/cyberpunk aesthetic**.

## 1. Core Aesthetic: Cyberpunk Glitch

Our brand is defined by a dark, futuristic, and digital aesthetic. The core elements are:
- **Dark Mode First**: All designs must prioritize a dark theme.
- **Neon Glow**: Use neon colors for highlights, titles, and interactive elements.
- **Digital Glitch**: Incorporate glitch animations and effects subtly.
- **Grid Patterns**: Use grid backgrounds to create a digital, cyberspace feel.
- **Clean & Sharp**: Despite the "glitch" theme, the UI should be clean, sharp, and easy to navigate.

---

## 2. Color Palette

Our color palette is designed for high contrast and a futuristic feel. All colors must have a neon glow effect when used as primary elements.

| Role        | Color                                                              | HEX       | Usage                                                      |
|-------------|--------------------------------------------------------------------|-----------|------------------------------------------------------------|
| **Primary** | <img src="https://via.placeholder.com/20/ff00ff/000000?text=+" /> Magenta  | `#ff00ff` | Titles, main CTAs, borders, primary focus                  |
| **Secondary** | <img src="https://via.placeholder.com/20/00ffff/000000?text=+" /> Cyan     | `#00ffff` | Subtitles, secondary buttons, accents, highlights          |
| **Accent**    | <img src="https://via.placeholder.com/20/00ff00/000000?text=+" /> Green    | `#00ff00` | Success states, special highlights, tertiary elements      |
| **Background**| <img src="https://via.placeholder.com/20/0a0a0a/000000?text=+" /> Dark     | `#0a0a0a` | Main page background                                       |
| **UI BG**   | <img src="https://via.placeholder.com/20/121212/000000?text=+" /> UI Dark  | `#121212` | Card backgrounds, modals, secondary UI elements            |
| **Text**      | <img src="https://via.placeholder.com/20/ffffff/000000?text=+" /> White    | `#ffffff` | Body text, paragraphs, labels                              |

---

## 3. Typography

All text must use **Courier New** monospace font to maintain the cyberpunk aesthetic.

### **Headings & Titles**
- **Font**: Courier New, monospace
- **Color**: `var(--primary)` (#ff00ff)
- **Style**: Bold, uppercase
- **Effects**: Neon glow `text-shadow` and `glitch` animation.
- **Spacing**: `letter-spacing: 3px`

### **Body Text & Paragraphs**
- **Font**: Courier New, monospace
- **Color**: `var(--text)` (#ffffff)
- **Style**: Regular
- **Line Height**: `1.6`

---

## 4. UI Components

### **Buttons**
- **Primary CTA**: Linear gradient `magenta` to `cyan`.
- **Secondary CTA**: Ghost button style with `cyan` border and text.
- **Font**: Courier New, monospace, uppercase, bold.
- **Hover State**: `transform: translateY(-2px)` and intensified neon glow.

### **Cards & Panels**
- **Background**: `rgba(18, 18, 18, 0.9)` with `backdrop-filter: blur(10px)`.
- **Border**: `2px solid var(--primary)`.
- **Box Shadow**: Neon glow `0 0 20px rgba(255, 0, 255, 0.3)`.
- **Hover State**: Border color change to `var(--secondary)` and intensified glow.

### **Backgrounds**
- **Main BG**: `var(--dark)` (#0a0a0a).
- **Pattern**: Linear gradient grid with `rgba(255, 0, 255, 0.1)`.
- **Effects**: Radial gradient glows for atmospheric effect.

---

## 5. Animations & Effects

### **Glitch Title Animation**
All `<h1>` titles must use the standard `glitch` keyframe animation for a consistent, dynamic feel.

```css
@keyframes glitch {
    0%, 100% { transform: translateX(0); }
    10% { transform: translateX(-2px) skew(-1deg); }
    20% { transform: translateX(2px) skew(1deg); }
    30% { transform: translateX(-1px) skew(-0.5deg); }
    40% { transform: translateX(1px) skew(0.5deg); }
    50% { transform: translateX(-1px) skew(-0.2deg); }
    60% { transform: translateX(1px) skew(0.2deg); }
    70% { transform: translateX(0); }
}
```

### **Neon Glow Effect**
Use `box-shadow` and `text-shadow` to create a neon glow on all primary, secondary, and accent colors. The glow should intensify on hover.

**Example:** `text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;`

---

By adhering to these guidelines, we will ensure that the Glitch Text Generator project maintains a strong, consistent, and professional brand identity. All future development and design changes must follow these standards. 