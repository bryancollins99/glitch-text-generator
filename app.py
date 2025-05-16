from flask import Flask, render_template, request, jsonify, make_response, send_file, redirect, url_for
import random
import string
from io import BytesIO
import base64
import time
from PIL import Image, ImageDraw
import datetime

app = Flask(__name__)

MAX_IMAGE_SIZE = 1.5 * 1024 * 1024 # Max image size in bytes (1.5MB)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: blob:; script-src 'self' 'unsafe-inline' plausible.io; style-src 'self' 'unsafe-inline'; connect-src 'self' plausible.io;"
    return response

def zalgo(text, intensity=5):
    zalgo_chars = [
        chr(x) for x in range(0x0300, 0x036F + 1)
    ]
    result = ""
    for char in text:
        result += char
        count = int(intensity)
        result += ''.join(random.choice(zalgo_chars) for _ in range(count))
    return result

def ascii_glitch(text, intensity=5):
    glitch_chars = ['̴', '̷', '̶', '̯', '̮', '̭', '̬']
    result = ""
    for char in text:
        result += char
        if random.random() < intensity/10:
            result += random.choice(glitch_chars)
    return result

def binary_corruption(text, intensity=5):
    binary_chars = ['0', '1', '_', '/', '\\', '|', '<', '>', '$']
    result = list(text)
    corruptions = int(len(text) * (intensity/10))
    for _ in range(corruptions):
        pos = random.randint(0, len(text)-1)
        result[pos] = random.choice(binary_chars)
    return ''.join(result)

def apply_text_glitch_effect(text, effect='zalgo', intensity=5):
    if not text:
        return ''
        
    intensity = min(max(int(intensity), 1), 10)
    
    effects = {
        'zalgo': zalgo,
        'ascii': ascii_glitch,
        'binary': binary_corruption,
    }
    
    glitch_func = effects.get(effect, zalgo)
    return glitch_func(text, intensity)

def apply_font_style(text, style='default'):
    font_styles = {
        'cyber': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫")
        },
        'retro': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ")
        },
        'digital': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫")
        },
        'horror': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "ԹՅՇԺȝԲԳɧɿʝƙʅʍՌԾρφՐՏԵՄעաՃՎՀԹՅՇԺȝԲԳɧɿʝƙʅʍՌԾρφՐՏԵՄעաՃՎՀ")
        }
    }
    
    if style in font_styles:
        return text.translate(font_styles[style]['normal'])
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/halloween')
def halloween():
    return render_template('halloween.html')



@app.route('/guides/aesthetic')
def guide_aesthetic():
    return render_template('guides/aesthetic.html')

@app.route('/guides/zalgo')
def guide_zalgo():
    return render_template('guides/zalgo.html')

@app.route('/guides/social')
def guide_social():
    return render_template('guides/social.html')

@app.route('/guides/fonts')
def guide_fonts():
    return render_template('guides/fonts.html')

@app.route('/guides/history')
def guide_history():
    return render_template('guides/history.html')

