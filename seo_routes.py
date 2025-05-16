from flask import Blueprint, render_template

seo_blueprint = Blueprint('seo', __name__)

# Main SEO pages for generator tools
@seo_blueprint.route('/cursed-text')
def cursed_text():
    return render_template('seo/cursed_text.html')

@seo_blueprint.route('/glitch-text')
def glitch_text():
    return render_template('seo/glitch_text.html')

@seo_blueprint.route('/discord-glitch-text')
def discord_glitch_text():
    return render_template('seo/discord_glitch_text.html')

# Informational pages
@seo_blueprint.route('/what-is-glitch-text')
def what_is_glitch_text():
    meta = {
        'page_title': 'What Is Glitch Text? The Complete Guide to Glitched Text Effects',
        'meta_description': 'Learn what glitch text is, how it works, its history, and how to create your own glitched text effects for social media, gaming, and digital art.',
        'meta_keywords': 'glitch text, what is glitch text, corrupted text, zalgo text, glitch effect, text effects',
        'page_url': 'what-is-glitch-text',
        'h1_title': 'What Is Glitch Text? The Complete Guide to Glitched Text Effects',
        'show_toc': True,
        'toc_items': [
            {'id': 'how-glitch-text-works', 'title': 'How Glitch Text Works'},
            {'id': 'types-of-glitch-text', 'title': 'Types of Glitch Text'},
            {'id': 'history-of-glitch-text', 'title': 'The History of Glitch Text'},
            {'id': 'uses-of-glitch-text', 'title': 'Common Uses of Glitch Text'},
            {'id': 'creating-glitch-text', 'title': 'How to Create Glitch Text'},
            {'id': 'platform-compatibility', 'title': 'Platform Compatibility'},
        ],
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/zalgo-text-explained', 'title': 'Zalgo Text Explained'},
            {'url': '/how-to-make-glitch-text', 'title': 'How to Make Glitch Text'},
            {'url': '/glitch-text-examples', 'title': '50+ Glitch Text Examples'},
        ]
    }
    return render_template('seo/what_is_glitch_text.html', **meta)

@seo_blueprint.route('/how-to-make-glitch-text')
def how_to_make_glitch_text():
    meta = {
        'page_title': 'How to Make Glitch Text Online: Step-by-Step Guide',
        'meta_description': 'Learn how to create glitch text online with our easy step-by-step guide. Transform normal text into glitched, corrupted text for social media, usernames, and more.',
        'meta_keywords': 'how to make glitch text, create glitch text, glitch text generator, zalgo text creator, glitch text online',
        'page_url': 'how-to-make-glitch-text',
        'h1_title': 'How to Make Glitch Text Online: Step-by-Step Guide',
        'show_toc': True,
        'toc_items': [
            {'id': 'what-is-glitch-text', 'title': 'What is Glitch Text?'},
            {'id': 'using-our-generator', 'title': 'Using Our Generator'},
            {'id': 'other-methods', 'title': 'Other Methods'},
            {'id': 'tips-for-using', 'title': 'Tips for Using Glitch Text'},
            {'id': 'common-uses', 'title': 'Common Uses'},
            {'id': 'troubleshooting', 'title': 'Troubleshooting'},
        ],
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/what-is-glitch-text', 'title': 'What Is Glitch Text?'},
            {'url': '/zalgo-text-explained', 'title': 'Zalgo Text Explained'},
            {'url': '/glitch-text-examples', 'title': '50+ Glitch Text Examples'},
        ]
    }
    return render_template('seo/how_to_make_glitch_text.html', **meta)

@seo_blueprint.route('/glitch-text-examples')
def glitch_text_examples():
    meta = {
        'page_title': '50+ Glitch Text Examples You Can Copy & Paste',
        'meta_description': 'Browse over 50 glitch text examples you can copy and paste for social media, usernames, bios, and more. From mild to extreme glitch effects.',
        'meta_keywords': 'glitch text examples, zalgo text examples, corrupted text examples, glitch text copy paste',
        'page_url': 'glitch-text-examples',
        'h1_title': '50+ Glitch Text Examples You Can Copy & Paste',
        'show_toc': False,
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/what-is-glitch-text', 'title': 'What Is Glitch Text?'},
            {'url': '/how-to-make-glitch-text', 'title': 'How to Make Glitch Text'},
        ]
    }
    return render_template('seo/glitch_text_examples.html', **meta)

