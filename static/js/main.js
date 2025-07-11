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
    
    // Load preset combinations on page load
    loadPresetCombinations();

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

    // Copy button functionality (consolidated)
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            try {
                const textToCopy = outputText.textContent;
                await navigator.clipboard.writeText(textToCopy);
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
    
    // Load preset combinations function
    async function loadPresetCombinations() {
        try {
            const response = await fetch('/api/preset-combinations');
            const presets = await response.json();
            
            const presetGrid = document.getElementById('preset-grid');
            if (presetGrid) {
                presetGrid.innerHTML = '';
                
                presets.forEach(preset => {
                    const presetItem = document.createElement('div');
                    presetItem.className = 'preset-item';
                    presetItem.innerHTML = `
                        <div class="preset-name">${preset.name}</div>
                        <div class="preset-original">${preset.original}</div>
                        <div class="preset-glitched">${preset.glitched}</div>
                        <div class="preset-effects">
                            <span class="effect-badge">${preset.effect}</span>
                            <span class="effect-badge">Level ${preset.intensity}</span>
                        </div>
                        <button class="use-preset-btn" onclick="usePreset('${preset.glitched}', '${preset.original}', '${preset.effect}', ${preset.intensity})">
                            Use This Combination
                        </button>
                    `;
                    presetGrid.appendChild(presetItem);
                });
            }
        } catch (error) {
            console.error('Error loading preset combinations:', error);
        }
    }
    
    // Make loadPresetCombinations available globally
    window.loadPresetCombinations = loadPresetCombinations;
});

// Share button functionality
function shareToTwitter() {
    const output = document.getElementById('output-text');
    const text = output ? output.textContent : '';
    if (text && text.trim()) {
        const tweetText = encodeURIComponent(`Check out this glitch text I created: ${text.substring(0, 100)}${text.length > 100 ? '...' : ''}`);
        const url = encodeURIComponent(window.location.href);
        window.open(`https://twitter.com/intent/tweet?text=${tweetText}&url=${url}`, '_blank');
    }
}

function shareToFacebook() {
    const url = encodeURIComponent(window.location.href);
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
}

function copyShareLink() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
        showToast('Link copied to clipboard!');
    }).catch(() => {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = url;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Link copied to clipboard!');
    });
}

function showToast(message) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--primary-color);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Use preset combination
function usePreset(glitchedText, originalText, effect, intensity) {
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const effectType = document.getElementById('effect-type');
    const intensitySlider = document.getElementById('intensity-slider');
    const intensityValue = document.getElementById('intensity-value');
    
    if (inputText) {
        inputText.value = originalText;
    }
    
    if (outputText) {
        outputText.textContent = glitchedText;
        outputText.style.display = 'block';
    }
    
    if (effectType) {
        effectType.value = effect;
    }
    
    if (intensitySlider) {
        intensitySlider.value = intensity;
    }
    
    if (intensityValue) {
        intensityValue.textContent = intensity;
    }
    
    showToast('Preset combination applied!');
}

// Use with Glitch Generator function (for inspiration pages)
function useWithGlitchGenerator(text) {
    // Store text in localStorage to pass to main page
    localStorage.setItem('glitch_prefill_text', text);
    
    // Navigate to main page
    window.location.href = '/';
}

// Quick combine function
async function quickCombine(emoticon, symbol, effect = 'zalgo', intensity = 5) {
    try {
        const response = await fetch('/api/quick-combine', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                emoticon: emoticon,
                symbol: symbol,
                effect: effect,
                intensity: intensity
            })
        });
        
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Failed to combine');
        
        // Update the UI with the combined result
        const inputText = document.getElementById('input-text');
        const outputText = document.getElementById('output-text');
        const effectType = document.getElementById('effect-type');
        const intensitySlider = document.getElementById('intensity-slider');
        const intensityValue = document.getElementById('intensity-value');
        
        if (inputText) {
            inputText.value = data.original;
        }
        
        if (outputText) {
            outputText.textContent = data.result;
            outputText.style.display = 'block';
        }
        
        if (effectType) {
            effectType.value = data.effect;
        }
        
        if (intensitySlider) {
            intensitySlider.value = data.intensity;
        }
        
        if (intensityValue) {
            intensityValue.textContent = data.intensity;
        }
        
        showToast('Quick combination created!');
        
    } catch (error) {
        console.error('Error in quick combine:', error);
        showToast('Error creating combination: ' + error.message);
    }
}

// Check for prefilled text on page load
document.addEventListener('DOMContentLoaded', function() {
    const prefilledText = localStorage.getItem('glitch_prefill_text');
    const prefilledResult = localStorage.getItem('glitch_result');
    
    if (prefilledText) {
        const inputText = document.getElementById('input-text');
        const outputText = document.getElementById('output-text');
        
        if (inputText) {
            inputText.value = prefilledText;
            // Trigger the update if no result is stored
            if (!prefilledResult) {
                inputText.dispatchEvent(new Event('input'));
            }
        }
        
        // If we have a pre-generated result, use it
        if (prefilledResult && outputText) {
            outputText.textContent = prefilledResult;
            outputText.style.display = 'block';
        }
        
        // Clear the stored text and result
        localStorage.removeItem('glitch_prefill_text');
        localStorage.removeItem('glitch_result');
        
        // Show toast notification
        showToast('Text imported from inspiration page! 🎉');
    }
});

// Add animation keyframes (check if not already added)
if (!document.getElementById('main-animations')) {
    const mainAnimationStyle = document.createElement('style');
    mainAnimationStyle.id = 'main-animations';
    mainAnimationStyle.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(mainAnimationStyle);
}
