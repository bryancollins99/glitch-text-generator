"""
SEO data module for programmatic SEO pages.
This file contains the content and metadata for each SEO page.
"""

# Define the effects and fonts for the generator
EFFECTS = [
    {"value": "zalgo", "name": "Zalgo Text (Corrupted Diacritics)"},
    {"value": "ascii", "name": "Glitchy ASCII Art"},
    {"value": "binary", "name": "Binary Corruption"},
    {"value": "scanline", "name": "CRT Scanline Effect"},
    {"value": "datamosh", "name": "Datamosh Compression"}
]

FONTS = [
    {"value": "cyber", "name": "Cyberpunk"},
    {"value": "retro", "name": "Retro Arcade"},
    {"value": "digital", "name": "Digital"},
    {"value": "horror", "name": "Horror"}
]

# SEO pages data
SEO_PAGES = {
    "cursed-text": {
        "url": "cursed-text",
        "page_title": "Cursed Text Generator - Create Creepy Glitched Text",
        "meta_description": "Create cursed text with our free online generator. Perfect for social media, gaming profiles, and creepy content. Copy and paste cursed text easily.",
        "meta_keywords": "cursed text, cursed text generator, creepy text, glitch text",
        "canonical_url": "https://glitchtexteffect.com/cursed-text",
        "h1_title": "Cursed Text Generator",
        "subtitle": "Create creepy, corrupted text that will unsettle your friends. Perfect for horror-themed content, scary stories, and spooky social media posts.",
        "primary_effect": "zalgo",
        "primary_effect_name": "Zalgo (Cursed Effect)",
        "default_font": "horror",
        "default_intensity": "7",
        "effect_intensity_label": "Curse Intensity",
        "input_placeholder": "Enter text to curse...",
        "default_text": "The void stares back",
        "output_header": "Cursed Output",
        "h2_title": "What is Cursed Text?",
        "main_content": "<p>Cursed text is a style of text that appears corrupted, glitched, or 'haunted' using special Unicode characters that stack above and below normal letters. This creates an unsettling, creepy effect that makes text appear to be glitching or possessed.</p><p>Our cursed text generator uses the Zalgo text effect, which adds random combining diacritical marks to standard characters. The result is text that appears to be corrupted or 'cursed' - perfect for creating an eerie atmosphere in your online content.</p>",
        "examples_title": "Cursed Text Examples",
        "examples": [
            {
                "title": "Mild Curse",
                "text": "T̶h̶e̶ ̶v̶o̶i̶d̶ ̶w̶a̶t̶c̶h̶e̶s̶",
                "original": "The void watches"
            },
            {
                "title": "Medium Curse",
                "text": "D̷o̷n̷'̷t̷ ̷l̷o̷o̷k̷ ̷b̷e̷h̷i̷n̷d̷ ̷y̷o̷u̷",
                "original": "Don't look behind you"
            },
            {
                "title": "Heavy Curse",
                "text": "H̴̢̧̛̭̣̖̙̙̞̩̖̰̓̈́̀̓̓̈́̌̈́͘͝ͅE̵̢̡̛̱̰̯̱̣̞̙͖̠̓̈́̀̓̓̈́̌̈́͘͝ ̴̢̧̛̭̣̖̙̙̞̩̖̰̓̈́̀̓̓̈́̌̈́͘͝C̵̢̡̛̱̰̯̱̣̞̙͖̠̓̈́̀̓̓̈́̌̈́͘͝Ơ̴̢̧̭̣̖̙̙̞̩̖̰̓̈́̀̓̓̈́̌̈́͘͝M̵̢̡̛̱̰̯̱̣̞̙͖̠̓̈́̀̓̓̈́̌̈́͘͝Ḙ̴̢̧̛̣̖̙̙̞̩̖̰̓̈́̀̓̓̈́̌̈́͘͝S̵̢̡̛̱̰̯̱̣̞̙͖̠̓̈́̀̓̓̈́̌̈́͘͝",
                "original": "HE COMES"
            }
        ],
        "faq": [
            {
                "question": "How do I copy and paste cursed text?",
                "answer": "Simply click the 'Copy' button next to your cursed text output, or use the 'Copy to Clipboard' button. Then paste it anywhere you want to use it - social media, messaging apps, or gaming platforms."
            },
            {
                "question": "Will cursed text work everywhere?",
                "answer": "Cursed text uses Unicode characters that work on most modern platforms including Discord, Twitter, Instagram, and most messaging apps. Some platforms may limit the intensity of the effect by removing excessive diacritical marks."
            },
            {
                "question": "Can I use cursed text in my username?",
                "answer": "Many platforms restrict the use of special characters in usernames. Discord allows some cursed text in usernames but with limitations. Experiment with lower intensity settings for better compatibility."
            }
        ],
        "related_pages": [
            {"route": "glitch_text", "title": "Glitch Text Generator"},
            {"route": "discord_text", "title": "Discord Text Effects"},
            {"route": "zalgo_text", "title": "Zalgo Text Generator"}
        ]
    },
    "glitch-text": {
        "url": "glitch-text",
        "page_title": "Glitch Text Generator - Create Distorted Text Effects",
        "meta_description": "Transform your text with our free glitch text generator. Create corrupted, distorted text for social media, gaming, and creative projects.",
        "meta_keywords": "glitch text, glitch text generator, distorted text, text effects",
        "canonical_url": "https://glitchtexteffect.com/glitch-text",
        "h1_title": "Glitch Text Generator",
        "subtitle": "Create digital distortion effects for your text. Perfect for cyberpunk aesthetics, digital art, and standing out on social media.",
        "primary_effect": "ascii",
        "primary_effect_name": "ASCII Glitch",
        "default_font": "cyber",
        "default_intensity": "5",
        "effect_intensity_label": "Glitch Intensity",
        "input_placeholder": "Enter text to glitch...",
        "default_text": "Glitch Aesthetic",
        "output_header": "Glitched Output",
        "h2_title": "What is Glitch Text?",
        "main_content": "<p>Glitch text is a style that mimics digital corruption or errors, creating a distorted, broken appearance. This aesthetic has become popular in cyberpunk, vaporwave, and digital art communities.</p><p>Our glitch text generator lets you create various types of digital distortion effects that you can copy and paste anywhere. It's perfect for creating unique usernames, social media posts, or digital art projects.</p>",
        "examples_title": "Glitch Text Examples",
        "examples": [
            {
                "title": "Subtle Glitch",
                "text": "G̷l̷i̷t̷c̷h̷ ̷A̷e̷s̷t̷h̷e̷t̷i̷c̷",
                "original": "Glitch Aesthetic"
            },
            {
                "title": "Medium Distortion",
                "text": "D̸i̸g̸i̸t̸a̸l̸ ̸C̸o̸r̸r̸u̸p̸t̸i̸o̸n̸",
                "original": "Digital Corruption"
            },
            {
                "title": "Heavy Glitch",
                "text": "B̵̧̩̭̣̖̙̙̞̩̖̰͂̓̈́̀̓̓̈́̌̈́͘͝Ṟ̵̢̡̛̰̯̱̣̞̙͖̠͂̓̈́̀̓̓̈́̌̈́͘͝Ơ̴̢̧̭̣̖̙̙̞̩̖̰͂̓̈́̀̓̓̈́̌̈́͘͝Ḵ̵̢̡̛̰̯̱̣̞̙͖̠͂̓̈́̀̓̓̈́̌̈́͘͝Ȩ̴̢̧̛̣̖̙̙̞̩̖̰͂̓̈́̀̓̓̈́̌̈́͘͝Ṉ̵̢̡̛̰̯̱̣̞̙͖̠͂̓̈́̀̓̓̈́̌̈́͘͝",
                "original": "BROKEN"
            }
        ],
        "faq": [
            {
                "question": "How can I use glitch text on social media?",
                "answer": "Simply generate your glitched text, copy it using the copy button, and paste it into your social media posts, bio, or comments. Most platforms support these Unicode characters."
            },
            {
                "question": "What's the difference between glitch text and cursed text?",
                "answer": "Glitch text typically mimics digital corruption and has a technological, cyberpunk aesthetic. Cursed text (Zalgo) has a more horror-oriented appearance with characters extending far above and below the text line."
            },
            {
                "question": "Can I use glitch text in my username?",
                "answer": "Many platforms allow some glitch text characters in usernames, but often with limitations. Try using a lower intensity setting for better compatibility with username fields."
            }
        ],
        "related_pages": [
            {"route": "cursed_text", "title": "Cursed Text Generator"},
            {"route": "discord_glitch_text", "title": "Discord Glitch Text"},
            {"route": "vaporwave_text", "title": "Vaporwave Text Generator"}
        ]
    },
    "discord-glitch-text": {
        "url": "discord-glitch-text",
        "page_title": "Discord Glitch Text Generator - Stand Out in Discord Chats",
        "meta_description": "Create Discord-compatible glitch text effects for your username, messages, and server names. Copy and paste directly into Discord.",
        "meta_keywords": "discord glitch text, discord text effects, discord formatting, discord zalgo",
        "canonical_url": "https://glitchtexteffect.com/discord-glitch-text",
        "h1_title": "Discord Glitch Text Generator",
        "subtitle": "Create eye-catching glitch effects that work perfectly in Discord chats, usernames, and server names. Stand out from other users with unique text styles.",
        "primary_effect": "ascii",
        "primary_effect_name": "Discord-Safe Glitch",
        "default_font": "cyber",
        "default_intensity": "4",
        "effect_intensity_label": "Discord Glitch Intensity",
        "input_placeholder": "Enter Discord text to glitch...",
        "default_text": "Cool Discord Username",
        "output_header": "Discord-Ready Glitched Text",
        "h2_title": "Using Glitch Text in Discord",
        "main_content": "<p>Discord supports many Unicode characters and text effects, making it perfect for using glitch text. Our Discord Glitch Text Generator creates effects that are compatible with Discord's character limitations.</p><p>You can use these effects for your username, in chat messages, for channel names, or even in your server description to create a unique aesthetic that stands out from other users and servers.</p>",
        "examples_title": "Discord Glitch Text Examples",
        "examples": [
            {
                "title": "Discord Username",
                "text": "G̷a̷m̷e̷r̷G̷l̷i̷t̷c̷h̷",
                "original": "GamerGlitch"
            },
            {
                "title": "Server Name",
                "text": "V̸o̸i̸d̸ ̸R̸e̸a̸l̸m̸",
                "original": "Void Realm"
            },
            {
                "title": "Chat Message",
                "text": "T̷h̷i̷s̷ ̷s̷e̷r̷v̷e̷r̷ ̷h̷a̷s̷ ̷b̷e̷e̷n̷ ̷c̷o̷r̷r̷u̷p̷t̷e̷d̷",
                "original": "This server has been corrupted"
            }
        ],
        "faq": [
            {
                "question": "Will these glitch effects work in Discord?",
                "answer": "Yes, our Discord Glitch Text Generator is specifically designed to work with Discord's character limitations. We've optimized the effects to be compatible while still looking impressive."
            },
            {
                "question": "Can I use glitch text in my Discord username?",
                "answer": "Yes, but Discord has some limitations on special characters in usernames. We recommend using our 'Discord-Safe Glitch' effect with a lower intensity setting (3-4) for usernames."
            },
            {
                "question": "How do I change my Discord username to glitch text?",
                "answer": "Generate your glitched username using our tool, copy it, then go to Discord User Settings > My Account > Edit username. Paste your glitched text and save changes."
            }
        ],
        "related_pages": [
            {"route": "cursed_text", "title": "Cursed Text Generator"},
            {"route": "glitch_text", "title": "Glitch Text Generator"},
            {"route": "minecraft_glitch_text", "title": "Minecraft Glitch Text"}
        ]
    }
}
