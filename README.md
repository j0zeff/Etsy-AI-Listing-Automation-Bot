# Etsy AI Listing Automation Bot 🤖🛍️

An advanced, asynchronous Telegram bot designed to automate the creation of Etsy product listings. By leveraging a multi-agent AI system, the bot analyzes product images and user descriptions to generate highly optimized SEO titles, descriptions, and tags, and automatically exports them as drafts to your Etsy shop using the Etsy API v3.

---

## 🚀 Key Features

* **Lightweight & Streamlined Setup:** Efficient execution with the Telegram bot polling and CrewAI multi-agent orchestration contained within `main.py` for rapid deployment and easy debugging.
* **3-Agent AI Ensemble:** Three specialized CrewAI agents collaborate to transform raw user input into a marketplace-ready Etsy listing.
* **Smart Image Processing:** Integrated background removal (`rembg`) and automatic ranking/sorting for primary and additional listing photos.
* **Robust Etsy API v3 Integration:** Custom API client wrapper featuring **automatic OAuth token refresh** (handles `401 Unauthorized` states on the fly).
* **Secure Session Handling:** Local encrypted token management storing access and rolling refresh tokens securely in `tokens.json`.

---

## 🤖 The 3-Agent AI System

The multi-agent workflow utilizes exactly **three specialized agents** acting as a digital product launch team:

| Agent Name | Role | Core Responsibility |
| :--- | :--- | :--- |
| **Product Analyst Agent** | Research & Extraction | Analyzes raw input text and images to extract core product features, materials, and unique selling points. |
| **Etsy SEO & Copywriter** | SEO Optimization | Crafts an engaging, conversion-focused title (under 140 characters) and a detailed description while generating 13 high-traffic search tags. |
| **Quality Assurance (QA)** | Validation & Formatting | Validates output constraints, ensures tags strictly comply with Etsy policies, and formats the final payload into a clean, parseable JSON object. |

---

## 📁 Project Structure

```text
Etsy-AI-Listing-Automation-Bot/
│
├── main.py                 # Core application: Telegram bot handlers & CrewAI setup
├── etsy_api.py             # Custom Etsy API V3 client wrapper with token auto-refresh
├── requirements.txt        # Production dependencies
├── tokens.json             # App-generated OAuth sessions (DO NOT COMMIT)
└── README.md               # Project documentation
```
## 🛠️ Installation & Setup

### 1. Clone the Repository

git clone [https://github.com/yourusername/Etsy-AI-Listing-Automation-Bot.git](https://github.com/yourusername/Etsy-AI-Listing-Automation-Bot.git)

### 2. Configure Environment Variables
Create a new file named '.env' in the root directory of the project and add the following required keys:
- GEMINI_API_KEY="_your_api_key_"
- TELEGRAM_BOT_TOKEN="_your_token_"
- ETSY_CLIENT_ID="_etsy_client_id_"
- ETSY_SHARED_SECRET="_shared_key_"
- ETSY_REDIRECT_URI="_redirect_uri_"
- ETSY_SHOP_ID="_etsy_shop_id_"
- ALLOWED_USERS_ID=[_user_id_]

### 3. Install Dependencies
Make sure your virtual environment is active, then run:
```bash
pip install -r requirements.txt
```

### 📦 Usage
Start the bot by executing:
```bash
python main.py
```

Open your Telegram bot and type ```/start```.

Send a photo or an album of your product. Make sure to include your raw product description inside the caption of the message.

The bot will automatically:

- Process and prepare the images.

- Run the 3-agent CrewAI brainstorm to generate optimized SEO details.

- Connect to Etsy, create a listing draft, and upload the photos with corresponding display ranks.

## 🔒 Security Note
Never commit your ```.env``` file to version control. It contain highly sensitive credentials capable of managing your live Etsy storefront. Ensure you have a standard ```.gitignore``` file configured to exclude it.
