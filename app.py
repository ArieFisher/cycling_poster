from flask import Flask, render_template, request, send_file, flash
import io
import main
import config
import json
import base64

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

@app.route('/', methods=['GET'])
def index():
    # Pass defaults to the template
    defaults = {
        'style': config.STYLE,
        'scale': getattr(config, 'SCALE_FACTOR', 2),
        'width': getattr(config, 'WIDTH', 3000),
        'height': getattr(config, 'HEIGHT', 4000),
        'zoom': getattr(config, 'ZOOM', 10.5),
        'pitch': getattr(config, 'PITCH', 43),
        'bearing': getattr(config, 'BEARING', 163),
    }
    return render_template('index.html', defaults=defaults)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get parameters from form
        source_type = request.form.get('source_type', 'url')
        url = request.form.get('url')
        
        width = int(request.form.get('width', 2048))
        height = int(request.form.get('height', 2048))
        scale = int(request.form.get('scale', 2))
        style = request.form.get('style')
        
        # Optional float parameters
        zoom = request.form.get('zoom')
        zoom = float(zoom) if zoom else None
        
        pitch = request.form.get('pitch')
        pitch = float(pitch) if pitch else None
        
        bearing = request.form.get('bearing')
        bearing = float(bearing) if bearing else None

        # 1. Fetch Data
        data = None
        if source_type == 'file':
            if 'file' not in request.files:
                return render_template('index.html', error="No file uploaded.", defaults=request.form)
            file = request.files['file']
            if file.filename == '':
                return render_template('index.html', error="No file selected.", defaults=request.form)
            try:
                data = json.load(file)
            except Exception as e:
                return render_template('index.html', error=f"Invalid JSON file: {e}", defaults=request.form)
        else:
            if not url:
                return render_template('index.html', error="Please provide a GeoJSON URL.", defaults=request.form)
            data = main.fetch_geojson_data(url)
        
        if not data:
            return render_template('index.html', error="Failed to fetch/parse GeoJSON data.", defaults=request.form)

        # 2. Apply Style
        data = main.apply_style_to_geojson(data)

        # 3. Generate Map
        image_content = main.generate_map_from_geojson(
            config.API_KEY,
            data,
            width=width,
            height=height,
            scale_factor=scale,
            style=style,
            zoom=zoom,
            pitch=pitch,
            bearing=bearing
        )

        if not image_content:
            return render_template('index.html', error="Failed to generate map image from API.", defaults=request.form)

        # 4. Return Image for Preview
        # Convert to base64
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        
        return render_template(
            'index.html', 
            image_data=image_base64, 
            defaults=request.form,
            success="Map generated successfully!"
        )

    except Exception as e:
        return render_template('index.html', error=f"An unexpected error occurred: {str(e)}", defaults=request.form)

if __name__ == '__main__':
    app.run(debug=True)
