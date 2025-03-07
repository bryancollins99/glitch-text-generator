document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('halloween-input');
    const output = document.getElementById('halloween-output');
    const copyBtn = document.getElementById('copy-btn');
    const styleSelect = document.getElementById('halloween-style');
    const animationSelect = document.getElementById('animation-type');
    const colorSelect = document.getElementById('color-scheme');
    const presetButtons = document.querySelectorAll('.preset-btn');

    // Error handling functions
    function showError(message) {
        const errorDiv = document.getElementById('error-message') || createErrorDiv();
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 3000);
    }

    function createErrorDiv() {
        const errorDiv = document.createElement('div');
        errorDiv.id = 'error-message';
        errorDiv.style.cssText = 'display:none; color:red; margin:10px 0; padding:10px; border:1px solid red; border-radius:4px;';
        input.parentNode.insertBefore(errorDiv, input);
        return errorDiv;
    }

    // Halloween text effects
    const effects = {
        blood: text => {
            return text.split('').map(char => 
                `<span style="color: #ff0000; text-shadow: 2px 2px 4px #800000;">${char}</span>`
            ).join('');
        },
        zombie: text => {
            return text.split('').map(char => 
                `<span style="color: #50c878; text-shadow: 2px 2px 4px #2f4f4f;">${char}</span>`
            ).join('');
        },
        ghost: text => {
            return text.split('').map(char => 
                `<span style="color: #f8f8ff; text-shadow: 0 0 15px #f8f8ff;">${char}</span>`
            ).join('');
        },
        witch: text => {
            return text.split('').map(char => 
                `<span style="color: #9370db; text-shadow: 2px 2px 4px #4b0082;">${char}</span>`
            ).join('');
        },
        vampire: text => {
            return text.split('').map(char => 
                `<span style="color: #800000; text-shadow: 2px 2px 4px #000000;">${char}</span>`
            ).join('');
        }
    };

    // Color themes
    const colors = {
        blood: { color: '#ff0000', shadow: '#800000' },
        pumpkin: { color: '#ff6600', shadow: '#cc5500' },
        ghost: { color: '#f8f8ff', shadow: '#c0c0c0' },
        witch: { color: '#50c878', shadow: '#2f4f4f' },
        purple: { color: '#9370db', shadow: '#4b0082' }
    };

    // Animation classes
    const animations = {
        none: '',
        flicker: 'halloween-flicker',
        float: 'halloween-float',
        shake: 'halloween-shake',
        drip: 'halloween-drip'
    };

    // Preset text styles
    const presets = {
        haunted: { style: 'ghost', animation: 'flicker', color: 'ghost' },
        graveyard: { style: 'zombie', animation: 'float', color: 'witch' },
        pumpkin: { style: 'witch', animation: 'shake', color: 'pumpkin' },
        spider: { style: 'vampire', animation: 'drip', color: 'purple' }
    };

    function applyHalloweenEffect() {
        const text = input.value.trim();
        if (!text) {
            output.innerHTML = '';
            return;
        }

        const style = styleSelect.value;
        const animation = animationSelect.value;
        const colorTheme = colorSelect.value;

        try {
            // Apply the selected effect
            let transformedText = effects[style](text);

            // Apply color theme
            const theme = colors[colorTheme];
            output.style.color = theme.color;
            output.style.textShadow = `2px 2px 4px ${theme.shadow}`;

            // Set the transformed text
            output.innerHTML = transformedText;

            // Remove any existing animation classes
            Object.values(animations).forEach(cls => {
                if (cls) output.classList.remove(cls);
            });

            // Add the selected animation class
            if (animations[animation]) {
                output.classList.add(animations[animation]);
            }
        } catch (error) {
            console.error('Error applying effect:', error);
            showError('Failed to apply effect. Please try again.');
        }
    }

    // Event listeners
    input.addEventListener('input', applyHalloweenEffect);
    styleSelect.addEventListener('change', applyHalloweenEffect);
    animationSelect.addEventListener('change', applyHalloweenEffect);
    colorSelect.addEventListener('change', applyHalloweenEffect);

    // Copy button functionality
    copyBtn.addEventListener('click', () => {
        const textToCopy = output.textContent;
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = 'Copied!';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        }).catch(() => {
            showError('Failed to copy text');
        });
    });

    // Preset buttons
    presetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const preset = presets[button.dataset.preset];
            if (preset) {
                styleSelect.value = preset.style;
                animationSelect.value = preset.animation;
                colorSelect.value = preset.color;
                applyHalloweenEffect();
            }
        });
    });
});
