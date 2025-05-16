from flask import Blueprint, render_template

seo_blueprint = Blueprint('seo', __name__)

@seo_blueprint.route('/cursed-text')
def cursed_text():
    return render_template('seo/cursed_text.html')

@seo_blueprint.route('/glitch-text')
def glitch_text():
    return render_template('seo/glitch_text.html')

@seo_blueprint.route('/discord-glitch-text')
def discord_glitch_text():
    return render_template('seo/discord_glitch_text.html')
