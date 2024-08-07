import flickrapi
import sys
import csv
import pandas as pd
import folium


def get_posts(hashtag, no_of_posts):
    """
    Retrieves recent posts with a given hashtag from Flickr.

    Parameters:
        - hashtag (str): Hashtag to search for.
        - no_of_posts (int): Number of posts to search for.

    Returns:
        - List of public posts.

    Raises:
        - flickrapi.exceptions.FlickrError: If no posts are found.
    """
    try:
        recent_photos = flickr.photos.search(
            tags=hashtag, has_geo=1, sort="date-posted-desc"
        )
        return recent_photos["photos"]["photo"][:no_of_posts]
    except flickrapi.exceptions.FlickrError as exception:
        raise flickrapi.exceptions.FlickrError(
            "Error retrieving posts: " + str(exception)
        )


def extract_posts_info(posts):
    """
    Extracts relevant information from a list of posts and saves it to a CSV file.

    Parameters:
        - posts (list): List of posts to extract information from.

    Raises:
        - flickrapi.exceptions.FlickrError: If no location information is found.
        - Exception: If an error occurs while saving the CSV file.
    """
    data = [["id", "title", "latitude", "longitude", "image_url", "post_url"]]
    for post in posts:
        location_info = flickr.photos.geo.getLocation(photo_id=post["id"])

        if location_info is not None:
            data.append(
                [
                    post["id"],
                    post["title"],
                    location_info["photo"]["location"]["latitude"],
                    location_info["photo"]["location"]["longitude"],
                    f"https://live.staticflickr.com/{post['server']}/{post['id']}_{post['secret']}_w.jpg",
                    f"https://www.flickr.com/photos/{post['owner']}/{post['id']}",
                ]
            )
        else:
            raise flickrapi.exceptions.FlickrError("No location info found!")
    try:
        with open("posts_info.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    except Exception as exception:
        raise Exception(f"Error while saving posts info to CSV: {exception}")


def plot_map():
    """
    Plots a map with locations of posts.

    Reads the extracted information from the 'posts.info.csv' file, groups posts with same location
    and creates interactive markers on the Folium mapThe map is centered and zoomed based on the average
    coordinates of all posts.

    Multiple posts at the same location are grouped together and displayed in a popup window.

    Note:
        - This function requires the 'posts_info.csv' file generated by the
        - 'extract_posts_info' function.

    Raises:
        - FileNotFoundError: If the 'posts_info.csv' file is not found.
        - Exception: If an error occurs while loading the CSV file.
    """
    # Load posts info from CSV file
    try:
        recent_posts = pd.read_csv("posts_info.csv", encoding="utf-8").to_dict(
            "records"
        )
    except FileNotFoundError as exception:
        raise FileNotFoundError(
            "Error while loading posts info from CSV: " + str(exception)
        )
    except Exception as exception:
        raise Exception("Error while loading posts info from CSV: " + str(exception))

    coordinates = list(
        (float(post["latitude"]), float(post["longitude"])) for post in recent_posts
    )

    # Calculate map center based on average coordinates of all posts
    map_center = (
        sum(x[0] for x in coordinates) / len(recent_posts),
        sum(x[1] for x in coordinates) / len(recent_posts),
    )

    # Create Folium map
    my_map = folium.Map(location=map_center, zoom_start=2)

    # Group posts with same location
    grouped_posts = {}
    for post in recent_posts:
        if (post["latitude"], post["longitude"]) not in grouped_posts:
            grouped_posts[(post["latitude"], post["longitude"])] = [post]
        else:
            grouped_posts[(post["latitude"], post["longitude"])].append(post)

    # Create markers on the map
    for location in grouped_posts.keys():
        if len(grouped_posts[location]) > 1:
            # Display multiple posts at the same location in a popup window
            html = "<div style='display: flex; flex-direction: column; align-items: center; "
            html += f'text-align: center; font-size: 16px; font-family: "Roboto", sans-serif;\'>'
            html += "<b>Multiple posts</b>"
            counter = 1
            for post in grouped_posts[location]:
                html += (
                    f"<div style='margin-top: 10px; display: flex; flex-direction: column;"
                    f" align-items: center; text-align: center;"
                    f' font-size: 16px; font-family: "Roboto", sans-serif;\'>'
                    f"<b>{counter} {post['title']}</b>"
                    f"<br><img src={post['image_url']} width=250>"
                    f"<br><a href='{post['post_url']}' target='_blank'>Post link address</a>"
                    "</div>"
                )
                counter += 1
            html += "</div>"
            # Add marker for multiple posts at the same location to the map
            folium.Marker(
                location=list(location),
                popup=folium.Popup(
                    folium.IFrame(
                        html=html,
                        width=300,
                        height=300,
                    )
                ),
                tooltip="Multiple posts",
            ).add_to(my_map)
        else:
            # Display single post at the location
            post = grouped_posts[location][0]
            #
            folium.Marker(
                location=list(location),
                popup=folium.Popup(
                    folium.IFrame(
                        html=f"<div style='display: flex; flex-direction: column; align-items: center; "
                        + f'text-align: center; font-size: 16px; font-family: "Roboto", sans-serif;\'>'
                        + f"<b>{post['title']}</b>"
                        + f"<br><img src={post['image_url']} width=250>"
                        + f"<br><a href='{post['post_url']}' target='_blank'>Post link address</a>"
                        + "</div>",
                        width=300,
                        height=300,
                    )
                ),
                tooltip=post["title"],
            ).add_to(my_map)

    # Fit the map to the bounds of the markers
    my_map.fit_bounds(coordinates)

    # Display the map in the browser
    my_map.show_in_browser()

    type("hello".upper())


if __name__ == "__main__":
    api_key = "f5182644ea1b5833908346029b1f39db"
    api_secret = "a5e515aecc94ec2f"

    try:
        if len(sys.argv) != 3:
            raise Exception("Add a hashtag and number of posts to search for!")

        flickr = flickrapi.FlickrAPI(api_key, api_secret, format="parsed-json")

        # Get most recent x posts with a given hashtag and x (number of posts) from Flickr
        posts = get_posts(sys.argv[1], int(sys.argv[2]))

        # Extract relevant information from posts and save it to a CSV file
        extract_posts_info(posts)

        # Plot a map with locations of posts.
        plot_map()

    except Exception as e:
        print(f"Error: {e}")
