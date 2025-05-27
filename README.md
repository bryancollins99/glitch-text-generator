# Glitch Text Generator

A powerful web application for creating glitch text effects, Zalgo text, cursed text, and various other distorted text styles. Perfect for social media, gaming usernames, creative projects, and adding a unique aesthetic to your digital content.

## 🌟 Features

- **Multiple Text Effects**: Zalgo, ASCII glitch, binary corruption, and more
- **Font Styles**: Cyber, retro, digital, horror, and custom font transformations
- **Image Glitch Effects**: Upload images and apply various glitch effects
- **Real-time Preview**: See your text transform as you type
- **Copy & Paste**: One-click copying for easy use across platforms
- **Mobile Friendly**: Responsive design works on all devices
- **SEO Optimized**: Multiple landing pages for different text effects

## 🚀 Live Demo

Visit the live application: [https://glitchtexteffect.com](https://glitchtexteffect.com)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Gunicorn WSGI server
- **Deployment**: Render (Docker-based)
- **CI/CD**: GitHub Actions

## 📦 Installation & Local Development

### Prerequisites

- Python 3.11 or higher
- Git
- Docker (optional, for containerized development)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bryancollins99/glitch_text_generator.git
   cd glitch_text_generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to `http://localhost:5000`

### Docker Development

1. **Build the Docker image**
   ```bash
   docker build -t glitch-text-generator .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 glitch-text-generator
   ```

3. **Access the application**
   Open your browser and go to `http://localhost:8000`

## 🚀 Deployment

This application is configured for deployment on [Render](https://render.com).

### Quick Deploy to Render

1. Fork this repository
2. Sign up for a Render account
3. Connect your GitHub repository
4. Render will automatically deploy using the included `render.yaml` configuration

### Manual Render Setup

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use these settings:
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Environment Variables**:
     - `FLASK_ENV`: `production`
     - `FLASK_APP`: `app.py`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 📁 Project Structure

```
glitch_text_generator/
├── app.py                 # Main Flask application
├── wsgi.py               # WSGI entry point
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── render.yaml          # Render deployment config
├── gunicorn_config.py   # Gunicorn server config
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── .github/workflows/   # CI/CD workflows
└── README.md           # This file
```

## 🎨 Text Effects Available

### Glitch Effects
- **Zalgo Text**: Classic "cursed" text with diacritical marks
- **ASCII Glitch**: Digital corruption with ASCII characters
- **Binary Corruption**: Random binary and symbol replacement

### Font Styles
- **Cyber**: Futuristic double-struck characters
- **Retro**: Small caps and vintage styling
- **Digital**: Number-like character replacements
- **Horror**: Creepy and unsettling character variants

### Image Effects
- **Color Shift**: RGB channel separation
- **Scanlines**: Retro CRT monitor effect
- **Noise**: Digital static and artifacts
- **Pixel Sort**: Glitched pixel sorting algorithm

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_APP`: Entry point file (default: `app.py`)
- `PORT`: Server port (automatically set by Render)

### Security Features

- Content Security Policy headers
- Input validation and sanitization
- File size limits for image uploads
- Rate limiting (configurable)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Endpoints

### Text Generation
- `POST /api/glitch`: Generate glitch text
  ```json
  {
    "text": "Your text here",
    "effect": "zalgo",
    "intensity": 5,
    "font_style": "cyber"
  }
  ```

### Image Processing
- `POST /download`: Process and download glitched images

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `gunicorn_config.py`
2. **Module not found**: Ensure virtual environment is activated
3. **Docker build fails**: Check Docker is running and has sufficient resources

### Getting Help

- Check the [Issues](https://github.com/bryancollins99/glitch_text_generator/issues) page
- Review the deployment documentation in [DEPLOYMENT.md](DEPLOYMENT.md)
- Check application logs in Render dashboard

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Unicode Consortium for character encoding standards
- Flask community for the excellent web framework
- Render for providing reliable hosting platform

## 📊 SEO & Marketing

The application includes optimized pages for various keywords:
- Cursed text generator
- Zalgo text creator
- Glitch text effects
- Discord and Roblox text formatting
- Social media text styling

Visit any of the specialized pages for targeted text generation experiences.

---

**Made with ❤️ for the creative community**