@seo_blueprint.route('/zalgo-text-explained')
def zalgo_text_explained():
    meta = {
        'page_title': 'Zalgo Text: Meaning, History, and How to Use It',
        'meta_description': 'Discover the meaning and history of Zalgo text, how it works technically, and how to create your own corrupted text effects using our generator.',
        'meta_keywords': 'zalgo text, zalgo meaning, corrupted text, glitch text, he comes, zalgo generator',
        'page_url': 'zalgo-text-explained',
        'h1_title': 'Zalgo Text: Meaning, History, and How to Use It',
        'show_toc': True,
        'toc_items': [
            {'id': 'origin-and-etymology', 'title': 'Origin and Etymology'},
            {'id': 'how-zalgo-text-works', 'title': 'How Zalgo Text Works'},
            {'id': 'types-of-zalgo', 'title': 'Types of Zalgo Text Effects'},
            {'id': 'zalgo-in-culture', 'title': 'Zalgo Text in Internet Culture'},
            {'id': 'practical-uses', 'title': 'Practical Uses'},
            {'id': 'limitations', 'title': 'Limitations and Considerations'},
            {'id': 'creating-zalgo', 'title': 'Creating Your Own Zalgo Text'},
        ],
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/what-is-glitch-text', 'title': 'What Is Glitch Text?'},
            {'url': '/creepypasta-explained', 'title': 'Creepypasta Explained'},
            {'url': '/cursed-text-meaning', 'title': 'What Does Cursed Text Mean?'},
        ]
    }
    return render_template('seo/zalgo_text_explained.html', **meta)

@seo_blueprint.route('/creepypasta-explained')
def creepypasta_explained():
    meta = {
        'page_title': 'Creepypasta: Internet Horror Stories & Digital Folklore',
        'meta_description': 'Learn about creepypasta, the internet horror stories that have become digital folklore. Discover famous examples, history, and the connection to glitch text.',
        'meta_keywords': 'creepypasta, internet horror stories, digital folklore, zalgo, slender man, creepypasta examples',
        'page_url': 'creepypasta-explained',
        'h1_title': 'Creepypasta: Internet Horror Stories & Digital Folklore',
        'show_toc': True,
        'toc_items': [
            {'id': 'what-is-creepypasta', 'title': 'What is Creepypasta?'},
            {'id': 'history-of-creepypasta', 'title': 'History and Evolution'},
            {'id': 'types-of-creepypasta', 'title': 'Types of Creepypasta'},
            {'id': 'famous-creepypastas', 'title': 'Famous Creepypasta Stories'},
            {'id': 'creepypasta-and-zalgo', 'title': 'Creepypasta and Zalgo Text'},
            {'id': 'cultural-impact', 'title': 'Cultural Impact'},
            {'id': 'creating-creepypasta', 'title': 'Creating Effective Creepypasta'},
        ],
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/zalgo-text-explained', 'title': 'Zalgo Text Explained'},
            {'url': '/cursed-text-meaning', 'title': 'What Does Cursed Text Mean?'},
        ]
    }
    return render_template('seo/creepypasta_explained.html', **meta)

@seo_blueprint.route('/cursed-text-meaning')
def cursed_text_meaning():
    meta = {
        'page_title': 'What Does Cursed Text Mean? Origins & Usage Explained',
        'meta_description': 'Discover what cursed text means, its origins in internet culture, and how to create your own cursed text effects using our generator.',
        'meta_keywords': 'cursed text meaning, cursed text, zalgo text, corrupted text, creepy text',
        'page_url': 'cursed-text-meaning',
        'h1_title': 'What Does Cursed Text Mean? Origins & Usage Explained',
        'show_toc': False,
        'related_links': [
            {'url': '/cursed-text', 'title': 'Cursed Text Generator'},
            {'url': '/zalgo-text-explained', 'title': 'Zalgo Text Explained'},
            {'url': '/creepypasta-explained', 'title': 'Creepypasta Explained'},
        ]
    }
    return render_template('seo/cursed_text_meaning.html', **meta)

