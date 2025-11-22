import requests
import json
import argparse
import sys
import os
import config

def test_static_map():
    """
    Makes a simple GET request to Geoapify Static Maps API
    to verify the API key and save a test image.
    """
    # Hardcoded location (Paris) for Sprint 1 test
    lat = 48.8566
    lon = 2.3522
    zoom = 12
    width = 600
    height = 400
    
    # Construct URL
    url = f"https://maps.geoapify.com/v1/staticmap?style=osm-carto&width={width}&height={height}&center=lonlat:{lon},{lat}&zoom={zoom}&apiKey={config.API_KEY}"
    
    print(f"Requesting map for location: {lat}, {lon}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an error for bad status codes
        
        output_filename = "sprint1_test.png"
        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"Success: {output_filename} saved.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching map: {e}")

def fetch_geojson_data(url):
    """
    Fetches GeoJSON data from a URL and returns the parsed JSON object.
    
    Args:
        url: The URL to fetch the GeoJSON from
        
    Returns:
        dict: Parsed GeoJSON data, or None if error
        
    Raises:
        requests.exceptions.ConnectionError: Network connection issues
        requests.exceptions.HTTPError: HTTP errors (404, 401, 5xx, etc.)
        ValueError: Invalid JSON data
    """
    print(f"Fetching GeoJSON data from {url}...")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"Success: GeoJSON data loaded.")
        
        # Display summary information
        if 'features' in data:
            print(f"Number of features: {len(data['features'])}")
        if 'type' in data:
            print(f"GeoJSON type: {data['type']}")
            
        return data
        
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Network connection failed. Please check your internet connection.")
        print(f"Details: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"ERROR: Request timed out. The server took too long to respond.")
        print(f"Details: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"ERROR: GeoJSON file not found (404). Please check the URL.")
        elif e.response.status_code == 401:
            print(f"ERROR: Unauthorized (401). Authentication required.")
        elif e.response.status_code >= 500:
            print(f"ERROR: Server error ({e.response.status_code}). Please try again later.")
        else:
            print(f"ERROR: HTTP error {e.response.status_code}: {e}")
        return None
    except ValueError as e:
        print(f"ERROR: Invalid JSON data. The file is not valid GeoJSON.")
        print(f"Details: {e}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error while fetching GeoJSON: {e}")
        return None

def apply_style_to_geojson(data):
    """
    Applies configured styling to GeoJSON features.
    
    Args:
        data: GeoJSON data (FeatureCollection)
        
    Returns:
        dict: Styled GeoJSON data
    """
    if 'features' in data:
        print(f"Applying route styling: color={config.LINE_COLOR}, width={config.LINE_WIDTH}, opacity={config.LINE_OPACITY}")
        for feature in data['features']:
            if 'properties' not in feature:
                feature['properties'] = {}
            
            # Override/Set styling properties
            feature['properties']['linecolor'] = config.LINE_COLOR
            feature['properties']['linewidth'] = config.LINE_WIDTH
            feature['properties']['lineopacity'] = config.LINE_OPACITY
            
    return data

def generate_map_from_geojson(api_key, data, width=800, height=600, scale_factor=1, style=None, zoom=None, pitch=None, bearing=None):
    """
    Generates a static map image from GeoJSON data using Geoapify Static Maps API.
    
    Args:
        api_key: Geoapify API key
        data: GeoJSON data (FeatureCollection or Feature)
        width: Image width in pixels (default: 800)
        height: Image height in pixels (default: 600)
        scale_factor: Scale factor for higher resolution (1 or 2, default: 1)
        style: Map style (optional, defaults to config.STYLE)
        zoom: Zoom level (optional, defaults to config.ZOOM)
        pitch: Pitch angle (optional, defaults to config.PITCH)
        bearing: Bearing angle (optional, defaults to config.BEARING)
        
    Returns:
        bytes: Image content if successful, None otherwise
        
    Raises:
        requests.exceptions.HTTPError: HTTP errors from API
    """
    # Use provided values or fall back to config defaults
    style = style if style is not None else config.STYLE
    zoom = zoom if zoom is not None else getattr(config, 'ZOOM', None)
    pitch = pitch if pitch is not None else getattr(config, 'PITCH', None)
    bearing = bearing if bearing is not None else getattr(config, 'BEARING', None)

    effective_resolution = f"{width * scale_factor}x{height * scale_factor}"
    print(f"Generating map from GeoJSON data ({width}x{height}, scale={scale_factor}, effective={effective_resolution})...")
    print(f"Using map style: {style}")
    if bearing is not None:
        print(f"Using bearing: {bearing}")
    if pitch is not None:
        print(f"Using pitch: {pitch}")
    if zoom is not None:
        print(f"Using zoom: {zoom}")
    
    # API key goes in the URL, GeoJSON goes in the body
    url = f"https://maps.geoapify.com/v1/staticmap?apiKey={api_key}"
    
    # Wrap GeoJSON in request body with dimensions and style
    request_body = {
        "geojson": data,
        "width": width,
        "height": height,
        "scaleFactor": scale_factor,
        "style": style
    }

    # Add optional parameters if they exist
    if bearing is not None:
        request_body["bearing"] = bearing
    if pitch is not None:
        request_body["pitch"] = pitch
    if zoom is not None:
        request_body["zoom"] = zoom
    
    # Add style customization if configured
    if hasattr(config, 'STYLE_CUSTOMIZATION') and config.STYLE_CUSTOMIZATION:
        print(f"Applying {len(config.STYLE_CUSTOMIZATION)} layer style customizations.")
        request_body["styleCustomization"] = config.STYLE_CUSTOMIZATION
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(request_body),
            timeout=60
        )
        response.raise_for_status()
        
        print(f"Success: Map generated ({len(response.content)} bytes)")
        return response.content
        
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Network connection failed while generating map.")
        print(f"Details: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"ERROR: Map generation timed out. Try a smaller image size.")
        print(f"Details: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"ERROR: Invalid API key (401). Please check your API key.")
        elif e.response.status_code == 400:
            print(f"ERROR: Bad request (400). Check your GeoJSON data or parameters.")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
        elif e.response.status_code >= 500:
            print(f"ERROR: Server error ({e.response.status_code}). Try reducing image size or try again later.")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
        else:
            print(f"ERROR: HTTP error {e.response.status_code}: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error while generating map: {e}")
        return None

def save_image(image_content, output_path):
    """
    Saves image content to a file.
    
    Args:
        image_content: Image bytes to save
        output_path: Path to save the image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            print(f"ERROR: Directory does not exist: {output_dir}")
            return False
            
        # Try to write the file
        with open(output_path, "wb") as f:
            f.write(image_content)
        print(f"Success: Map saved as {output_path}")
        return True
        
    except PermissionError:
        print(f"ERROR: Permission denied. Cannot write to {output_path}")
        return False
    except OSError as e:
        print(f"ERROR: Cannot save file: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error while saving file: {e}")
        return False

def main():
    """
    Main CLI entry point.
    """
    parser = argparse.ArgumentParser(
        description="Generate a high-resolution map image from GeoJSON data using Geoapify Static Maps API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url https://example.com/data.geojson --output map.png
  %(prog)s --url https://example.com/data.geojson --output map.png --width 2048 --height 2048 --scale 2
        """
    )
    
    parser.add_argument(
        "--url",
        required=True,
        help="URL to the GeoJSON file"
    )
    
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path for the generated map image (e.g., map.png)"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        default=2048,
        help="Image width in pixels (default: 2048)"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        default=2048,
        help="Image height in pixels (default: 2048)"
    )
    
    parser.add_argument(
        "--scale",
        type=int,
        default=2,
        choices=[1, 2],
        help="Scale factor for higher resolution: 1 or 2 (default: 2)"
    )
    
    args = parser.parse_args()
    
    # Validate dimensions
    if args.width <= 0 or args.height <= 0:
        print("ERROR: Width and height must be positive integers.")
        sys.exit(1)
    
    if args.width > 4096 or args.height > 4096:
        print("WARNING: Very large dimensions may cause API errors. Recommended max: 2048x2048 with scale=2")
    
    # Fetch GeoJSON data
    geojson_data = fetch_geojson_data(args.url)
    if not geojson_data:
        print("ERROR: Failed to fetch GeoJSON data. Exiting.")
        sys.exit(1)
    
    # Apply styling from config
    geojson_data = apply_style_to_geojson(geojson_data)
    
    # Generate map
    image_content = generate_map_from_geojson(
        config.API_KEY,
        geojson_data,
        width=args.width,
        height=args.height,
        scale_factor=args.scale
    )
    
    if not image_content:
        print("ERROR: Failed to generate map. Exiting.")
        sys.exit(1)
    
    # Save image
    if not save_image(image_content, args.output):
        print("ERROR: Failed to save image. Exiting.")
        sys.exit(1)
    
    print(f"\n✓ Successfully created map: {args.output}")
    print(f"  Resolution: {args.width}x{args.height} (scale={args.scale}, effective={args.width * args.scale}x{args.height * args.scale})")

if __name__ == "__main__":
    main()


