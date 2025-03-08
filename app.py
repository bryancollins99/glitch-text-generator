from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

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
                                  "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫")
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
            print(f'Error processing image: {e}')
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
            format_type = 'gif'
        else:
            # Save as PNG with maximum quality
            final_image.save(
                buffer,
                format='PNG',
                optimize=False,
                quality=100
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
        print(f'Error downloading image: {e}')
        return jsonify({'error': str(e)}), 500
        
        # For single frame PNG
        if format_type == 'png' or frame_count == 1:
            glitched_image = apply_glitch_effect(image_data, effects)
            
            buffer = BytesIO()
            glitched_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            return send_file(buffer,
                           mimetype='image/png',
                           as_attachment=True,
                           download_name='glitch-image.png')
        
        # For animated GIF
        frames = []
        base_image = None
        
        # Convert base64 to PIL Image
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            base_image = Image.open(BytesIO(image_bytes))
        
        # Generate frames with slightly different effects
        for _ in range(frame_count):
            frame_effects = effects.copy()
            # Vary the effects slightly for each frame
            for key in frame_effects:
                frame_effects[key] = float(frame_effects[key]) * random.uniform(0.8, 1.2)
            
            frame = apply_glitch_effect(base_image, frame_effects)
            frames.append(frame)
        
        # Save as animated GIF
        buffer = BytesIO()
        frames[0].save(
            buffer,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=50,  # 20fps
            loop=0
        )
        buffer.seek(0)
        
        return send_file(buffer,
                       mimetype='image/gif',
                       as_attachment=True,
                       download_name='glitch-image.gif')
                       
    except Exception as e:
        print(f'Error downloading image: {e}')
        return jsonify({'error': str(e)}), 500

        
        # Convert to requested format
        output = io.BytesIO()
        if format_type == 'jpg':
            img.save(output, format='JPEG', quality=95)
            mimetype = 'image/jpeg'
            filename = 'glitch-text.jpg'
        else:  # PNG is default
            img.save(output, format='PNG')
            mimetype = 'image/png'
            filename = 'glitch-text.png'
        
        output.seek(0)
        return send_file(
            output,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
