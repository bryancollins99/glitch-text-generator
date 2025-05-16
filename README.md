# Glitch Text Generator

A powerful web application that creates various text and image glitch effects. Perfect for social media, gaming profiles, and creative projects.

Live site: [glitchtexteffect.com](https://glitchtexteffect.com)

## Features

- **Text Effects**:
  - Zalgo (cursed text)
  - ASCII glitch
  - Binary corruption
  - Scanline effect
  - Datamosh compression

- **Font Styles**:
  - Cyberpunk
  - Retro Arcade
  - Digital
  - Horror

- **SEO-Optimized Pages**:
  - Cursed Text Generator
  - Glitch Text Generator
  - Discord Glitch Text
  - And more specialized pages

- **Image Glitching**:
  - Upload and glitch images
  - Multiple effect parameters
  - Download as PNG or animated GIF

## Technology Stack

- **Backend**: Flask (Python 3.11)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker, Nginx, DigitalOcean
- **CI/CD**: Custom deployment script

## Project Structure

```
glitch-text-generator/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── deploy.sh              # Deployment script
├── Dockerfile             # Docker configuration
├── gunicorn_config.py     # Gunicorn WSGI server config
├── requirements.txt       # Python dependencies
├── seo_data.py            # SEO page content
├── seo_routes.py          # SEO route definitions
├── static/                # Static assets (CSS, JS, images)
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── img/               # Images and icons
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── seo_page.html      # Template for SEO pages
│   └── ...                # Other page templates
└── wsgi.py                # WSGI entry point
```

## Local Development

### Prerequisites

- Python 3.11+
- Docker (optional)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/bryancollins99/glitch_text_generator.git
   cd glitch_text_generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Visit `http://localhost:5003` in your browser.

### Docker Development

```bash
docker build -t glitch-text-generator .
docker run -p 8000:8000 glitch-text-generator
```

## Deployment

The application is deployed to a DigitalOcean droplet using Docker and Nginx. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## SEO Strategy

The project implements programmatic SEO with dedicated pages for high-value keywords:

- `/cursed-text` - Cursed text generator
- `/glitch-text` - Glitch text generator
- `/discord-glitch-text` - Discord-specific glitch text

Each page has unique content, meta tags, and examples tailored to the specific keyword.

## License

Copyright © 2025 Bryan Collins. All rights reserved.

## Contact

For questions or support, please contact [your-email@example.com](mailto:your-email@example.com).
