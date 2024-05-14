# Imports
import requests
import webbrowser

# Local Imports
import flaskController as flCon


def internetConnection():
    """Checks if current user has access to the internet by requesting a response from cloudflare.

    Returns:
        Bool: Bool for if internet is connected or not.
    """

    try:
        response = requests.get("https://1.1.1.1", timeout=5)
        return True
    except requests.ConnectionError:
        return False
   
def main():
    """Main start and terminator for program. 
    Checks for certain params to be true in order to control startup and shutdown.
    """
    
    if (internetConnection()):
        print("INFO: Internet Connection Verified.")
    else:
        print("ERR: Unable to establish an internet connection, please verify connection and ad-blockers.")
        exit()
        
    flCon.init()

if __name__ == '__main__':
    main()