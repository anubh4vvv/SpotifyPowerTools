from services.spotify_api import get_spotify_client

sp = get_spotify_client()

me = sp.current_user()

print("Logged in as:")
print("Display name:", me.get("display_name"))
print("User ID:", me.get("id"))
print("Email:", me.get("email"))

token = sp.auth_manager.get_cached_token()

print("\nToken scopes:")
print(token.get("scope"))