from flask import Flask, render_template, request, send_file, flash
import io
import main
import config

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        url = request.form.get('url')
        width = int(request.form.get('width', 2048))
        height = int(request.form.get('height', 2048))
        scale = int(request.form.get('scale', 2))

        if not url:
            return render_template('index.html', error="Please provide a GeoJSON URL.")

        # 1. Fetch Data
        data = main.fetch_geojson_data(url)
        if not data:
            return render_template('index.html', error="Failed to fetch GeoJSON data. Check the URL.")

        # 2. Apply Style
        data = main.apply_style_to_geojson(data)

        # 3. Generate Map
        # Use API Key from config (or env var if we were fully cloud-native)
        image_content = main.generate_map_from_geojson(
            config.API_KEY,
            data,
            width=width,
            height=height,
            scale_factor=scale
        )

        if not image_content:
            return render_template('index.html', error="Failed to generate map image from API.")

        # 4. Return Image
        return send_file(
            io.BytesIO(image_content),
            mimetype='image/png',
            as_attachment=True,
            download_name='cycle_map.png'
        )

    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
