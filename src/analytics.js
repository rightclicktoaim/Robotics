// analytics.js
class VisitorAnalytics {
    constructor() {
        this.data = {
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            language: navigator.language,
            screenResolution: `${window.screen.width}x${window.screen.height}`,
            viewport: `${window.innerWidth}x${window.innerHeight}`,
            referrer: document.referrer || 'direct',
            path: window.location.pathname,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            sessionId: this.generateSessionId()
        };
    }

    generateSessionId() {
        return 'sess_' + Math.random().toString(36).substr(2, 9);
    }

    getBrowserInfo() {
        const ua = navigator.userAgent;
        let browser = "Unknown";
        let version = "Unknown";

        if (ua.includes("Firefox/")) {
            browser = "Firefox";
            version = ua.split("Firefox/")[1];
        } else if (ua.includes("Chrome/")) {
            browser = "Chrome";
            version = ua.split("Chrome/")[1].split(" ")[0];
        } else if (ua.includes("Safari/") && !ua.includes("Chrome")) {
            browser = "Safari";
            version = ua.split("Version/")[1].split(" ")[0];
        }

        this.data.browser = browser;
        this.data.browserVersion = version;
    }

    async getIPInfo() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const data = await response.json();
            this.data.ipAddress = data.ip;
        } catch (error) {
            console.error('Error fetching IP:', error);
            this.data.ipAddress = 'unknown';
        }
    }

    async collectAndSend() {
        this.getBrowserInfo();
        await this.getIPInfo();
        
        try {
            const response = await fetch('/api/analytics', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.data)
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            console.log('Analytics data sent successfully');
        } catch (error) {
            console.error('Error sending analytics data:', error);
        }
    }
}

// Usage
document.addEventListener('DOMContentLoaded', () => {
    const analytics = new VisitorAnalytics();
    analytics.collectAndSend();
});