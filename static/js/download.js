// Function to download text as an image
function downloadAsImage() {
    // Find the output element based on the current page
    let outputElement;
    if (window.location.pathname.includes('halloween')) {
        outputElement = document.getElementById('halloween-output');
    } else if (window.location.pathname.includes('discord')) {
        outputElement = document.getElementById('output-text');
    } else if (window.location.pathname.includes('roblox')) {
        outputElement = document.getElementById('output-text');
    } else {
        outputElement = document.getElementById('output-text');
    }

    if (!outputElement) {
        console.error('Output element not found');
        return;
    }

    // Create canvas
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size with padding
    const padding = 40;
    canvas.width = Math.max(600, outputElement.offsetWidth + padding * 2);
    canvas.height = Math.max(200, outputElement.offsetHeight + padding * 2);

    // Set background
    ctx.fillStyle = getComputedStyle(outputElement).backgroundColor || '#1a1a1a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Add gradient background
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    gradient.addColorStop(0, '#1a1a1a');
    gradient.addColorStop(1, '#2a1a2a');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Get computed styles
    const styles = window.getComputedStyle(outputElement);
    ctx.font = `${styles.fontSize} ${styles.fontFamily}`;
    ctx.fillStyle = styles.color;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Draw text
    const text = outputElement.textContent;
    const lines = text.split('\n');
    const lineHeight = parseInt(styles.lineHeight) || parseInt(styles.fontSize) * 1.2;

    lines.forEach((line, i) => {
        const y = canvas.height/2 - ((lines.length-1)*lineHeight)/2 + i*lineHeight;
        ctx.fillText(line, canvas.width/2, y);
    });

    // Add watermark
    ctx.font = '14px Arial';
    ctx.fillStyle = 'rgba(255,255,255,0.3)';
    ctx.fillText('glitchtextgenerator.com', canvas.width - 100, canvas.height - 20);

    // Download image
    const link = document.createElement('a');
    const pageName = window.location.pathname.split('/').pop().split('.')[0] || 'text';
    link.download = `${pageName}-text.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}



