import os

workers = 4
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
timeout = 120
keepalive = 5
errorlog = "-"
accesslog = "-"
capture_output = True
