from flask import Flask, render_template, url_for, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main HTML page
    return render_template('index.html')

@app.route('/palette')
def get_palette():
    # Provide the path to the JSON file with color palettes
    try:
        with open('static/palettes/palette.json') as f:
            palettes = f.read()
        return jsonify(palettes)
    except FileNotFoundError:
        return jsonify({"error": "Palette file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