@app.route('/api/glitch', methods=['POST'])
def glitch():
    try:
        data = request.get_json()
        text = data.get('text', '')
        effect = data.get('effect', 'zalgo')
        intensity = int(data.get('intensity', 5))
        font_style = data.get('font_style', 'default')
        
        # Apply font style first if specified
        if font_style != 'default':
            text = apply_font_style(text, font_style)
        
        # Then apply glitch effect
        glitched_text = apply_text_glitch_effect(text, effect, intensity)
        return jsonify({'result': glitched_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def apply_glitch_effect(image, effects):
    # Convert base64 to PIL Image if needed
    if isinstance(image, str) and image.startswith('data:image'):
        try:
            # Remove the data URL prefix and decode
            image_data = image.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            # Check file size (1.5MB = 1.5 * 1024 * 1024 bytes)
            if len(image_bytes) > MAX_IMAGE_SIZE:
                raise ValueError('Image size must be less than 1.5MB')
                
            image = Image.open(BytesIO(image_bytes))
        except Exception as e:
            app.logger.error(f'Error processing image: {e}')
            raise ValueError('Failed to process image. Please try a different image.')
    
    # Get original size
    width, height = image.size
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Create copy for manipulation
    glitched = image.copy()
    
    # Apply color shift (RGB channel separation)
    if float(effects.get('colorShift', 0)) > 0:
        shift_amount = int(float(effects['colorShift']) * width * 0.01)
        r, g, b = glitched.split()
        r = r.transform(r.size, Image.AFFINE, (1, 0, shift_amount, 0, 1, 0))
        b = b.transform(b.size, Image.AFFINE, (1, 0, -shift_amount, 0, 1, 0))
        glitched = Image.merge('RGB', (r, g, b))
    
    # Apply scanlines
    if float(effects.get('scanlines', 0)) > 0:
        scanline_intensity = int(float(effects['scanlines']) * 2.55)  # 0-255
        scanline_spacing = max(2, int(10 - float(effects['scanlines']) * 0.09))  # More intense = closer lines
        overlay = Image.new('RGB', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for y in range(0, height, scanline_spacing):
            draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=1)
        overlay = overlay.point(lambda x: x * scanline_intensity // 255)
        glitched = Image.blend(glitched, overlay, 0.5)
    
    # Apply noise
    if float(effects.get('noise', 0)) > 0:
        noise_data = []
        noise_factor = float(effects['noise']) * 0.02
        for y in range(height):
            for x in range(width):
                if random.random() < noise_factor:
                    noise_data.append((random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255)))
                else:
                    pixel = glitched.getpixel((x, y))
                    noise_data.append(pixel)
        glitched.putdata(noise_data)
    
    # Apply pixel sorting
    if float(effects.get('pixelSort', 0)) > 0:
        sort_probability = float(effects['pixelSort']) * 0.02
        data = list(glitched.getdata())
        width = glitched.width
        sorted_data = []
        
        for y in range(height):
            row = data[y * width:(y + 1) * width]
            if random.random() < sort_probability:
                # Sort by brightness and create a glitch effect
                brightness = [sum(p) for p in row]
                threshold = sum(brightness) / len(brightness)
                
                # Split row into segments based on brightness
                segments = []
                current_segment = []
                for i, pixel in enumerate(row):
                    if sum(pixel) > threshold or random.random() < 0.1:
                        if current_segment:
                            segments.append(current_segment)
                            current_segment = []
                    current_segment.append(pixel)
                if current_segment:
                    segments.append(current_segment)
                
                # Sort each segment independently
                sorted_row = []
                for segment in segments:
                    if random.random() < 0.7:  # 70% chance to sort segment
                        segment.sort(key=sum, reverse=bool(random.getrandbits(1)))
                    sorted_row.extend(segment)
                sorted_data.extend(sorted_row)
            else:
                sorted_data.extend(row)
        
        glitched.putdata(sorted_data)
    
    return glitched



@app.route('/download', methods=['POST'])
def download_image():
    try:
        data = request.get_json()
        image_data = data.get('image')
        format_type = data.get('format', 'png').lower()
        effects = data.get('effects', {})
        frame_count = int(data.get('frameCount', 1))
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
            
        # Apply effects to create final image
        final_image = apply_glitch_effect(image_data, effects)
        
        # Save to buffer
        buffer = BytesIO()
        
        if format_type == 'gif' and frame_count > 1:
            frames = [final_image]  # First frame is current effect
            
            # Generate additional frames with varying effects
            for _ in range(frame_count - 1):
                frame_effects = effects.copy()
                for key in frame_effects:
                    # Vary effects by ±20%
                    variation = random.uniform(0.8, 1.2)
                    frame_effects[key] = float(frame_effects[key]) * variation
                frame = apply_glitch_effect(image_data, frame_effects)
                frames.append(frame)
            
            # Save as animated GIF
            frames[0].save(
                buffer,
                format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=100,  # Slower animation
                loop=0  # Loop forever
            )
        else:
            # Save as PNG
            final_image.save(
                buffer,
                format='PNG',
                optimize=True
            )
            format_type = 'png'
        
        buffer.seek(0)
        
        # Set filename based on current time to avoid caching
        timestamp = int(time.time())
        filename = f'glitch-image-{timestamp}.{format_type}'
        
        return send_file(
            buffer,
            mimetype=f'image/{format_type}',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        app.logger.error(f'Error downloading image: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/roblox')
def roblox():
    return render_template('roblox.html')

@app.route('/tutorials/photoshop')
def photoshop_tutorial():
    return render_template('photoshop_tutorial.html')

@app.route('/tutorials/after-effects')
def after_effects_tutorial():
    return render_template('after_effects_tutorial.html')

# SEO Pages
SEO_PAGES_DATA = {
    "cursed-text": {
        "title": "Cursed Text Generator - Create Creepy Zalgo Text",
        "meta_description": "Generate cursed text, Zalgo text, and creepy fonts easily. Copy and paste cursed text for social media, gaming, and more.",
        "h1": "Cursed Text Generator",
        "keywords": "cursed text, zalgo text, creepy text, scary text generator",
        "page_content_html": """
            <p>Unleash the power of Zalgo and create truly <strong>cursed text</strong> with our generator. This tool allows you to transform ordinary text into an unsettling, chaotic masterpiece, perfect for adding a touch of horror or mystery to your digital communications. The effect is achieved by stacking numerous diacritical marks above, below, and through your characters, resulting in text that appears corrupted, haunted, or "cursed."</p>
            <p>Whether you're looking to make your social media posts stand out with a creepy vibe, add a unique touch to your gaming profiles, or simply explore the darker side of typography, our cursed text generator is ready. It's simple to use: just type your desired text, adjust the intensity, and watch as it morphs into something wonderfully weird. Get ready to make your words unforgettable... and a little bit scary!</p>
        """
    },
    "cursed-text-copy-paste": {
        "title": "Cursed Text Copy Paste - Easy Zalgo & Creepy Fonts",
        "meta_description": "Copy and paste cursed text effortlessly. Perfect for TikTok, Instagram, Discord, and other platforms. Try our cursed font generator.",
        "h1": "Cursed Text Copy and Paste",
        "keywords": "cursed text copy paste, copy paste cursed font, zalgo copy paste",
        "page_content_html": """
            <p>Need to quickly <strong>copy and paste cursed text</strong>? You're in the right place! Our generator makes it incredibly easy to create unsettling Zalgo text and other creepy font styles, then instantly copy your creation to the clipboard. No complex steps, just type, generate, and paste wherever you need that touch of digital dread.</p>
            <p>This is perfect for spicing up your TikTok comments, Instagram bios, Discord messages, or any online platform where you want to make an impact. The "cursed" effect, with its chaotic and overlapping characters, is sure to grab attention. Try our simple copy-paste function now and start spreading the weirdness!</p>
        """
    },
    "cursed-text-gen": {
        "title": "Cursed Text Gen - Your Ultimate Cursed Font Maker",
        "meta_description": "The best cursed text gen for creating unique and unsettling text styles. Generate and use cursed symbols and fonts in seconds.",
        "h1": "Cursed Text Gen (Generator)",
        "keywords": "cursed text gen, cursed font generator, cursed symbols maker",
        "page_content_html": """
            <p>Welcome to your ultimate <strong>cursed text gen</strong>! This tool is designed to be your go-to cursed font maker, allowing you to craft unique and unsettling text styles with ease. If you're looking to generate text that looks like it's been pulled from a digital abyss or a haunted manuscript, you've found the perfect generator.</p>
            <p>Our cursed text generator provides various levels of intensity, letting you control just how "cursed" your text appears. From subtly unsettling to wildly chaotic, you can create the perfect look. Generate cursed symbols and fonts in mere seconds and use them to make your online presence truly unforgettable.</p>
        """
    },
    "cursed-text-symbols": {
        "title": "Cursed Text Symbols - Find & Use Creepy Characters",
        "meta_description": "Discover a wide array of cursed text symbols and creepy characters. Easily integrate them into your messages and posts.",
        "h1": "Cursed Text Symbols",
        "keywords": "cursed text symbols, creepy symbols, zalgo symbols, scary characters",
        "page_content_html": """
            <p>Dive into the world of <strong>cursed text symbols</strong> and discover a vast collection of creepy characters that can transform your ordinary text. These symbols, often diacritical marks and other special characters, are the building blocks of Zalgo and other "cursed" text effects. Our generator helps you easily combine these to achieve that sought-after unsettling look.</p>
            <p>You don't need to manually hunt for each scary character; our tool does the heavy lifting. Simply input your text, and we'll artfully scatter and stack cursed symbols to create the desired effect. Perfect for adding a touch of horror or the arcane to your digital messages and posts.</p>
        """
    },
    "cursed-text-font": {
        "title": "Cursed Text Font - Spooky & Glitchy Font Styles",
        "meta_description": "Explore various cursed text fonts. Generate scary, glitchy, and weird font styles for your online presence.",
        "h1": "Cursed Text Font Styles",
        "keywords": "cursed text font, scary font, glitch font, creepy typeface",
        "page_content_html": """
            <p>Explore a variety of <strong>cursed text font</strong> styles with our versatile generator. While not a traditional "font" in the installable sense, cursed text creates a unique visual typeface by chaotically combining characters and diacritics. This results in spooky, glitchy, and wonderfully weird font appearances that can make your text pop.</p>
            <p>If you're looking for a scary font to make a statement or a creepy typeface to unnerve your readers, you're in the right place. Generate text that looks like it's decaying, haunted, or digitally corrupted, perfect for themed content or just for fun.</p>
        """
    },
    "weird-symbols-text": {
        "title": "Weird Symbols Text Generator - Create Unique Text",
        "meta_description": "Generate text with weird symbols. Stand out with unique and attention-grabbing text for messages, bios, and posts.",
        "h1": "Weird Symbols Text Generator",
        "keywords": "weird symbols text, unique symbols, strange text generator",
        "page_content_html": """
            <p>Step away from the ordinary with our <strong>weird symbols text generator</strong>! This tool is all about creating unique and attention-grabbing text by incorporating a wide array of strange and unusual symbols into your writing. If you want your messages, bios, or posts to stand out from the crowd, using weird symbols is a fantastic way to do it.</p>
            <p>Our generator makes it easy to sprinkle your text with these unique symbols, transforming plain sentences into something eye-catching and memorable. Explore different combinations and find the perfect level of weirdness for your needs. It's time to make your text as unique as you are!</p>
        """
    },
    "weird-text-messages": {
        "title": "Weird Text Messages - Send Unusual & Funky Texts",
        "meta_description": "Craft weird text messages with our generator. Surprise your friends with unique and unconventional text styles.",
        "h1": "Weird Text Messages",
        "keywords": "weird text messages, funky text, unusual messages generator",
        "page_content_html": """
            <p>Ready to send some truly <strong>weird text messages</strong>? Our generator is here to help you craft funky, unusual, and surprising texts that will make your friends look twice. Move beyond standard emojis and boring fonts, and inject some real character into your communications.</p>
            <p>Whether you want to be playful, mysterious, or just plain odd, our tool provides the means to generate unconventional text styles. Surprise your contacts on WhatsApp, Messenger, or any other platform with messages that are anything but ordinary. Start creating your unique weird texts today!</p>
        """
    },
    "crazy-fonts": {
        "title": "Crazy Fonts Generator - Wild & Unusual Font Styles",
        "meta_description": "Generate crazy fonts for your projects. A wide selection of wild, wacky, and unusual font styles to copy and paste.",
        "h1": "Crazy Fonts Generator",
        "keywords": "crazy fonts, wild fonts, unusual typeface, funky fonts",
        "page_content_html": """
            <p>Unleash your creativity with our <strong>crazy fonts generator</strong>! If you're looking for wild, wacky, and truly unusual font styles, you've come to the perfect place. Our tool allows you to transform your standard text into a variety of funky and eye-catching typefaces that are perfect for making a statement.</p>
            <p>These crazy fonts are ideal for social media posts, creative projects, nicknames, or anywhere you want to inject a bit of fun and personality. Easy to generate and copy-paste, you can start using these wild typefaces in seconds. Let your text go a little crazy!</p>
        """
    },
    "glitch-text-generator": {
        "title": "Glitch Text Generator - Create Cool Glitched Text Effects",
        "meta_description": "Our Glitch Text Generator creates awesome glitched text effects. Easy to use, copy and paste for Roblox, Discord, and more.",
        "h1": "Glitch Text Generator",
        "keywords": "glitch text generator, text glitch, glitched text, glitch effect",
        "page_content_html": """
            <p>Welcome to the ultimate <strong>glitch text generator</strong>! This tool is designed to help you create awesome glitched text effects with ease. If you love the aesthetic of digital corruption, distorted signals, and retro-tech errors, you can now apply that cool vibe to your text. It's perfect for usernames, social media posts, artistic projects, or just for fun.</p>
            <p>Our generator allows you to control the intensity of the glitch, creating everything from subtle distortions to chaotic, unreadable masterpieces. Simply type your text, choose your settings, and watch it transform. Then, copy and paste your glitched text for use on platforms like Roblox, Discord, and beyond!</p>
        """
    },
    "glitch-text": {
        "title": "Glitch Text - Create and Use Glitched Writing",
        "meta_description": "Generate glitch text for your social media, games, or designs. Quick and easy way to get that distorted text effect.",
        "h1": "Glitch Text",
        "keywords": "glitch text, glitched writing, distorted text, text effect",
        "page_content_html": """
            <p>Explore the world of <strong>glitch text</strong> and learn how to create and use this unique distorted writing style. Glitch text mimics the appearance of digital errors, corrupted data, or malfunctioning displays, giving your words a distinct, edgy, and often retro-tech look. It's a popular effect in digital art, music visuals, and online branding.</p>
            <p>With our tool, generating glitched writing is simple. You can easily achieve various levels of distortion to suit your needs, whether for a subtle effect or a completely chaotic appearance. Start creating your own unique glitch text for social media, games, or creative designs today!</p>
        """
    },
    "glitch-text-copy-paste": {
        "title": "Glitch Text Copy and Paste - Quick Glitched Fonts",
        "meta_description": "Easily copy and paste glitch text. Perfect for adding a cool, distorted effect to your online content. Try our glitch font tool.",
        "h1": "Glitch Text Copy and Paste",
        "keywords": "glitch text copy paste, copy paste glitch font, glitched text",
        "page_content_html": """
            <p>Need <strong>glitch text</strong> that you can <strong>copy and paste</strong> in an instant? Our generator is optimized for speed and convenience! Create cool, distorted text effects and immediately copy them to your clipboard for use anywhere online. It's the fastest way to get that glitched font look for your profiles, posts, or messages.</p>
            <p>This tool is perfect for quickly adding a unique, eye-catching touch to your digital content. No fuss, no complicated settings – just generate, copy, and paste. Try our glitch text copy-paste feature now and give your text an edgy, modern vibe!</p>
        """
    },
    "glitch-text-generator-roblox": {
        "title": "Glitch Text Generator for Roblox - Glitched Roblox Names & Chat",
        "meta_description": "Create glitch text for Roblox! Use our generator for glitched usernames, chat messages, and profiles on Roblox.",
        "h1": "Glitch Text Generator for Roblox",
        "keywords": "glitch text generator roblox, roblox glitch text, roblox fonts",
        "page_content_html": """
            <p>Attention Roblox players! Our <strong>glitch text generator for Roblox</strong> is here to help you stand out. Create awesome glitched usernames, eye-catching chat messages, and unique profile descriptions that will make your avatar the talk of the server. Adding a glitch effect to your text is a great way to express your style in the Roblox universe.</p>
            <p>This tool is easy to use: simply type the text you want to glitch, and our generator will create a version perfect for copying and pasting directly into Roblox. Whether you want a subtle distortion or a completely chaotic look for your Roblox text, we've got you covered. Start glitching your Roblox presence today!</p>
        """
    },
    "animated-glitch-text-generator": {
        "title": "Animated Glitch Text Generator - Dynamic Glitching Effects",
        "meta_description": "Generate animated glitch text! (Note: This page describes the effect, actual animation may depend on platform or require GIF generation).",
        "h1": "Animated Glitch Text Generator",
        "keywords": "animated glitch text, glitch animation, dynamic text effect",
        "page_content_html": """
            <p>Explore the exciting concept of an <strong>animated glitch text generator</strong>. While direct text animation is often platform-dependent, our tools can help you create the styles and frames that form the basis of dynamic glitching effects. Imagine text that shimmers, distorts, and reforms, capturing the essence of a true digital glitch in motion!</p>
            <p>You can use our generator to create variations of glitched text that, when sequenced (for example, in a GIF or video), can produce a compelling animated effect. Learn about creating these dynamic text effects and start bringing a new level of energy to your digital designs and messages.</p>
            <p><em>(Note: This site primarily generates static glitch text effects. For creating animated GIFs from images, please see our image glitching tools if available, or use specialized animation software with generated text styles.)</em></p>
        """
    },
    "glitch-text-font": {
        "title": "Glitch Text Font - Distorted & Corrupted Font Styles",
        "meta_description": "Explore a variety of glitch text fonts. Create unique, corrupted, and distorted font styles for any purpose.",
        "h1": "Glitch Text Font",
        "keywords": "glitch text font, distorted font, corrupted font, glitchy typeface",
        "page_content_html": """
            <p>Discover the world of <strong>glitch text font</strong> styles with our generator. This isn't about installing a new font file, but about creating text that embodies the aesthetic of digital corruption and distortion. Think of it as a dynamic, glitchy typeface that you can apply to any string of characters.</p>
            <p>Our tool allows you to generate various distorted and corrupted font styles, perfect for album art, social media profiles, game interfaces, or any project that calls for an edgy, digital-age look. Create unique, memorable text that looks like it's been through a digital meltdown!</p>
        """
    },
    "glitch-text-translator": {
        "title": "Glitch Text Translator - Convert Normal Text to Glitched",
        "meta_description": "Use our glitch text translator to convert your standard text into a cool, glitched-out version. Simple and fast.",
        "h1": "Glitch Text Translator",
        "keywords": "glitch text translator, text to glitch, glitch converter",
        "page_content_html": """
            <p>Welcome to the <strong>glitch text translator</strong>! This simple yet powerful tool allows you to convert your ordinary, plain text into an exciting, glitched-out version. If you've ever wanted to see what your words would look like if they passed through a faulty modem or a corrupted data stream, this is the place to do it.</p>
            <p>Our text-to-glitch converter is fast and easy to use. Just type or paste your standard text, and watch as it gets transformed with a variety of digital distortions. It's perfect for adding a unique flair to your online communications or creative projects.</p>
        """
    },
    "glitch-text-effect": {
        "title": "Glitch Text Effect - Apply Digital Distortion to Text",
        "meta_description": "Easily create a glitch text effect for your digital content. Get that cool, distorted, and corrupted text look.",
        "h1": "Glitch Text Effect",
        "keywords": "glitch text effect, text distortion, digital glitch, corrupted text",
        "page_content_html": """
            <p>Easily apply a striking <strong>glitch text effect</strong> to your digital content with our generator. This popular visual style mimics digital errors, data corruption, and signal interference, giving your text an edgy, modern, and often retro-futuristic vibe. It's a fantastic way to add visual interest and a unique aesthetic to your words.</p>
            <p>Our tool provides you with the controls to create various levels of text distortion, from subtle digital noise to more intense corrupted text looks. Achieve the perfect glitch text effect for your social media, artistic projects, or online branding in just a few clicks.</p>
        """
    },
    "minecraft-glitch-text-generator": {
        "title": "Minecraft Glitch Text Generator - Glitched Text for Minecraft",
        "meta_description": "Generate glitch text for Minecraft! Use for signs, chat, and server messages to get a unique, glitched look.",
        "h1": "Minecraft Glitch Text Generator",
        "keywords": "minecraft glitch text, glitch text minecraft, minecraft fonts",
        "page_content_html": """
            <p>Elevate your Minecraft experience with our <strong>Minecraft glitch text generator</strong>! Want to make your in-game signs, chat messages, or server announcements look uniquely corrupted or digitally disturbed? Our tool helps you create that awesome glitched look quickly and easily.</p>
            <p>Simply type the text you want to use in Minecraft, and our generator will output a glitched version that you can copy and paste directly into the game. Surprise your friends, add flair to your builds, or create a unique theme for your server with custom Minecraft glitch text and fonts.</p>
        """
    },
    "discord-glitch-text": {
        "title": "Discord Glitch Text - Create Glitched Messages for Discord",
        "meta_description": "Make your Discord messages stand out with glitch text. Easy to generate and use in your Discord chats and server.",
        "h1": "Discord Glitch Text",
        "keywords": "discord glitch text, glitch text discord, discord fonts",
        "page_content_html": """
            <p>Make your Discord messages unforgettable with our <strong>Discord glitch text</strong> generator! If you want your text to pop in busy channels or add a unique style to your server's announcements and roles, using glitched text is a fantastic way to do it. Stand out from the crowd and give your Discord communications an edgy, digital vibe.</p>
            <p>Our tool makes it simple: type your message, generate the glitched version, and then copy-paste it directly into your Discord chats or server settings. It's an easy way to enhance your Discord presence with cool and eye-catching text effects.</p>
        """
    },
    "what-is-glitch-text": {
        "title": "What Is Glitch Text? Understanding Digital Distortion",
        "meta_description": "Learn what glitch text is, how it mimics digital errors, its common aesthetics (like Zalgo), and popular uses in art and online communication.",
        "h1": "What Is Glitch Text?",
        "keywords": "what is glitch text, glitch text meaning, digital distortion text, zalgo text, corrupted text",
        "page_content_html": """
            <p><strong>Glitch text</strong> is a style of text that is intentionally distorted to create an aesthetic эффект of digital errors, data corruption, or malfunctioning hardware. It's a visual representation of a \"glitch\" in the digital realm, applied to written words. This can range from subtle visual noise and character misplacement to extreme, chaotic scrambling that renders the text nearly unreadable.</p>
            <p>Common characteristics of glitch text include:</p>
            <ul>
                <li>Overlapping characters</li>
                <li>Unexpected symbols or artifacts mixed with letters</li>
                <li>Strikethroughs, underlines, and overlines appearing erratically</li>
                <li>Use of combining diacritical marks (like in Zalgo text) to create vertical chaos</li>
                <li>A general sense of digital decay or interference</li>
            </ul>
            <p>Glitch text is popular in various forms of digital art, social media (for edgy or humorous effects), online gaming (for unique usernames), and music visuals. It taps into a nostalgia for older technology and the imperfections of the digital age. Our <a href=\"{{ url_for('home') }}\">glitch text generator</a> allows you to easily create these effects for your own use!</p>
        """
    },
    "how-to-make-glitch-text": {
        "title": "How to Make Glitch Text Online (Easy Method)",
        "meta_description": "Discover how to make glitch text online easily using our generator. Transform your text into cool, distorted effects for social media, gaming, and more.",
        "h1": "How to Make Glitch Text Online",
        "keywords": "how to make glitch text, create glitch text, glitch text tutorial, online glitch text generator",
        "page_content_html": """
            <p>Wondering <strong>how to make glitch text</strong>? While manually creating it by meticulously combining Unicode characters can be complex, using an online generator is by far the easiest method. Our tool automates the process, allowing you to create stunning glitch effects in seconds!</p>
            <p>Here's how simple it is with our generator:</p>
            <ol>
                <li><strong>Enter Your Text:</strong> Type or paste the text you want to glitch into the input field on our <a href=\"{{ url_for('home') }}\">generator page</a>.</li>
                <li><strong>Choose Your Effect (Optional):</strong> Select the type of glitch or cursed effect you're aiming for. Some generators offer different styles like Zalgo, corrupted, or ASCII-based glitches.</li>
                <li><strong>Adjust Intensity (Optional):</strong> Many tools, including ours, let you control the intensity of the glitch. You can make it subtle or go for a completely chaotic look.</li>
                <li><strong>Generate:</strong> Click the generate button.</li>
                <li><strong>Copy and Paste:</strong> Your glitched text will appear! Simply copy it and paste it wherever you want – social media, game chats, documents, etc.</li>
            </ol>
            <p>Manually, glitch text is often made by strategically using Unicode combining diacritical marks which stack above, below, or through base characters. However, this requires knowledge of specific Unicode ranges and can be very time-consuming. Our generator handles all that complexity for you, providing instant, customizable results.</p>
        """
    },
    "glitch-text-examples": {
        "title": "50+ Glitch Text Examples You Can Generate & Copy",
        "meta_description": "Explore over 50 types of glitch text examples you can create with our tool. From subtle digital noise to extreme Zalgo, find inspiration and copy paste.",
        "h1": "50+ Glitch Text Examples",
        "keywords": "glitch text examples, zalgo text examples, cursed text examples, copy paste glitch text",
        "page_content_html": """
            <p>Looking for <strong>glitch text examples</strong> to inspire your next creative post or unique username? Our generator can produce a vast array of glitched styles! While we can't list 50+ static examples here (as they are best generated live!), we can describe the types of effects you can achieve and encourage you to experiment with our <a href=\"{{ url_for('home') }}\">glitch text generator</a> to see them all.</p>
            <p>Here are some categories of glitch text examples you can create:</p>
            <ul>
                <li><strong>Subtle Digital Static:</strong> A light scattering of diacritics or minor character misalignments.</li>
                <li><strong>Zalgo-Lite:</strong> Minimal upward or downward character corruption, still readable.</li>
                <li><strong>Heavy Zalgo/Cursed Text:</strong> Extreme vertical distortion with characters appearing to bleed up and down the page.</li>
                <li><strong>Corrupted Characters:</strong> Some letters replaced with random symbols or blocks.</li>
                <li><strong>Interference Lines:</strong> Text with strikethroughs or overlines that mimic signal interference.</li>
                <li><strong>Character Shifting:</strong> Letters slightly offset from their baseline.</li>
                <li><strong>Mixed Intensity:</strong> Text where some words are heavily glitched while others are clearer.</li>
            </ul>
            <p>The best way to see these examples is to use the generator yourself! Type in different words, play with the intensity settings, and try various effect options. You'll quickly discover countless unique combinations that you can copy and paste anywhere.</p>
            <p><strong>Tip:</strong> Try generating your name, a favorite quote, or a call to action to see how different inputs react to the glitching process. You're sure to find more than 50 variations you love!</p>
        """
    },
    "zalgo-text-explained": {
        "title": "Zalgo Text: Meaning, History, and How to Use It",
        "meta_description": "Explore Zalgo text: its meaning, internet creepypasta history, how it's made with Unicode, and how to use our generator to create it.",
        "h1": "Zalgo Text: Meaning, History, and How to Use It",
        "keywords": "zalgo text, what is zalgo, zalgo meaning, zalgo history, cursed text, he comes",
        "page_content_html": """
            <p><strong>Zalgo text</strong> is a specific type of distorted or \"cursed\" text that has gained notoriety online, particularly within internet folklore and creepypasta communities. It's characterized by its chaotic appearance, with text characters seemingly stretching upwards and downwards, often to an extreme degree, by heavily utilizing Unicode's combining diacritical marks.</p>
            <h3>Meaning and History</h3>
            <p>The term \"Zalgo\" is often associated with a demonic or eldritch entity from online horror stories, invoked with phrases like \"He comes.\" The text style is meant to represent the corruption or malevolent influence of this entity. Its origins trace back to internet forums and imageboards around 2004, with a comic strip by Dave Kelly (Shmorky) being a key early popularizer of the visual style and the name.</p>
            <h3>How Zalgo Text is Made</h3>
            <p>Zalgo text is created by adding a large number of combining diacritical marks to base characters. These marks are special Unicode characters (ranging from U+0300 to U+036F and beyond) that are designed to modify preceding characters. When many are stacked, they create the distinctive vertical \"glitching\" or \"bleeding\" effect.</p>
            <h3>How to Use Zalgo Text</h3>
            <p>Zalgo text is used to:</p>
            <ul>
                <li>Create a sense of unease, horror, or chaos.</li>
                <li>Add emphasis or a supernatural feel to text in stories or online posts.</li>
                <li>Make memes or social media comments stand out with a creepy aesthetic.</li>
            </ul>
            <p>You can easily create Zalgo text using our <a href=\"{{ url_for('home') }}\">glitch text generator</a>. Simply type your text, and choose an intensity level that suits your desired level of corruption!</p>
        """
    },
    "cursed-text-meaning": {
        "title": "What Does Cursed Text Mean? Unraveling the Mystery",
        "meta_description": "Understand what cursed text means, its connection to Zalgo and distorted fonts, and why it's used for horror or unsettling digital effects.",
        "h1": "What Does Cursed Text Mean?",
        "keywords": "cursed text meaning, what is cursed text, define cursed text, scary text meaning",
        "page_content_html": """
            <p><strong>Cursed text</strong> generally refers to any text that has been intentionally distorted to appear unsettling, corrupted, chaotic, or difficult to read. It's designed to evoke a sense of unease, digital decay, or even a supernatural or malevolent influence. The term is often used interchangeably with \"Zalgo text,\" which is a specific and well-known style of cursed text.</p>
            <p>The \"meaning\" behind cursed text lies in its visual impact. It aims to:</p>
            <ul>
                <li><strong>Break Readability:</strong> Making text hard to decipher can be intentionally jarring or mysterious.</li>
                <li><strong>Evoke Horror or Dread:</strong> The chaotic, seemingly broken appearance is often used in horror contexts or to give a creepy vibe.</li>
                <li><strong>Signal Corruption:</strong> It can visually represent data corruption, a virus, or a system meltdown.</li>
                <li><strong>Stand Out:</strong> In a sea of plain text, cursed text is undeniably eye-catching.</li>
            </ul>
            <p>Technically, cursed text is usually created by exploiting Unicode features, particularly combining diacritical marks that stack on top of, below, or through standard characters. The more marks are added, the more \"cursed\" the text appears. Our <a href=\"{{ url_for('home') }}\">generator</a> can help you create various styles of cursed text with ease.</p>
        """
    },
    "is-glitch-text-safe": {
        "title": "Is Glitch Text Safe to Use Online? (FAQ)",
        "meta_description": "Addressing safety concerns: Is glitch text safe for your browser, social media, or devices? Generally yes, but with some caveats. Learn more.",
        "h1": "Is Glitch Text Safe to Use?",
        "keywords": "is glitch text safe, glitch text safety, cursed text safe, zalgo text issues, text generator safe",
        "page_content_html": """
            <p>A common question is: <strong>Is glitch text safe to use?</strong> Generally, for the user viewing or generating it, yes, glitch text is safe. It's essentially just a string of Unicode characters that most modern browsers and applications know how to render, albeit in a visually chaotic way.</p>
            
            <h3>Potential Considerations:</h3>
            <ul>
                <li><strong>Rendering Issues & Lag:</strong> Extremely long or complex strings of glitch text (especially those with thousands of combining diacritical marks, like very intense Zalgo text) can sometimes cause performance issues in certain applications or older browsers. This might manifest as lag when typing, scrolling, or rendering the page. This is usually temporary and resolves once the text is removed or the page is reloaded.</li>
                <li><strong>Accessibility:</strong> Glitch text is, by its nature, often difficult or impossible to read for screen readers used by visually impaired individuals. It should be used sparingly in contexts where accessibility is critical, or an alternative plain text version should be provided.</li>
                <li><strong>Character Limits:</strong> Some platforms (like Twitter, or game username fields) have character limits. Since glitch text can use many characters to create its effect, a visually short piece of glitch text might actually be quite long in terms of raw character count and could exceed these limits.</li>
                <li><strong>User Experience:</strong> Overusing glitch text or making essential information unreadable can lead to a poor user experience. Use it thoughtfully.</li>
            </ul>
            <p>Our <a href=\"{{ url_for('home') }}\">glitch text generator</a> aims to create effects that are broadly compatible, but it's always good practice to test your generated text on the platform where you intend to use it, especially if you opt for very high-intensity effects. In summary, while not inherently malicious, extreme glitch text can be resource-intensive for some systems to display.</p>
        """
    },
    "unicode-glitch-text": {
        "title": "Unicode & Glitch Text: How Combining Characters Create Chaos",
        "meta_description": "Learn how Unicode, specifically combining diacritical marks, is the magic behind glitch text and Zalgo effects. An easy explanation.",
        "h1": "Unicode & Glitch Text: How It Works",
        "keywords": "unicode glitch text, combining diacritical marks, unicode characters, how glitch text works, zalgo unicode",
        "page_content_html": """
            <p>The chaotic and distorted appearance of <strong>glitch text</strong> (including styles like Zalgo text) is primarily achieved through the clever use of <strong>Unicode</strong>, specifically a set of characters called <strong>combining diacritical marks</strong>.</p>
            <p>Here's a simplified explanation of how it works:</p>
            <ul>
                <li><strong>Unicode Basics:</strong> Unicode is a universal character encoding standard. It assigns a unique number (a code point) to virtually every character, symbol, or emoji from all writing systems in the world. This allows computers to consistently display and process text from different languages.</li>
                <li><strong>Combining Diacritical Marks:</strong> Within the Unicode standard, there's a special category of characters (typically in the U+0300–U+036F range, but also others) known as combining diacritical marks. These are characters like accents (e.g.,  ́,  ̀,  ̂), tildes (e.g.,  ̃), dots above/below (e.g.,  ̇,  ̣), and various lines and squiggles.</li>
                <li><strong>How They Combine:</strong> Unlike regular characters that take up their own space, combining marks are designed to be non-spacing and modify the *preceding* base character. For example, typing an \"e\" followed by the combining acute accent mark \" ́ \" (U+0301) results in \"é\".</li>
                <li><strong>Creating Glitch/Zalgo Text:</strong> Glitch text generators exploit this by programmatically adding *many* of these combining marks (sometimes dozens or hundreds) to each character in the input text. These marks stack above, below, and through the base characters, creating the signature vertical chaos and overlapping visual noise that defines glitch and Zalgo text.</li>
            </ul>
            <p>So, when you use a <a href=\"{{ url_for('home') }}\">glitch text generator</a>, it's not creating an image or a new font; it's strategically assembling a string of Unicode characters that, when rendered by a browser or application, produce the desired distorted visual effect. The more combining marks used, the more intense the \"glitch\" appears.</p>
        """
    },
    "glitch-text-generator-review": {
        "title": "The Best Glitch Text Generators (Reviewed) - Features to Look For",
        "meta_description": "What makes the best glitch text generator? Our review covers key features like ease of use, customization, and copy-paste functionality.",
        "h1": "Choosing the Best Glitch Text Generator: A Review of Features",
        "keywords": "best glitch text generator, glitch text generator review, top glitch text tools, compare glitch generators",
        "page_content_html": """
            <p>When looking for the <strong>best glitch text generator</strong>, several features can make a big difference in user experience and the quality of the output. While many tools exist, here's a review of what to look for, and how our generator aims to provide these key aspects:</p>
            <ul>
                <li><strong>Ease of Use:</strong> The best generators are intuitive. You should be able to type or paste your text and get results quickly without navigating complex menus. Our tool prioritizes a simple, straightforward interface.</li>
                <li><strong>Customization Options:</strong> While simplicity is good, having control over the intensity and style of the glitch is crucial. Look for generators that offer sliders or options to adjust how chaotic the text becomes. We provide intensity controls for our effects.</li>
                <li><strong>Variety of Effects:</strong> Some users want classic Zalgo, others prefer more subtle digital static, and some might look for ASCII-based glitches. A good generator might offer different modes or styles. Our generator focuses on core glitch and cursed text effects, which cover many popular styles.</li>
                <li><strong>Copy-Paste Functionality:</strong> A one-click copy button is essential for quickly transferring the generated glitch text to social media, games, or other applications. This is a standard feature in our tool.</li>
                <li><strong>Speed and Performance:</strong> The generation process should be fast, even with longer texts or higher intensities. The tool should also not cause significant browser lag. We strive for efficient generation.</li>
                <li><strong>Mobile-Friendliness:</strong> Many users generate text on the go, so a responsive design that works well on mobile devices is a big plus. Our website is designed to be mobile-friendly.</li>
                <li><strong>No Intrusive Ads/Popups:</strong> A clean user experience is important. The best tools avoid bombarding users with excessive advertising.</li>
            </ul>
            <p>Ultimately, the \"best\" generator depends on your specific needs. Our <a href=\"{{ url_for('home') }}\">glitch text generator</a> is designed to be a fast, easy-to-use, and effective tool for creating a wide range of popular glitch and cursed text effects. We encourage you to try it and see how it meets these criteria for your projects!</p>
        """
    },
    "how-to-use-glitch-text-on-discord": {
        "title": "How to Use Glitch Text on Discord (Easy Guide)",
        "meta_description": "Learn how to use glitch text on Discord for chat messages, nicknames, and server names. A simple guide to copy-pasting glitched fonts.",
        "h1": "How to Use Glitch Text on Discord",
        "keywords": "glitch text discord, how to use glitch text discord, discord fonts, cursed text discord, discord glitched messages",
        "page_content_html": """
            <p>Want to spice up your Discord server or messages with some eye-catching <strong>glitch text</strong>? It's easier than you think! Here's a simple guide:</p>
            <ol>
                <li><strong>Generate Your Glitch Text:</strong> First, head over to our <a href=\"{{ url_for('home') }}\">glitch text generator</a>. Type in the text you want to use for your Discord message, nickname, server name, or role name.</li>
                <li><strong>Adjust and Choose:</strong> Play with the intensity settings to get the desired glitch effect. Whether you want something subtly distorted or completely chaotic, you can fine-tune it.</li>
                <li><strong>Copy the Glitched Text:</strong> Once you're happy with the result, use the copy button or manually select and copy the generated glitch text.</li>
                <li><strong>Paste into Discord:</strong>
                    <ul>
                        <li><strong>For Chat Messages:</strong> Simply paste the copied text directly into the chat input field in any Discord channel or direct message and hit send.</li>
                        <li><strong>For Nicknames:</strong> Go to User Settings (the gear icon near your username) > My Account > Edit User Profile > Server Profiles. Select the server where you want to change your nickname, and paste the glitch text into the \"Nickname\" field.</li>
                        <li><strong>For Server Names/Channel Names:</strong> If you have the necessary permissions, you can edit server settings or channel settings and paste the glitch text into the name fields.</li>
                    </ul>
                </li>
            </ol>
            <h3>Important Notes for Discord:</h3>
            <ul>
                <li><strong>Character Limits:</strong> Discord has character limits for nicknames, channel names, and messages. Very intense glitch text can use a lot of Unicode characters, so a short visual string might be too long for Discord's limits. If your text doesn't fit, try reducing the intensity or shortening the input.</li>
                <li><strong>Rendering:</strong> While Discord generally renders Unicode well, extremely complex glitch text might look slightly different across devices or could (rarely) cause minor display quirks for some users. Test it out!</li>
                <li><strong>Readability:</strong> Remember that highly glitched text can be hard to read. Use it appropriately, especially for important information.</li>
            </ul>
            <p>Have fun making your Discord presence uniquely glitched!</p>
        """
    },
    "glitch-fonts-vs-cursed-fonts": {
        "title": "Glitch Fonts vs Cursed Fonts: What's the Difference?",
        "meta_description": "Glitch fonts vs cursed fonts (like Zalgo) - learn the subtle differences and similarities in these distorted text styles and how to generate both.",
        "h1": "Glitch Fonts vs Cursed Fonts: What's the Difference?",
        "keywords": "glitch fonts vs cursed fonts, glitch vs zalgo, cursed text vs glitch text, distorted fonts, text effects comparison",
        "page_content_html": """
            <p>The terms <strong>glitch fonts</strong> (or glitch text) and <strong>cursed fonts</strong> (often referring to Zalgo text) are frequently used interchangeably, as both describe text that is intentionally distorted and visually chaotic. However, there can be subtle distinctions in connotation and common aesthetics:</p>
            
            <h3>Shared Characteristics:</h3>
            <ul>
                <li>Both rely on Unicode combining diacritical marks and other special characters to achieve their effects.</li>
                <li>Both result in text that is difficult to read and visually disruptive.</li>
                <li>Both aim to create an unconventional, eye-catching appearance.</li>
            </ul>
            
            <h3>Glitch Text / Glitch Fonts:</h3>
            <ul>
                <li><strong>Aesthetic:</strong> Often evokes a sense of digital error, data corruption, malfunctioning screens, or retro-tech aesthetics. The distortion might appear more random or like digital \"static.\"</li>
                <li><strong>Common Styles:</strong> Can include character shifting, symbol replacement, strikethroughs, and some degree of Zalgo-like vertical stacking, but might also feature more horizontal displacement or pixelation-like effects (though true pixelation is an image effect, not pure text).</li>
            </ul>
            
            <h3>Cursed Text / Cursed Fonts (including Zalgo):</h3>
            <ul>
                <li><strong>Aesthetic:</strong> Typically leans more towards a horror, supernatural, or demonic theme. The distortion is often more focused on extreme vertical chaos, with characters appearing to \"bleed\" up and down the page.</li>
                <li><strong>Common Styles:</strong> Zalgo text is the quintessential example, with heavy use of combining marks to create towering, terrifying letterforms. The intent is often to be unsettling or creepy.</li>
            </ul>
            
            <h3>Is There a Strict Difference?</h3>
            <p>In practice, the line is very blurry. Many \"glitch text generators\" can produce Zalgo/cursed effects, and vice-versa. The terms often depend more on the user's intent and the specific visual style they are aiming for.</p>
            <p>Our <a href=\"{{ url_for('home') }}\">generator</a> is capable of producing a wide spectrum of these effects. By adjusting the intensity and type of glitch, you can create text that fits either the \"digital error\" vibe of general glitch text or the more overtly \"horrific\" style of cursed/Zalgo text. Experiment to find the perfect distorted look for your needs!</p>
        """
    }
}

# Consolidate similar terms to avoid near-duplicate content issues if possible
# For example, "cursed text copy paste", "cursed text copy and paste", "cursed text copy"
# can all point to a primary "cursed-text-copy-paste" page or a general "cursed-text" page.
# For simplicity here, I'm creating distinct entries based on your list, but consider canonical URLs or redirects for very similar terms.

@app.route('/s/<page_slug>')
def seo_page(page_slug):
    page_data = SEO_PAGES_DATA.get(page_slug)
    if not page_data:
        return redirect(url_for('home'))
    
    current_year = datetime.date.today().year
    return render_template('seo_page.html', 
                           title=page_data['title'], 
                           meta_description=page_data['meta_description'],
                           h1=page_data['h1'],
                           keywords_meta=page_data['keywords'],
                           page_content_html=page_data.get('page_content_html', '<p>Explore our generator to create unique text effects!</p>'), # Pass new content
                           current_year=current_year)

# Generate routes for all SEO pages
for page_key, page_data in SEO_PAGES.items():
    @app.route(f'/{page_data["url"]}')
    def seo_page_route(page_key=page_key):
        page = SEO_PAGES[page_key]
        
        # Get all effects except the primary one
        other_effects = [effect for effect in EFFECTS if effect["value"] != page["primary_effect"]]
        
        return render_template(
            'seo_page.html',
            page_url=page["url"],
            page_title=page["page_title"],
            meta_description=page["meta_description"],
            meta_keywords=page["meta_keywords"],
            h1_title=page["h1_title"],
            subtitle=page["subtitle"],
            primary_effect=page["primary_effect"],
            primary_effect_name=page["primary_effect_name"],
            other_effects=other_effects,
            font_styles=FONTS,
            default_font=page["default_font"],
            default_intensity=page["default_intensity"],
            effect_intensity_label=page["effect_intensity_label"],
            input_placeholder=page["input_placeholder"],
            default_text=page["default_text"],
            output_header=page["output_header"],
            h2_title=page["h2_title"],
            main_content=page["main_content"],
            examples_title=page.get("examples_title", "Examples"),
            examples=page.get("examples", []),
            faq=page.get("faq", []),
            related_pages=page.get("related_pages", [])
        )

@app.route('/sitemap')
def html_sitemap():
    return render_template('sitemap.html')

@app.route('/sitemap.xml')
def sitemap():
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Add home page
    url = ET.SubElement(root, 'url')
    loc = ET.SubElement(url, 'loc')
    loc.text = 'https://glitchtexteffect.com/'
    lastmod = ET.SubElement(url, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    # Add all SEO pages
    for page_key, page_data in SEO_PAGES.items():
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page_data["url"]}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    # Add informational pages
    info_pages = [
        'what-is-glitch-text',
        'how-to-make-glitch-text',
        'zalgo-text-explained',
        'creepypasta-explained'
    ]
    
    for page in info_pages:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    # Add other pages
    other_pages = ['about', 'examples', 'discord', 'roblox']
    for page in other_pages:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    # Convert to string
    xml_string = ET.tostring(root, encoding='utf8', method='xml')
    
    # Create response
    response = make_response(xml_string)
    response.headers['Content-Type'] = 'application/xml'
    
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
