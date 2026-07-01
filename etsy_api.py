import os
import json
import requests
from pathlib import Path

class EtsyAPIClient:
    def __init__(self, shop_id: str, tokens_file: str = "tokens.json"):
        """
        shop_id: Etsy shop ID.
        tokens_file: Path to the JSON file storing OAuth tokens.
        """
        self.shop_id = shop_id
        
        current_dir = Path(__file__).resolve().parent
        self.tokens_file = current_dir / tokens_file
        
        self.base_url = "https://openapi.etsy.com/v3/application"
        self.tokens = self._load_tokens()
        
        # Fetch credentials from environment variables and strip trailing spaces
        keystring = os.environ.get("ETSY_CLIENT_ID", "").strip()
        shared_secret = os.environ.get("ETSY_SHARED_SECRET", "").strip()

        self.client_id = f"{keystring}:{shared_secret}"
        
        self.headers = {
            "x-api-key": self.client_id,
            "Authorization": f"Bearer {self.tokens.get('access_token')}"
        }

    def _load_tokens(self) -> dict:
        """Loads OAuth tokens from the tokens.json file."""
        if self.tokens_file.exists():
            with open(self.tokens_file, "r") as f:
                return json.load(f)
        raise FileNotFoundError(f"Tokens file not found at {self.tokens_file}. Please ensure it exists.")

    def _save_tokens(self, tokens: dict):
        """Saves new OAuth tokens to the tokens.json file."""
        with open(self.tokens_file, "w") as f:
            json.dump(tokens, f, indent=4)
        self.tokens = tokens
        
        # Update the Authorization header for the current instance
        self.headers["Authorization"] = f"Bearer {tokens.get('access_token')}"
        print("🔄 [Etsy API] Tokens successfully updated and saved to file.")

    def refresh_access_token(self):
        """Refreshes the access_token using the stored refresh_token."""
        print("🔄 [Etsy API] Attempting to refresh Access Token...")
        refresh_url = "https://api.etsy.com/v3/public/oauth/token"
        
        headers = {
            "Content-Type": "application/json"
        }

        # Extract the keystring component from the client_id
        pure_client_id = self.client_id.split(":")[0]

        payload = { 
            "grant_type": "refresh_token",
            "client_id": pure_client_id,
            "refresh_token": self.tokens.get("refresh_token")
        }
        
        response = requests.post(refresh_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            new_tokens = response.json()
            self._save_tokens({
                "access_token": new_tokens.get("access_token"),
                "refresh_token": new_tokens.get("refresh_token")
            })
        else:
            print(f"❌ [Etsy API] Token refresh failed (Status code {response.status_code}):")
            print(response.text)
            raise Exception("Failed to refresh OAuth token. The refresh_token may have expired (30-day validity period).")
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """A wrapper around requests with automatic OAuth token refresh."""
        
        # Attempt the request with the current token
        response = requests.request(method, url, headers=self.headers, **kwargs)
        
        # 401 Unauthorized indicates that the 2-hour access token has expired
        if response.status_code == 401:
            print("⚠️ [Etsy API] Expired token detected (401). Initiating auto-refresh...")
            self.refresh_access_token()
            
            # Retry the request with the newly updated token
            response = requests.request(method, url, headers=self.headers, **kwargs)
            
        return response

    def create_draft_listing(self, title: str, description: str, tags: list, price: float = 15.0, quantity: int = 1, taxonomy_id: int = 1326) -> str:
        """Creates a draft listing on Etsy populated with tags and materials."""
        url = f"{self.base_url}/shops/{self.shop_id}/listings"
        
        payload = {
            "title": title,
            "description": description,
            "price": price,
            "quantity": quantity,
            "taxonomy_id": taxonomy_id,
            "who_made": "i_did", 
            "when_made": "2020_2026", 
            "is_supply": False, 
            "state": "draft",
            "shipping_profile_id": 296799540562,
            "readiness_state_id": 1456970168089,
            "materials": ["polymer clay", "uv resin"],
            "tags": tags 
        }
        
        print(f"🚀 [Etsy API] Creating draft listing: {title[:30]}...")
        
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        
        response = requests.request("POST", url, headers=headers, json=payload)
        
        if response.status_code == 201:
            listing_data = response.json()
            listing_id = listing_data.get("listing_id")
            print(f"✅ Draft created successfully! Listing ID: {listing_id}")
            return str(listing_id)
        else:
            print(f"❌ Listing creation failed (Status code {response.status_code}):")
            print(response.text)
            raise Exception(f"Failed to create draft on Etsy: {response.text}")

    def upload_listing_image(self, listing_id: str, image_path: str, rank: int = 1):
        """Uploads an image to a specific Etsy listing."""
        url = f"{self.base_url}/shops/{self.shop_id}/listings/{listing_id}/images"
        path = Path(image_path)
        
        if not path.exists():
            print(f"⚠️ File {image_path} not found for upload.")
            return

        print(f"📸 [Etsy API] Uploading image {path.name} (Rank: {rank})...")
        content_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        
        with open(path, "rb") as img_file:
            files = {
                "image": (path.name, img_file, content_type)
            }
            data = {
                "rank": rank
            }
            
            # Use the request wrapper to handle automatic token refresh
            response = self._make_request("POST", url, data=data, files=files)
            
            if response.status_code == 201:
                print(f"✅ Image {path.name} uploaded successfully!")
            else:
                print(f"❌ Failed to upload image {path.name} (Status code {response.status_code}):")
                print(response.text)
                raise Exception(f"Failed to upload image {path.name}: {response.text}")

    def get_and_save_taxonomy(self):
        """Fetches all Etsy seller taxonomy nodes and saves them to a local JSON file."""
        url = f"{self.base_url}/seller-taxonomy/nodes"
        response = self._make_request("GET", url)
        
        if response.status_code == 200:
            with open("etsy_categories.json", "w", encoding="utf-8") as f:
                json.dump(response.json(), f, indent=4, ensure_ascii=False)
            print("📁 All categories successfully saved to etsy_categories.json")
        else:
            print(f"❌ Failed to fetch categories: {response.text}")