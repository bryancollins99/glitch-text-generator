document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const effectType = document.getElementById('effect-type');
    const fontStyle = document.getElementById('font-family');
    const intensitySlider = document.getElementById('intensity-slider');
    const animationSpeed = document.getElementById('animation-speed');
    const colorScheme = document.getElementById('color-scheme');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');
    const shareBtn = document.getElementById('share-btn');
    let currentTimeout;
    let animationInterval;

    async function updateOutput() {
        clearTimeout(currentTimeout);
        currentTimeout = setTimeout(async () => {
            const text = inputText.value;
            const effect = effectType ? effectType.value : 'zalgo';
            const font = fontStyle ? fontStyle.value : 'default';
            const intensity = intensitySlider ? intensitySlider.value : 5;

            if (!text) {
                outputText.textContent = '';
                return;
            }

            try {
                const response = await fetch('/api/glitch', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: text,
                        effect: effect,
                        font_style: font,
                        intensity: parseInt(intensity)
                    })
                });

                const data = await response.json();
                if (!response.ok) throw new Error(data.error || 'Failed to generate text');

                if (data.result) {
                    outputText.textContent = data.result;
                    outputText.style.display = 'block';
                    if (animationSpeed && parseInt(animationSpeed.value) > 0) {
                        startAnimation();
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                outputText.textContent = 'Error generating glitch text: ' + error.message;
            }
        }, 300);
    }

    function startAnimation() {
        if (animationInterval) {
            clearInterval(animationInterval);
        }
        
        if (!animationSpeed || !outputText) return;
        
        const speed = Math.max(50, (11 - parseFloat(animationSpeed.value)) * 100);
        outputText.style.animation = `glitch-animation ${speed}ms infinite`;
    }

    function updateColorScheme(scheme) {
        document.body.className = '';
        document.body.classList.add(`scheme-${scheme}`);
    }

    // Copy button functionality
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(outputText.textContent);
                const originalText = copyBtn.textContent;
                copyBtn.textContent = 'Copied!';
                setTimeout(() => copyBtn.textContent = originalText, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
        });
    }

    // Download button functionality
    if (downloadBtn) {
        downloadBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: outputText.textContent,
                        format: 'png'
                    })
                });

                if (!response.ok) throw new Error('Failed to generate image');

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'glitch-text.png';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } catch (error) {
                console.error('Download failed:', error);
                alert('Failed to download image: ' + error.message);
            }
        });
    }

    // Share button functionality
    if (shareBtn) {
        shareBtn.addEventListener('click', async () => {
            try {
                if (navigator.share) {
                    await navigator.share({
                        title: 'Glitch Text',
                        text: outputText.textContent,
                        url: window.location.href
                    });
                } else {
                    await navigator.clipboard.writeText(outputText.textContent);
                    alert('Text copied to clipboard!');
                }
            } catch (err) {
                console.error('Share failed:', err);
            }
        });
    }

    // Input and effect change handlers
    if (inputText && outputText) {
        inputText.addEventListener('input', updateOutput);
        if (effectType) effectType.addEventListener('change', updateOutput);
        if (fontStyle) fontStyle.addEventListener('change', updateOutput);
        if (intensitySlider) {
            intensitySlider.addEventListener('input', updateOutput);
            const intensityValue = document.getElementById('intensity-value');
            if (intensityValue) {
                intensitySlider.addEventListener('input', () => {
                    intensityValue.textContent = intensitySlider.value;
                });
            }
        }
        if (animationSpeed) {
            animationSpeed.addEventListener('input', () => {
                const value = parseFloat(animationSpeed.value);
                if (value > 0) {
                    startAnimation();
                } else {
                    if (animationInterval) {
                        clearInterval(animationInterval);
                    }
                    outputText.style.animation = 'none';
                }
            });
        }
        if (colorScheme) {
            colorScheme.addEventListener('change', (e) => {
                updateColorScheme(e.target.value);
            });
        }
    }

    if (copyBtn) {
        copyBtn.addEventListener('click', () => {
            const textToCopy = outputText.textContent;
            navigator.clipboard.writeText(textToCopy).then(() => {
                copyBtn.textContent = 'Copied!';
                setTimeout(() => {
                    copyBtn.textContent = 'Copy';
                }, 2000);
            });
        });
    }

    // Quick effect buttons
    document.querySelectorAll('.quick-effect').forEach(btn => {
        btn.addEventListener('click', () => {
            const preset = btn.dataset.preset;
            if (!intensitySlider) return;
            
            switch(preset) {
                case 'mild':
                    intensitySlider.value = 3;
                    break;
                case 'medium':
                    intensitySlider.value = 5;
                    break;
                case 'extreme':
                    intensitySlider.value = 8;
                    break;
                case 'random':
                    intensitySlider.value = Math.floor(Math.random() * 10) + 1;
                    break;
            }
            updateOutput();
        });
    });

    // Initialize color scheme
    if (colorScheme) {
        updateColorScheme(colorScheme.value);
    }
});
