from flask import Flask, render_template, request, jsonify, make_response, send_file, redirect, url_for
import random
import string
from io import BytesIO
import base64
import time
from PIL import Image, ImageDraw
import datetime
import os
import xml.etree.ElementTree as ET
from seo_data import SEO_PAGES, EFFECTS, FONTS
from seo_routes import seo_blueprint

app = Flask(__name__)

# Register the SEO blueprint
app.register_blueprint(seo_blueprint)

MAX_IMAGE_SIZE = 1.5 * 1024 * 1024 # Max image size in bytes (1.5MB)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: blob:; script-src 'self' 'unsafe-inline' plausible.io; style-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; font-src 'self' data: cdnjs.cloudflare.com; connect-src 'self' plausible.io; frame-src youtube.com www.youtube.com;"
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
        },
        'aesthetic': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ")
        },
        'fancy': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "𝓕𝓐𝓝𝓒𝓨𝓛𝓔𝓣𝓣𝓔𝓡𝓢𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃")
        },
        'bubble': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
                                  "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ⓪①②③④⑤⑥⑦⑧⑨")
        },
        'square': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
                                  "🄰🄱🄲🄳🄴🄵🄿🄷🄸🄹🄺🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉0123456789")
        },
        'medieval': {
            'normal': str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                                  "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟")
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

@app.route('/abntoout')
def redirect_about():
    return redirect(url_for('about'))

