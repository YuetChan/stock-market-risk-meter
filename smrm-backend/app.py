from flask import Flask, jsonify
import sqlite3
from flask_caching import Cache

app = Flask(__name__)

# Configure caching (simple cache for demonstration)
app.config['CACHE_TYPE'] = 'SimpleCache'  # You can also use 'RedisCache', 'MemcachedCache', etc.
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds (5 minutes)
cache = Cache(app)


def query_scores():
    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT stock, score, date FROM stock_scores")
    scores = cursor.fetchall()
    
    conn.close()
    
    return [{'stock': row[0], 'score': row[1], 'date': row[2]} for row in scores]


@app.route('/api/scores', methods=['GET'])
@cache.cached(timeout=300)  # Cache this view for 5 minutes (300 seconds)
def get_scores():
    scores = query_scores()
    return jsonify(scores)


if __name__ == '__main__':
    app.run(debug=True)
