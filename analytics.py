from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import json

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('analytics.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitor_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            session_id TEXT,
            ip_address TEXT,
            user_agent TEXT,
            browser TEXT,
            browser_version TEXT,
            language TEXT,
            screen_resolution TEXT,
            viewport TEXT,
            referrer TEXT,
            path TEXT,
            timezone TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.before_first_request
def setup():
    init_db()

@app.route('/api/analytics', methods=['POST'])
def collect_analytics():
    try:
        data = request.get_json()
        
        # Add server-side timestamp
        server_timestamp = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect('analytics.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO visitor_analytics (
                timestamp,
                session_id,
                ip_address,
                user_agent,
                browser,
                browser_version,
                language,
                screen_resolution,
                viewport,
                referrer,
                path,
                timezone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            server_timestamp,
            data.get('sessionId'),
            data.get('ipAddress'),
            data.get('userAgent'),
            data.get('browser'),
            data.get('browserVersion'),
            data.get('language'),
            data.get('screenResolution'),
            data.get('viewport'),
            data.get('referrer'),
            data.get('path'),
            data.get('timezone')
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'timestamp': server_timestamp}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/analytics/report', methods=['GET'])
def get_analytics_report():
    try:
        conn = sqlite3.connect('analytics.db')
        c = conn.cursor()
        
        # Get basic visitor stats
        c.execute('SELECT COUNT(DISTINCT session_id) FROM visitor_analytics')
        unique_visitors = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM visitor_analytics')
        total_pageviews = c.fetchone()[0]
        
        # Get most common browsers
        c.execute('''
            SELECT browser, COUNT(*) as count 
            FROM visitor_analytics 
            GROUP BY browser 
            ORDER BY count DESC 
            LIMIT 5
        ''')
        browsers = [{'browser': b[0], 'count': b[1]} for b in c.fetchall()]
        
        conn.close()
        
        return jsonify({
            'unique_visitors': unique_visitors,
            'total_pageviews': total_pageviews,
            'popular_browsers': browsers
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
