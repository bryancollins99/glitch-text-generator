function shareText() {
    const glitchText = document.getElementById('output-text').textContent;
    const shareUrl = `${window.location.origin}?text=${encodeURIComponent(glitchText)}`;
    
    if (navigator.share) {
        navigator.share({
            title: 'Check out this glitch text!',
            text: glitchText,
            url: shareUrl
        }).catch(console.error);
    } else {
        navigator.clipboard.writeText(shareUrl).then(() => {
            showToast('Share link copied to clipboard!');
        }).catch(console.error);
    }
}

function downloadAsImage() {
    const text = document.getElementById('output-text').textContent;
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = 800;
    canvas.height = 400;
    
    // Set background
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Set text style
    ctx.fillStyle = '#ffffff';
    ctx.font = '32px "Courier New", monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Add glitch effect to canvas
    const lines = text.split('\n');
    lines.forEach((line, i) => {
        const y = canvas.height/2 - ((lines.length-1)*40)/2 + i*40;
        
        // Add glitch effect
        if (Math.random() > 0.7) {
            ctx.fillStyle = '#ff00ff';
            ctx.fillText(line, canvas.width/2 + 2, y + 2);
            ctx.fillStyle = '#00ffff';
            ctx.fillText(line, canvas.width/2 - 2, y - 2);
        }
        
        ctx.fillStyle = '#ffffff';
        ctx.fillText(line, canvas.width/2, y);
    });
    
    // Create download link
    const link = document.createElement('a');
    link.download = 'glitch-text.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    }, 100);
}
