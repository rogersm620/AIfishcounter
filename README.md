# 🐟 Fry Counter

A mobile-friendly web app that uses Claude AI to count juvenile fish fry from a photo or live camera feed.

---

## Setup Instructions

### Step 1 — Get your Anthropic API key
1. Go to https://console.anthropic.com
2. Sign in or create a free account
3. Click **API Keys** in the left sidebar
4. Click **Create Key**, give it a name, and copy the key somewhere safe

---

### Step 2 — Put the code on GitHub
1. Go to https://github.com and sign in (or create a free account)
2. Click the **+** icon → **New repository**
3. Name it `fry-counter`, set it to **Private**, click **Create repository**
4. On the next page, click **uploading an existing file**
5. Upload all files from this folder:
   - `server.py`
   - `render.yaml`
   - `requirements.txt`
   - `static/index.html` (create a `static` folder first by including the path)
6. Click **Commit changes**

---

### Step 3 — Deploy on Render.com
1. Go to https://render.com and sign in (or create a free account — no credit card needed)
2. Click **New +** → **Web Service**
3. Click **Connect a Git repository** and connect your GitHub account
4. Select your `fry-counter` repository
5. Render will auto-detect the settings from `render.yaml`. Click **Create Web Service**
6. On the next screen, find the **Environment** section
7. Click **Add Environment Variable**:
   - Key: `ANTHROPIC_API_KEY`
   - Value: (paste your API key from Step 1)
8. Click **Save** — Render will deploy your app (takes ~1 minute)
9. Once deployed, you'll see a URL like `https://fry-counter-xxxx.onrender.com`

---

### Step 4 — Use it on your phone
1. Open the URL from Step 3 in your phone's browser (Chrome or Safari)
2. Tap **camera** and allow camera access when prompted
3. Point your phone straight down over the fry bucket
4. Tap **snap** then **count fry** — or tap **live** for automatic counting every 5 seconds
5. You can also tap **upload a photo** to count from a saved image

---

## Tips for best counts
- Point the camera **straight down** at the bucket — avoid angles
- Good overhead lighting helps significantly
- Avoid glare or reflections on the water surface
- For very large numbers (500+), counts are approximate

## Running locally (optional)
If you want to run it on your own computer instead of Render:
```
export ANTHROPIC_API_KEY=your_key_here
python server.py
```
Then open http://localhost:8000 in your browser.
