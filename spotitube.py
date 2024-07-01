from pytube import YouTube, Search
import pytube
import pytube.streams
import requests
from deepmerge import always_merger
import PySimpleGUI as sg
import os


def spotify_auth() -> str:
    """
    Authenticates with Spotify API and returns the access token.

    Returns:
        str: The access token with the token type, e.g. "Bearer YOUR_ACCESS_TOKEN".
    """

    # Spotify API credentials
    client_id: str = '2fb41a718a984bc493e59053c21b82e4'
    client_secret: str = '53f7bf3c29354180ae4983f20e4c912d'

    # Headers for the authentication request
    auth_headers: dict = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Body of the authentication request
    auth_body: dict = {
        'grant_type': 'client_credentials',  # Type of authentication
        'client_id': client_id,  # Client ID
        'client_secret': client_secret,  # Client secret
    }

    # Endpoint for the authentication request
    auth_endpoint: str = 'https://accounts.spotify.com/api/token'

    # Send a POST request to the authentication endpoint with the headers and body
    auth_response = requests.post(
        auth_endpoint, data=auth_body, headers=auth_headers)

    # Extract the access token and token type from the response
    access_token: str = auth_response.json()['access_token']
    token_type: str = auth_response.json()['token_type']

    # Return the access token with the token type
    return f'{token_type} {access_token}'


def get_playlist_info(id: str, token: str) -> dict:
    """
    Retrieves information about a Spotify playlist.

    Args:
        id (str): The ID of the playlist (str).
        token (str): The access token for authentication (str).

    Returns:
        dict: A dictionary containing the name (str) and total number of tracks (int) in the playlist (dict).
    """

    # Construct the endpoint URL for the playlist information
    playlist_endpoint = (
        f'https://api.spotify.com/v1/playlists/{id}?market=BR&fields=name%2Ctracks.total')

    # Send a GET request to the playlist endpoint with the authorization token
    playlist = requests.get(playlist_endpoint, headers={
                            'Authorization': token})

    # Check if the request was successful
    if playlist.status_code == 200:
        # Parse the response JSON and return the data
        data = playlist.json()
        return {'name': data['name'], 'total': data['tracks']['total']}


def get_playlist_tracks(
    id: str,
    token: str,
    total: int
) -> list[dict[str, any]]:
    """
    Retrieves tracks from a Spotify playlist.

    Args:
        id (str): The ID of the playlist.
        token (str): The access token for authentication.
        total (int): The total number of tracks in the playlist.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing information about the tracks.
    """
    # Initialize variables
    offset = 0
    tracks: list[dict[str, any]] = []

    # Iterate over the playlist in batches of 50 tracks
    for i in range(int(total / 50) + 1):
        offset = 50 * i

        # Construct the endpoint URL for the tracks
        tracks_endpoint = (
            f'https://api.spotify.com/v1/playlists/{id}/tracks'
            f'?market=BR&fields=items.track.name%2Citems.track.artists.name&limit=50&offset={int(offset)}'
        )

        # Send a GET request to the tracks endpoint with the authorization token
        actual_tracks = requests.get(tracks_endpoint, headers={
                                     'Authorization': token})

        # Check if the request was successful
        if actual_tracks.status_code == 200:
            # Merge the retrieved tracks with the existing tracks
            tracks.extend(actual_tracks.json()['items'])

    # Return the list of tracks
    return tracks


def make_search_names(tracks: list[dict]) -> list[str]:
    """
    Generate a list of search names for tracks.

    Args:
        tracks (list[dict]): A list of dictionaries containing information about the tracks.

    Returns:
        list[str]: A list of search names.
    """
    # Generate a search name for each track by concatenating the artist name and track name
    # with a hyphen in between.
    return [
        f'{track["track"]["artists"][0]["name"]} - {track["track"]["name"]}'
        for track in tracks
    ]


def search_and_download(index: int, search_value: str, path: str, artist: str, trackname: str) -> None:
    """
    Searches for a YouTube video corresponding to the given name and downloads the audio.

    Args:
        index (int): The index of the track in the playlist.
        search_value (str): The string that will be used to search for the YouTube video.
        path (str): The path to the directory where the audio file will be saved.
        artist (str): The name of the artist.
        trackname (str): The name of the track.

    Returns:
        None
    """
    # Search for the YouTube video corresponding to the given name
    pesquisa: Search = Search(search_value)

    try:
        # Get the first result from the search and download the audio
        video: YouTube = pesquisa.results[0]
        audio: pytube.Stream = video.streams.get_audio_only()
        audio.download(
            output_path=path,
            filename_prefix=f'{index+1} - ',
            filename=treat_trackname(artist, trackname)
        )
    except:
        # If there is an error, display a popup message
        sg.popup(
            f'Error to download the track {search_value}.\n'
            'Probably an inacessible YouTube video.\n\n'
            'Press Ok to continue',
            title='SpotiTube Downloader'
        )


