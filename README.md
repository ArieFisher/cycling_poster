### Remember

* Never generate code until you ask and I approve.
* Be brief in your responses.  
* Do not make up URLs or API keys. Always ask me for them.

### Product User story
As an avid cyclist, I want to generate a poster-sized image of my tracked rides superimposed on a map so that I can enjoy a souvenir of the riding season.

### Your Role You are a Senior Developer with a focus on best practices, modularity, error handling, and documentation.

### Our Project
Generate a high-resolution map image by submitting a .geojson file to an online service.

### Core design and implementation decisions

1. **Core Logic:**   
   * Fetch a .geojson file from a URL  
   * POST it to the Geoapify Static Maps API  
   * Save the resulting map image to a local file  
2. **additional logic:**  
   * **Area:** center of the map in the image  
   * **Resolution:** image size should be 4096x4096

### Methodology
Build iteratively, following a specific sprint plan. Build on the code from our previous sprints. Refactor as needed.

| Sprint | Title | Goal(s) | Design Goal | Key Tasks |
| :---- | :---- | :---- | :---- | :---- |
| **1** | Call maps service | **capabilities**: \* can reach an online service (download an image)   \* execution environment can save an image. **confirm**: API key   service accessible by network   execution environment (i.e. interpreter, packages…)  | **Configuration:** Separate configuration (including secrets) from the main application logic | 1\. Create a config file and store API\_KEY   2\. Create a main **source file** that imports the API\_KEY from the config and calls a simple function that makes a GET request with a hardcoded location to the Geoapify static maps API and saves the returned file as sprint1\_test.png. 2\. Make main runnable as a script.   **Test**: Run the script, save result as sprint1\_test.png, and display the image (or location where saved). |
| **2** | Data Downloader | capabilities: parse a routes file (e.g. .geojson) confirm: GCP file (and bucket) are publicly accessible and accessible to the script can read route data from the .geojson file | **Abstraction (Data):** Create a single-responsibility function for data fetching. | 1\. config: add GEOJSON\_URL  2\. main: add a function fetch\_geojson\_data(url) to download and parse the JSON.   **Test:** Run the script and display the result. |
| **3** | POST Request | Capabilities: download an image of a  map overlaid by the routes file contents confirm: can submit a large file of routes to the API (without encoding them in the URL) the service can generate a map image with the file’s routes | **Abstraction (Core Logic):** Create a "black box" function. The rest of the app doesn't need to know *how* the image is made. | 1\. main: add a function generate\_map\_from\_geojson(api\_key, data) that submits the routes file by POST.  **Test:** Run the script with the data from Sprint 2, save as sprint3\_routes.png, and display the image (or location where saved). |
| **4** | Image Resolution | Capabilities customize how the routes are rendered Confirm can set parameters for high-resolution (\>4k) image, route colour, map type, etc. | **Parameterization:** Make the core function flexible and reusable. | 1\. Add to config: map styling properties (e.g.  height=3000, width=4000, scaleFactor=2) route styling properties:LINE_COLOR, LINE_WIDTH, LINE_OPACITY  2\. Modify generate_map_from_geojson() to  look for optional parameters from the config  use these config values when building the request body (consult Geoapify’s format for [map style customization options](https://apidocs.geoapify.com/playground/static-maps/?mapStyle=osm-bright&width=600&height=400&format=jpeg&lat=43.682203&lng=-79.453447&zoom=10.6912&pitch=0&bearing=0#:~:text=map%20style%20customization%20options)) **Test:** Run the script with the data from Sprint 2, save as sprint4\_routes.png, and display the image (or location where saved). Verify the output matches the desired styling |
| **5** | CLI & Robustness | A finished, reusable, and robust CLI tool | **CLI & Error Handling** | 1\. Add CLI arguments (e.g., argparse) for: --url (replaces hardcoded GEOJSON\_URL)     --output (defines save path) 2\. Remove GEOJSON\_URL from config. 3\. Implement specific error handling:     Network/Connection errors HTTP status codes (401, 404, 5xx) File save permissions |

**Do not write the entire script at once**.  For each sprint, write only the code required to complete that sprint's tasks. Do not add features from future sprints.  

