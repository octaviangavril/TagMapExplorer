# Tag Map Explorer

This Python script uses the Flickr API to search for recent posts with a specific hashtag. It takes a hashtag and the specified number of posts and plots the locations of those posts on a map.

## Prerequisites

Before running the script, make sure you have the following:

- Python installed (version 3.6 or above)
- **Dependencies**: Install the required Python packages using the following command:
   ```bash
   pip install flickrapi pandas folium
## Usage

Run the script from the command line with the hashtag and the number of posts to search for as arguments.

```bash
python main.py <hashtag> <number_of_posts>
```

## Workflow

1. **Fetching Posts**:  The script searches for recent posts with the specified hashtag on Flickr using the Flickr API.

2. **Extracting Information**: Location information, including latitude and longitude, is extracted for each post.

3. **Map Plotting**: The script generates an interactive map using Folium. Posts are plotted as markers on the map.

4. **Handling Multiple Posts**:  If multiple posts are found at the same location, a grouped marker with a popup is created to display each post's details.

5. **Displaying Map**: The generated map is displayed in the default web browser.


## Output 

The script saves post information, including post ID, title, latitude, longitude, image URL, and post URL, to a CSV file named **'posts_info.csv'**.


## Author
  **Octavian Gavril**
    - [GitHub](https://github.com/octaviangavril)

## Additional Notes

- The script uses the [Flickr API](https://www.flickr.com/services/api/).
- This script assumes that the Flickr API responses follow the documented structure. If changes occur in the API, adjustments may be needed.