def treat_trackname(artist: str, trackname: str) -> str:
    """
    Removes special characters from the track name and artist name to create a valid file name.

    Args:
        artist (str): The name of the artist.
        trackname (str): The name of the track.

    Returns:
        str: The track name with the artist name and '.mp3' extension.
    """
    # Create the initial file name by concatenating the artist name and track name
    name: str = f'{artist} - {trackname}.mp3'

    # Remove special characters from the file name
    name = name.replace('/', '')
    name = name.replace('?', '')
    name = name.replace(':', '')
    name = name.replace('"', '')
    name = name.replace('<', '')
    name = name.replace('>', '')
    name = name.replace('|', '')
    name = name.replace('\\', '')

    return name


def main() -> None:
    """
    Initializes the GUI window and handles user events.

    Returns:
        None
    """
    sg.theme('Green')
    token: str = spotify_auth()

    layout: list[list[sg.Element]] = [
        [sg.Text('Save path:', size=(10,1)), sg.InputText(key='-PATH-'), sg.FolderBrowse()],
        [sg.Text('Playlist link:', size=(10,1)), sg.InputText(key='-LINK-')],
        [sg.HorizontalSeparator()],
        [sg.Text('', key='-OUTPUT-', visible=False)],
        [sg.ProgressBar(100, orientation='h', size=(1, 20),
                        key='progress_bar', visible=False, expand_x=True,
                        bar_color='red', style='black.Horizontal.TProgressbar')],
        [sg.Button('Download')]
    ]

    window: sg.Window = sg.Window('SpotiTube Downloader', layout,
                                  icon='spotitube.ico', progress_bar_color='red')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Download':
            playlist_link: str = values['-LINK-']
            if not playlist_link.startswith('https://open.spotify.com/playlist/'):
                sg.popup('Invalid playlist link!', icon='spotitube.ico')
                continue

            playlist: any[dict[str, any]] = get_playlist_info(
                playlist_link[34:56], token)
            if playlist is None:
                sg.popup('Invalid playlist link!', icon='spotitube.ico')
                continue

            path: str = os.path.join(values['-PATH-'], playlist['name'])
            if os.path.exists(path):
                sg.popup('Directory already exists!')
                continue

            os.makedirs(path, exist_ok=True)
            download_playlist(window, playlist_link, playlist, token, path)


def download_playlist(window: sg.Window, playlist_link: str, playlist: dict, token: str, path: str) -> None:
    """
    Downloads a Spotify playlist to a specified path.

    Args:
        window (sg.Window): The GUI window.
        playlist_link (str): The link to the Spotify playlist.
        token (str): The access token for authentication.
        path (str): The path to save the playlist.
    """
    tracks = get_playlist_tracks(
        playlist_link[34:56], token, playlist['total'])
    search_names = make_search_names(tracks)
    window['progress_bar'].update(visible=True)
    window['-OUTPUT-'].update(visible=True)
    window['Download'].update(disabled=True)

    for index, name in enumerate(search_names):
        window['-OUTPUT-'].update(value=f'Downloading: {name}')
        window['progress_bar'].update(
            current_count=(index + 1) * 100 / len(search_names))
        window.refresh()
        search_and_download(
            index,
            name,
            path,
            tracks[index]["track"]["artists"][0]["name"],
            tracks[index]["track"]["name"]
        )

    sg.popup('Download completed!', icon='spotitube.ico')
    reset_window(window)


def reset_window(window: sg.Window) -> None:
    """
    Resets the GUI window.

    Args:
        window (sg.Window): The GUI window.
    """
    window['Download'].update(disabled=False)
    window['-OUTPUT-'].update(visible=False)
    window['progress_bar'].update(visible=False)
    window['-PATH-'].update('')
    window['-LINK-'].update('')
    window.refresh()


if __name__ == '__main__':
    main()


# pyinstaller "spotitube.py" -F -i "data/icon.ico" -n SpotiTube --windowed