@app.route('/about/')
def about_trailing_slash():
    return redirect(url_for('about'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/discord')
def discord():
    return render_template('discord.html')

@app.route('/roblox')
def roblox():
    return render_template('roblox.html')

@app.route('/vaporwave')
def vaporwave():
    return render_template('vaporwave.html')

@app.route('/small-caps')
def small_caps():
    return render_template('small_caps.html')

@app.route('/reversed')
def reversed_text():
    return render_template('reversed.html')

@app.route('/mirrored')
def mirrored():
    return render_template('mirrored.html')

@app.route('/animated')
def animated():
    return render_template('animated.html')

@app.route('/large-caps')
def large_caps():
    return render_template('large_caps.html')

@app.route('/title-case')
def title_case():
    return render_template('title_case.html')

@app.route('/sentence-case')
def sentence_case():
    return render_template('sentence_case.html')

@app.route('/cursive')
def cursive():
    return render_template('cursive.html')

@app.route('/italics')
def italics():
    return render_template('italics.html')

@app.route('/gothic')
def gothic():
    return render_template('gothic.html')

@app.route('/cool-text')
def cool_text():
    return render_template('cool_text.html')

@app.route('/freaky')
def freaky():
    return render_template('freaky.html')

@app.route('/color-scheme')
def color_scheme():
    return render_template('color_scheme.html')

@app.route('/graffiti')
def graffiti():
    return render_template('graffiti.html')

@app.route('/random-object')
def random_object():
    return render_template('random_object.html')

@app.route('/dragon-name')
def dragon_name():
    return render_template('dragon_name.html')

@app.route('/tutorials/photoshop')
def photoshop_tutorial():
    return render_template('photoshop_tutorial.html')

@app.route('/tutorials/after-effects')
def after_effects_tutorial():
    return render_template('after_effects_tutorial.html')

# Content Pages
@app.route('/content/glitch-text-generator')
def content_glitch_text_generator():
    return render_template('content/glitch-text-generator.html')

@app.route('/content/minecraft-glitch-text')
def content_minecraft_glitch_text():
    return render_template('content/minecraft-glitch-text.html')

@app.route('/minecraft-color-codes')
def minecraft_color_codes():
    return render_template('content/minecraft-color-codes.html')

@app.route('/minecraft-motd-generator')
def minecraft_motd_generator():
    return render_template('minecraft_motd_generator.html')

@app.route('/minecraft-item-generator')
def minecraft_item_generator():
    return render_template('minecraft_item_generator.html')

@app.route('/content/roblox-glitch-text')
def content_roblox_glitch_text():
    return render_template('content/roblox-glitch-text.html')

@app.route('/content/discord-minecraft-glitch')
def content_discord_minecraft_glitch():
    return render_template('content/discord-minecraft-glitch.html')

@app.route('/content/glitch-art')
def content_glitch_art():
    return render_template('content/glitch-art.html')

@app.route('/content/digital-glitch')
def content_digital_glitch():
    return render_template('content/digital-glitch.html')

@app.route('/content/glitch-text-maker')
def content_glitch_text_maker():
    return render_template('content/glitch-text-maker.html')

@app.route('/content/glitch-text-translator')
def content_glitch_text_translator():
    return render_template('content/glitch-text-translator.html')

@app.route('/content/animated-glitch-text')
def content_animated_glitch_text():
    return render_template('content/animated-glitch-text.html')

@app.route('/content/glitch-texture')
def content_glitch_texture():
    return render_template('content/glitch-texture.html')

@app.route('/content/glitch-computer')
def content_glitch_computer():
    return render_template('content/glitch-computer.html')

@app.route('/content/glitch-definition')
def content_glitch_definition():
    return render_template('content/glitch-definition.html')

@app.route('/content/glitch-design')
def content_glitch_design():
    return render_template('content/glitch-design.html')

@app.route('/content/glitch-effect-after-effects')
def content_glitch_effect_after_effects():
    return render_template('content/glitch-effect-after-effects.html')

@app.route('/content/glitch-effect-online')
def content_glitch_effect_online():
    return render_template('content/glitch-effect-online.html')

@app.route('/content/glitch-meaning')
def content_glitch_meaning():
    return render_template('content/glitch-meaning.html')

@app.route('/content/glitch-painting')
def content_glitch_painting():
    return render_template('content/glitch-painting.html')

@app.route('/content/glitching')
def content_glitching():
    return render_template('content/glitching.html')

@app.route('/content/how-to-make-glitch-art')
def content_how_to_make_glitch_art():
    return render_template('content/how-to-make-glitch-art.html')

@app.route('/content/system-glitch')
def content_system_glitch():
    return render_template('content/system-glitch.html')

# Inspiration Pages
@app.route('/emoticons')
def emoticons():
    return render_template('emoticons.html')

@app.route('/cool-symbols')
def cool_symbols():
    return render_template('cool_symbols.html')

@app.route('/fonts')
def fonts():
    return render_template('fonts.html')

# SEO Pages
SEO_PAGES_DATA = {
    "cursed-text": {
        "title": "Cursed Text Generator - Create Creepy Zalgo Text",
        "meta_description": "👻 FREE Cursed Text Generator! Create creepy zalgo text, cursed fonts & scary letters instantly. Perfect for horror posts & Halloween content. Copy-paste ready!",
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
        "meta_description": "🔮 Best Cursed Text Gen! Create unique cursed fonts, zalgo text & creepy symbols instantly. Ultimate cursed font maker with copy-paste functionality. 100% free!",
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
        "meta_description": "🦇 FREE Cursed Text Font Generator! Create spooky, glitchy & scary font styles instantly. Perfect for horror content & creepy designs. Copy-paste ready fonts!",
        "h1": "Cursed Text Font Styles",
        "keywords": "cursed text font, scary font, glitch font, creepy typeface",
        "page_content_html": """
            <p>Explore a variety of <strong>cursed text font</strong> styles with our versatile generator. While not a traditional "font" in the installable sense, cursed text creates a unique visual typeface by chaotically combining characters and diacritics. This results in spooky, glitchy, and wonderfully weird font appearances that can make your text pop.</p>
            <p>If you're looking for a scary font to make a statement or a creepy typeface to unnerve your readers, you're in the right place. Generate text that looks like it's decaying, haunted, or digitally corrupted, perfect for themed content or just for fun.</p>
        """
    },
    "weird-symbols-text": {
        "title": "Weird Symbols Text Generator - Create Unique Text",
        "meta_description": "🌟 FREE Weird Symbols Text Generator! Create unique text with strange symbols & characters. Stand out with attention-grabbing text for messages & posts!",
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
        "meta_description": "🎪 FREE Crazy Fonts Generator! Create wild, wacky & unusual font styles instantly. Perfect for fun posts & creative projects. Copy-paste ready fonts!",
        "h1": "Crazy Fonts Generator",
        "keywords": "crazy fonts, wild fonts, unusual typeface, funky fonts",
        "page_content_html": """
            <p>Unleash your creativity with our <strong>crazy fonts generator</strong>! If you're looking for wild, wacky, and truly unusual font styles, you've come to the perfect place. Our tool allows you to transform your standard text into a variety of funky and eye-catching typefaces that are perfect for making a statement.</p>
            <p>These crazy fonts are ideal for social media posts, creative projects, nicknames, or anywhere you want to inject a bit of fun and personality. Easy to generate and copy-paste, you can start using these wild typefaces in seconds. Let your text go a little crazy!</p>
        """
    },
    "glitch-text-generator": {
        "title": "Glitch Text Generator - Create Cool Glitched Text Effects",
        "meta_description": "⚡ FREE Glitch Text Generator! Create awesome glitched text effects instantly. Perfect for Roblox, Discord, social media & gaming. Copy-paste ready!",
        "h1": "Glitch Text Generator",
        "keywords": "glitch text generator, text glitch, glitched text, glitch effect",
        "page_content_html": """
            <p>Welcome to the ultimate <strong>glitch text generator</strong>! This tool is designed to help you create awesome glitched text effects with ease. If you love the aesthetic of digital corruption, distorted signals, and retro-tech errors, you can now apply that cool vibe to your text. It's perfect for usernames, social media posts, artistic projects, or just for fun.</p>
            <p>Our generator allows you to control the intensity of the glitch, creating everything from subtle distortions to chaotic, unreadable masterpieces. Simply type your text, choose your settings, and watch it transform. Then, copy and paste your glitched text for use on platforms like Roblox, Discord, and beyond!</p>
        """
    },
    "glitch-text": {
        "title": "Glitch Text Generator - Create Glitched Text Effects",
        "meta_description": "⚡ FREE Glitch Text Generator! Create stunning glitched text effects, corrupted fonts & digital art instantly. Perfect for social media & gaming. Copy-paste ready!",
        "h1": "Glitch Text Generator",
        "keywords": "glitch text generator, glitched text, corrupted text, digital text effects",
        "page_content_html": """
            <p>Transform your ordinary text into mind-bending digital art with our <strong>glitch text generator</strong>. Create stunning glitched effects that look like they've been corrupted by a digital malfunction or passed through a broken screen. Perfect for social media posts, gaming profiles, and creative projects that need an edgy, futuristic aesthetic.</p>
            <p>Our generator uses advanced algorithms to create authentic-looking glitch effects including RGB channel separation, scan line distortion, and digital noise. Simply type your text, adjust the glitch intensity, and watch as your words transform into eye-catching corrupted masterpieces. Copy and paste your glitched text anywhere!</p>
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
        "title": "Glitch Text Generator for Roblox - Cool Fonts & Names",
        "meta_description": "🎮 FREE Roblox Glitch Text Generator! Create cool glitched usernames, chat messages & bios for Roblox. Instant copy-paste, works 100% in-game!",
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
        "title": "Glitch Text Font - Corrupted & Distorted Font Styles",
        "meta_description": "🔤 FREE Glitch Text Font Generator! Create corrupted, distorted & glitchy font styles instantly. Perfect for digital art & creative projects. Copy-paste ready!",
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

@app.route('/sitemap')
def html_sitemap():
    return render_template('sitemap.html', seo_pages=SEO_PAGES_DATA)

@app.route('/sitemap.xml')
def sitemap():
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Add home page
    url = ET.SubElement(root, 'url')
    loc = ET.SubElement(url, 'loc')
    loc.text = 'https://glitchtexteffect.com/'
    lastmod = ET.SubElement(url, 'lastmod')
    lastmod.text = datetime.datetime.now().strftime('%Y-%m-%d')
    changefreq = ET.SubElement(url, 'changefreq')
    changefreq.text = 'weekly'
    priority = ET.SubElement(url, 'priority')
    priority.text = '1.0'
    
    # Add main generator pages
    main_pages = [
        {'url': 'halloween', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': 'discord', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': 'roblox', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': 'vaporwave', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'superscript-text-generator', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'small-caps', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'large-caps', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'title-case', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'sentence-case', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'reversed', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'mirrored', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'animated', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'cursive', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'italics', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'gothic', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'cool-text', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'freaky', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'graffiti', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'minecraft-motd-generator', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'minecraft-item-generator', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'minecraft-color-codes', 'priority': '0.7', 'changefreq': 'weekly'},
        {'url': 'examples', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': 'faq', 'priority': '0.6', 'changefreq': 'monthly'},
        {'url': 'about', 'priority': '0.5', 'changefreq': 'monthly'},
        {'url': 'contact', 'priority': '0.5', 'changefreq': 'monthly'},
    ]
    
    for page in main_pages:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page["url"]}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = page['changefreq']
        priority = ET.SubElement(url, 'priority')
        priority.text = page['priority']
    
    # Add guide pages
    guide_pages = [
        'guides/aesthetic',
        'guides/zalgo', 
        'guides/social',
        'guides/fonts',
        'guides/history'
    ]
    
    for page in guide_pages:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'monthly'
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.7'
    
    # Add tutorial pages
    tutorial_pages = [
        'tutorials/photoshop',
        'tutorials/after-effects'
    ]
    
    for page in tutorial_pages:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'monthly'
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.6'
    
    # Add SEO generator pages from seo_data.py
    for page_key, page_data in SEO_PAGES.items():
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page_data["url"]}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'weekly'
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.8'
    
    # Add SEO informational pages from seo_routes.py
    seo_info_pages = [
        {'url': 'what-is-glitch-text', 'priority': '0.8'},
        {'url': 'how-to-make-glitch-text', 'priority': '0.8'},
        {'url': 'zalgo-text-explained', 'priority': '0.8'},
        {'url': 'creepypasta-explained', 'priority': '0.7'},
        {'url': 'cursed-text-meaning', 'priority': '0.7'},
        {'url': 'is-glitch-text-safe', 'priority': '0.7'},
        {'url': 'unicode-glitch-text', 'priority': '0.7'},
        {'url': 'glitch-text-generator-review', 'priority': '0.6'},
        {'url': 'how-to-use-glitch-text-on-discord', 'priority': '0.7'},
        {'url': 'glitch-fonts-vs-cursed-fonts', 'priority': '0.6'},
    ]
    
    for page in seo_info_pages:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page["url"]}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'monthly'
        priority = ET.SubElement(url, 'priority')
        priority.text = page['priority']
    
    # Add content library pages
    content_pages = [
        {'url': 'content/glitch-text-generator', 'priority': '0.8'},
        {'url': 'content/minecraft-glitch-text', 'priority': '0.8'},
        {'url': 'content/discord-minecraft-glitch', 'priority': '0.7'},
        {'url': 'content/roblox-glitch-text', 'priority': '0.8'},
        {'url': 'content/glitch-art', 'priority': '0.8'},
        {'url': 'content/digital-glitch', 'priority': '0.8'},
        {'url': 'content/glitch-text-maker', 'priority': '0.8'},
        {'url': 'content/glitch-text-translator', 'priority': '0.7'},
        {'url': 'content/animated-glitch-text', 'priority': '0.7'},
        {'url': 'content/glitch-texture', 'priority': '0.7'},
        {'url': 'content/glitch-computer', 'priority': '0.7'},
        {'url': 'content/glitch-definition', 'priority': '0.8'},
        {'url': 'content/glitch-design', 'priority': '0.7'},
        {'url': 'content/glitch-effect-after-effects', 'priority': '0.7'},
        {'url': 'content/glitch-effect-online', 'priority': '0.7'},
        {'url': 'content/glitch-meaning', 'priority': '0.8'},
        {'url': 'content/glitch-painting', 'priority': '0.7'},
        {'url': 'content/glitching', 'priority': '0.7'},
        {'url': 'content/how-to-make-glitch-art', 'priority': '0.8'},
        {'url': 'content/system-glitch', 'priority': '0.7'},
    ]
    
    for page in content_pages:
        url = ET.SubElement(root, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f'https://glitchtexteffect.com/{page["url"]}'
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'weekly'
        priority = ET.SubElement(url, 'priority')
        priority.text = page['priority']
    
    # Convert to string
    xml_string = ET.tostring(root, encoding='utf8', method='xml')
    
    # Create response
    response = make_response(xml_string)
    response.headers['Content-Type'] = 'application/xml'
    
    return response

@app.route('/text-to-image')
def text_to_image():
    return render_template('text_to_image.html')

@app.route('/api/text-to-image', methods=['POST'])
def generate_text_image():
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        data = request.get_json()
        text = data.get('text', '')
        effect = data.get('effect', 'zalgo')
        intensity = int(data.get('intensity', 5))
        font_style = data.get('font_style', 'default')
        
        # Image settings
        bg_color = data.get('bg_color', '#000000')
        text_color = data.get('text_color', '#00ff00')
        width = int(data.get('width', 800))
        height = int(data.get('height', 400))
        font_size = int(data.get('font_size', 48))
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Apply font style first if specified
        if font_style != 'default':
            text = apply_font_style(text, font_style)
        
        # Then apply glitch effect
        glitched_text = apply_text_glitch_effect(text, effect, intensity)
        
        # Create image
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a system font, fallback to default if not available
        try:
            # Try to load a monospace font for better glitch text rendering
            font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.load_default()
                except:
                    font = None
        
        # Calculate text position to center it
        if font:
            bbox = draw.textbbox((0, 0), glitched_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # Estimate size if no font available
            text_width = len(glitched_text) * (font_size * 0.6)
            text_height = font_size
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw the text
        draw.text((x, y), glitched_text, fill=text_color, font=font)
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        # Set filename with timestamp
        timestamp = int(time.time())
        filename = f'glitch-text-{timestamp}.png'
        
        return send_file(
            buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        app.logger.error(f'Error generating text image: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/social-media-templates')
def social_media_templates():
    return render_template('social_media_templates.html')

@app.route('/api/social-media-image', methods=['POST'])
def generate_social_media_image():
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
        import io
        
        data = request.get_json()
        text = data.get('text', '')
        effect = data.get('effect', 'zalgo')
        intensity = int(data.get('intensity', 5))
        font_style = data.get('font_style', 'default')
        
        # Template settings
        template = data.get('template', 'instagram-story')
        bg_color = data.get('bg_color', '#000000')
        text_color = data.get('text_color', '#00ff00')
        bg_pattern = data.get('bg_pattern', 'solid')
        font_size = int(data.get('font_size', 48))
        
        # Social media templates dimensions
        templates = {
            'instagram-story': {'width': 1080, 'height': 1920},
            'instagram-post': {'width': 1080, 'height': 1080},
            'discord-banner': {'width': 960, 'height': 540},
            'youtube-thumbnail': {'width': 1280, 'height': 720},
            'twitter-header': {'width': 1500, 'height': 500},
            'facebook-cover': {'width': 1200, 'height': 630},
            'twitch-overlay': {'width': 1920, 'height': 1080},
            'tiktok-video': {'width': 1080, 'height': 1920},
            'custom': {'width': int(data.get('width', 800)), 'height': int(data.get('height', 400))}
        }
        
        if template not in templates:
            template = 'instagram-story'
        
        width = templates[template]['width']
        height = templates[template]['height']
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Apply font style first if specified
        if font_style != 'default':
            text = apply_font_style(text, font_style)
        
        # Then apply glitch effect
        glitched_text = apply_text_glitch_effect(text, effect, intensity)
        
        # Create base image
        img = Image.new('RGB', (width, height), bg_color)
        
        # Apply background pattern
        if bg_pattern == 'gradient':
            # Create gradient background
            for y in range(height):
                for x in range(width):
                    # Create a diagonal gradient
                    r = int(int(bg_color[1:3], 16) * (1 - (x + y) / (width + height)))
                    g = int(int(bg_color[3:5], 16) * (1 - (x + y) / (width + height)))
                    b = int(int(bg_color[5:7], 16) * (1 - (x + y) / (width + height)))
                    img.putpixel((x, y), (r, g, b))
        
        elif bg_pattern == 'grid':
            # Create grid pattern
            draw = ImageDraw.Draw(img)
            grid_size = 50
            for x in range(0, width, grid_size):
                draw.line([(x, 0), (x, height)], fill='#333333', width=1)
            for y in range(0, height, grid_size):
                draw.line([(0, y), (width, y)], fill='#333333', width=1)
        
        elif bg_pattern == 'noise':
            # Add noise pattern
            import random
            pixels = img.load()
            for y in range(height):
                for x in range(width):
                    if random.random() < 0.1:  # 10% noise
                        noise_val = random.randint(0, 50)
                        r, g, b = pixels[x, y]
                        pixels[x, y] = (
                            min(255, r + noise_val),
                            min(255, g + noise_val),
                            min(255, b + noise_val)
                        )
        
        elif bg_pattern == 'scanlines':
            # Add scanlines effect
            draw = ImageDraw.Draw(img)
            for y in range(0, height, 4):
                draw.line([(0, y), (width, y)], fill='#333333', width=1)
        
        draw = ImageDraw.Draw(img)
        
        # Try to use a system font, fallback to default if not available
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.load_default()
                except:
                    font = None
        
        # Handle multiline text
        lines = glitched_text.split('\n')
        line_height = font_size + 10
        total_text_height = len(lines) * line_height
        
        # Calculate starting position to center text vertically
        start_y = (height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            if font:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
            else:
                text_width = len(line) * (font_size * 0.6)
            
            x = (width - text_width) // 2
            y = start_y + (i * line_height)
            
            # Add text shadow for better readability
            shadow_offset = 2
            draw.text((x + shadow_offset, y + shadow_offset), line, fill='#000000', font=font)
            draw.text((x, y), line, fill=text_color, font=font)
        
        # Add glitch effect overlay if intensity is high
        if intensity > 7:
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Add random glitch bars
            import random
            for _ in range(random.randint(3, 8)):
                bar_height = random.randint(2, 10)
                bar_y = random.randint(0, height - bar_height)
                bar_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100)
                overlay_draw.rectangle([0, bar_y, width, bar_y + bar_height], fill=bar_color)
            
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        # Set filename with template name and timestamp
        timestamp = int(time.time())
        filename = f'{template}-glitch-{timestamp}.png'
        
        return send_file(
            buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        app.logger.error(f'Error generating social media image: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/quick-combine', methods=['POST'])
def quick_combine():
    try:
        data = request.get_json()
        emoticon = data.get('emoticon', '')
        symbol = data.get('symbol', '')
        effect = data.get('effect', 'zalgo')
        intensity = int(data.get('intensity', 5))
        
        # Combine emoticon and symbol
        combined_text = f"{emoticon}{symbol}"
        
        # Apply glitch effect
        glitched_text = apply_text_glitch_effect(combined_text, effect, intensity)
        
        return jsonify({
            'result': glitched_text,
            'original': combined_text,
            'effect': effect,
            'intensity': intensity
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/preset-combinations')
def get_preset_combinations():
    """Get popular preset combinations for the homepage"""
    presets = [
        {'emoticon': '😈', 'symbol': '★', 'effect': 'zalgo', 'intensity': 7, 'name': 'Evil Star'},
        {'emoticon': '🔥', 'symbol': '◆', 'effect': 'binary', 'intensity': 6, 'name': 'Fire Diamond'},
        {'emoticon': '💀', 'symbol': '∞', 'effect': 'zalgo', 'intensity': 8, 'name': 'Death Infinity'},
        {'emoticon': '⚡', 'symbol': '→', 'effect': 'ascii', 'intensity': 5, 'name': 'Lightning Arrow'},
        {'emoticon': '🌟', 'symbol': '✦', 'effect': 'zalgo', 'intensity': 4, 'name': 'Starlight'},
        {'emoticon': '🎭', 'symbol': '◇', 'effect': 'binary', 'intensity': 6, 'name': 'Theater Diamond'},
        {'emoticon': '🔮', 'symbol': '∞', 'effect': 'zalgo', 'intensity': 7, 'name': 'Crystal Ball'},
        {'emoticon': '👁', 'symbol': '∆', 'effect': 'ascii', 'intensity': 8, 'name': 'All-Seeing Eye'},
        {'emoticon': '🌙', 'symbol': '✧', 'effect': 'zalgo', 'intensity': 3, 'name': 'Moonlight'},
        {'emoticon': '🕸', 'symbol': '※', 'effect': 'binary', 'intensity': 9, 'name': 'Spider Web'},
        {'emoticon': '🦇', 'symbol': '♦', 'effect': 'zalgo', 'intensity': 6, 'name': 'Bat Wing'},
        {'emoticon': '🔥', 'symbol': '∑', 'effect': 'ascii', 'intensity': 7, 'name': 'Fire Sum'}
    ]
    
    # Generate the glitched versions
    for preset in presets:
        combined_text = f"{preset['emoticon']}{preset['symbol']}"
        glitched_text = apply_text_glitch_effect(combined_text, preset['effect'], preset['intensity'])
        preset['glitched'] = glitched_text
        preset['original'] = combined_text
    
    return jsonify(presets)

@app.route('/superscript-text-generator')
def superscript():
    return render_template('superscript.html')

@app.route('/vaporwave-text-generator')
def vaporwave():
    return render_template('vaporwave.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, host='0.0.0.0', port=port)
