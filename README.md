## 🤖 HappyRobot Backend

HappyRobot is the backend service for an AI-powered phone call assistant. It’s built with **FastAPI**, supports querying available loads, and logs call outcomes directly to **Google Sheets**.

## 🚀 Deploying to Render

### 1. Clone this repository

``` bash
git clone https://github.com/cmartingu/HappyRobot.git
cd HappyRobot
```

## 2 . Create a new service on Render
Go to https://dashboard.render.com/

Click New + → Web Service

Connect your GitHub repo

Configure the service:
- Runtime: Docker
- Build Command: (leave empty)
- Start Command: (Render will use the CMD from your Dockerfile)
- Region: Choose the closest to your users
- Branch: main

## 3. Environment Variables
Add the following to the Render environment:

GOOGLE_CREDS_JSON: your Google service account credentials (as a full JSON string)

SPREADSHEET_ID: the ID of the Google Sheet where logs will be stored

API_KEY: your custom API key used for protecting all endpoints

✅ Make sure the Google service account has editor access to the Google Sheet.




## 🧱 API Endpoints
| Method | Endpoint                   | Description                                    |
| ------ | -------------------------- | ---------------------------------------------- |
| GET    | `/search_loads`            | Returns a random load or filtered by equipment |
| GET    | `/search_loads/{phy_city}` | Returns the closest load to the specified city |
| POST   | `/log_result`              | Logs call result to Google Sheets              |


🔐 All endpoints require an API key via the header x-api-key.

📌 Example curl test
```bash
curl -X POST https://happyrobot.onrender.com/log_result \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"carrier_name": "John D. Trucking", "agreed_rate": 1550, "load_id": "L003", "sentiment": "positive", "outcome": "deal_closed"}'
```

## 🐳 Docker
This project includes a Dockerfile and is ready to run on any container-based deployment.

## 📊 Output
The log_result POST endpoint will write a new row to your Google Sheet with:
- Timestamp
- Carrier name
- Agreed rate
- Load ID
- Sentiment
- Outcome

