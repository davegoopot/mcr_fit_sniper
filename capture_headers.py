# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

"""
Browser header capture instructions.

This script provides instructions and a simple server to help capture
the exact headers your browser sends when making a successful request.
"""

import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs


class HeaderCaptureHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to capture and display HTTP headers."""
    
    def do_GET(self):
        """Handle GET requests and display headers."""
        if self.path == "/" or self.path.startswith("/?"):
            # Serve the capture page
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Browser Header Capture</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
        }
        .step {
            background-color: #e9ecef;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }
        .step strong {
            color: #007bff;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #d63384;
        }
        .headers {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
            border: 1px solid #dee2e6;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            max-height: 400px;
            overflow-y: auto;
        }
        .copy-button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }
        .copy-button:hover {
            background-color: #0056b3;
        }
        .note {
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 4px;
            padding: 15px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Browser Header Capture Tool</h1>
        
        <p>This tool helps you capture the exact headers your browser sends when successfully accessing the website.</p>
        
        <h2>📋 Instructions</h2>
        
        <div class="step">
            <strong>Step 1:</strong> Open your browser's Developer Tools
            <ul>
                <li><strong>Chrome/Edge:</strong> Press F12 or Ctrl+Shift+I (Cmd+Option+I on Mac)</li>
                <li><strong>Firefox:</strong> Press F12 or Ctrl+Shift+I (Cmd+Option+I on Mac)</li>
                <li><strong>Safari:</strong> Enable Developer menu in Preferences, then press Cmd+Option+I</li>
            </ul>
        </div>
        
        <div class="step">
            <strong>Step 2:</strong> Go to the Network tab in Developer Tools
        </div>
        
        <div class="step">
            <strong>Step 3:</strong> Visit the target URL in your browser:<br>
            <code>https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c</code>
        </div>
        
        <div class="step">
            <strong>Step 4:</strong> In the Network tab:
            <ul>
                <li>Find the first request (usually the HTML document)</li>
                <li>Click on it to see details</li>
                <li>Look for "Request Headers" section</li>
                <li>Copy the headers shown</li>
            </ul>
        </div>
        
        <div class="step">
            <strong>Step 5:</strong> Look for these important headers:
            <ul>
                <li><code>User-Agent</code> - Identifies your browser</li>
                <li><code>Accept</code> - Content types accepted</li>
                <li><code>Accept-Language</code> - Language preferences</li>
                <li><code>Accept-Encoding</code> - Compression methods</li>
                <li><code>Referer</code> - Previous page (if any)</li>
                <li><code>Cookie</code> - Session cookies (if any)</li>
            </ul>
        </div>
        
        <h2>📝 What Your Server Sees</h2>
        <div class="note">
            <strong>Note:</strong> These are the headers this page received from your browser.
            They may differ from what the target website receives.
        </div>
        
        <div class="headers" id="headers"></div>
        <button class="copy-button" onclick="copyHeaders()">📋 Copy Headers as Python Dict</button>
        
        <h2>🔧 Next Steps</h2>
        <div class="step">
            <strong>Option A:</strong> Use the captured headers in <code>diagnose_403.py</code>
            <ul>
                <li>Add a new test with your captured headers</li>
                <li>Run the script to see if it works</li>
            </ul>
        </div>
        
        <div class="step">
            <strong>Option B:</strong> Update <code>scrape.py</code> directly
            <ul>
                <li>Add the working headers to the requests.get() call</li>
                <li>Test the updated script</li>
            </ul>
        </div>
    </div>
    
    <script>
        // Display captured headers
        const headers = """ + json.dumps(dict(self.headers)) + """;
        const headersDiv = document.getElementById('headers');
        
        let headerHtml = '<strong>Captured Headers:</strong><br><br>';
        for (const [key, value] of Object.entries(headers)) {
            headerHtml += `<strong>${key}:</strong> ${value}<br>`;
        }
        headersDiv.innerHTML = headerHtml;
        
        function copyHeaders() {
            const pythonDict = "headers = {\\n" +
                Object.entries(headers)
                    .map(([key, value]) => `    "${key}": "${value}"`)
                    .join(",\\n") +
                "\\n}";
            
            navigator.clipboard.writeText(pythonDict).then(() => {
                alert('Headers copied to clipboard as Python dictionary!');
            }).catch(err => {
                console.error('Failed to copy:', err);
                alert('Failed to copy. Please copy manually from the console.');
                console.log(pythonDict);
            });
        }
    </script>
</body>
</html>
            """
            
            self.wfile.write(html_content.encode())
        else:
            super().do_GET()
    
    def log_message(self, format, *args):
        """Custom log message to show captured headers."""
        print(f"\n[Request Captured]")
        print(f"Path: {self.path}")
        print(f"Headers:")
        for header, value in self.headers.items():
            print(f"  {header}: {value}")
        print()


def main():
    """Start the header capture server."""
    PORT = 8000
    
    print("=" * 70)
    print("BROWSER HEADER CAPTURE SERVER")
    print("=" * 70)
    print()
    print(f"Starting server on http://localhost:{PORT}")
    print()
    print("Instructions:")
    print(f"1. Open your browser and navigate to: http://localhost:{PORT}")
    print("2. Follow the instructions on the page to capture your browser headers")
    print("3. Press Ctrl+C to stop the server when done")
    print()
    print("=" * 70)
    
    try:
        with socketserver.TCPServer(("", PORT), HeaderCaptureHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n✗ Error: Port {PORT} is already in use.")
            print(f"  Try closing other applications or use a different port.")
        else:
            print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