@seo_blueprint.route('/is-glitch-text-safe')
def is_glitch_text_safe():
    meta = {
        'page_title': 'Is Glitch Text Safe to Use? Security & Platform Compatibility',
        'meta_description': 'Learn whether glitch text is safe to use on different platforms, potential security concerns, and best practices for using glitch text responsibly.',
        'meta_keywords': 'is glitch text safe, glitch text security, zalgo text safety, platform compatibility',
        'page_url': 'is-glitch-text-safe',
        'h1_title': 'Is Glitch Text Safe to Use? Security & Platform Compatibility',
        'show_toc': False,
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/what-is-glitch-text', 'title': 'What Is Glitch Text?'},
            {'url': '/how-to-make-glitch-text', 'title': 'How to Make Glitch Text'},
        ]
    }
    return render_template('seo/is_glitch_text_safe.html', **meta)

@seo_blueprint.route('/unicode-glitch-text')
def unicode_glitch_text():
    meta = {
        'page_title': 'Unicode & Glitch Text: How It Works Technically',
        'meta_description': 'A technical explanation of how Unicode is used to create glitch text effects, combining characters, and the technical aspects behind zalgo text.',
        'meta_keywords': 'unicode glitch text, how glitch text works, combining characters, zalgo technical explanation',
        'page_url': 'unicode-glitch-text',
        'h1_title': 'Unicode & Glitch Text: How It Works Technically',
        'show_toc': False,
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/what-is-glitch-text', 'title': 'What Is Glitch Text?'},
            {'url': '/zalgo-text-explained', 'title': 'Zalgo Text Explained'},
        ]
    }
    return render_template('seo/unicode_glitch_text.html', **meta)

@seo_blueprint.route('/glitch-text-generator-review')
def glitch_text_generator_review():
    meta = {
        'page_title': 'The Best Glitch Text Generators (Reviewed)',
        'meta_description': 'A comprehensive review of the best glitch text generators available online, comparing features, ease of use, and output quality.',
        'meta_keywords': 'best glitch text generator, glitch text generator review, zalgo generator comparison',
        'page_url': 'glitch-text-generator-review',
        'h1_title': 'The Best Glitch Text Generators (Reviewed)',
        'show_toc': False,
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/how-to-make-glitch-text', 'title': 'How to Make Glitch Text'},
            {'url': '/glitch-text-examples', 'title': '50+ Glitch Text Examples'},
        ]
    }
    return render_template('seo/glitch_text_generator_review.html', **meta)

@seo_blueprint.route('/how-to-use-glitch-text-on-discord')
def how_to_use_glitch_text_on_discord():
    meta = {
        'page_title': 'How to Use Glitch Text on Discord: Complete Guide',
        'meta_description': 'Learn how to use glitch text on Discord for usernames, messages, channel names, and more. Step-by-step guide with examples and tips.',
        'meta_keywords': 'glitch text discord, discord zalgo text, discord text formatting, discord username glitch',
        'page_url': 'how-to-use-glitch-text-on-discord',
        'h1_title': 'How to Use Glitch Text on Discord: Complete Guide',
        'show_toc': False,
        'related_links': [
            {'url': '/discord-glitch-text', 'title': 'Discord Glitch Text Generator'},
            {'url': '/what-is-glitch-text', 'title': 'What Is Glitch Text?'},
            {'url': '/glitch-text-examples', 'title': '50+ Glitch Text Examples'},
        ]
    }
    return render_template('seo/how_to_use_glitch_text_on_discord.html', **meta)

@seo_blueprint.route('/glitch-fonts-vs-cursed-fonts')
def glitch_fonts_vs_cursed_fonts():
    meta = {
        'page_title': 'Glitch Fonts vs Cursed Fonts: What\'s the Difference?',
        'meta_description': 'Understand the differences between glitch fonts and cursed fonts, their origins, use cases, and how to create each type of effect.',
        'meta_keywords': 'glitch fonts vs cursed fonts, glitch text, cursed text, font differences, text effects comparison',
        'page_url': 'glitch-fonts-vs-cursed-fonts',
        'h1_title': 'Glitch Fonts vs Cursed Fonts: What\'s the Difference?',
        'show_toc': False,
        'related_links': [
            {'url': '/glitch-text', 'title': 'Glitch Text Generator'},
            {'url': '/cursed-text', 'title': 'Cursed Text Generator'},
            {'url': '/what-is-glitch-text', 'title': 'What Is Glitch Text?'},
            {'url': '/cursed-text-meaning', 'title': 'What Does Cursed Text Mean?'},
        ]
    }
    return render_template('seo/glitch_fonts_vs_cursed_fonts.html', **meta)
