# Kalshi API Setup Guide

This guide will help you get access to the Kalshi API for fetching real prediction market data.

## 🔑 Getting API Access

### Step 1: Create a Kalshi Account

1. Go to [kalshi.com](https://kalshi.com)
2. Click "Sign Up" and create an account
3. Complete the account verification process
4. You may need to provide identity verification depending on your location

### Step 2: Generate API Keys

1. **Log into your Kalshi account**
2. **Navigate to Account Settings**
   - Click on your profile/account icon
   - Select "Account Settings" or "API Keys"
3. **Create a New API Key**
   - Look for "API Keys" section
   - Click "Create New API Key" or "Generate API Key"
   - Give it a descriptive name (e.g., "NFL Analysis")
4. **⚠️ IMPORTANT: Save Your Credentials**
   - Copy the **Key ID** (this is your API key)
   - Copy the **Private Key** (this is your private key in PEM format)
   - **You cannot retrieve the private key later!** Save it securely

### Step 3: Configure Your Credentials

1. **Edit the configuration file:**
   ```bash
   nano kalshi_config.py
   ```

2. **Add your credentials:**
   ```python
   # Replace with your actual credentials
   KALSHI_API_KEY = "your_actual_key_id_here"
   KALSHI_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
   your_actual_private_key_content_here
   -----END PRIVATE KEY-----"""
   
   # Set to False to use real API
   USE_MOCK_DATA = False
   ```

3. **Save the file**

### Step 4: Test Your Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Test API connection
python3 scripts/data/test_kalshi_api.py

# Run data fetch with real API
python3 run_kalshi_fetch.py
```

## 🔒 Security Best Practices

### Protecting Your Credentials

1. **Never commit credentials to git:**
   ```bash
   # Add to .gitignore
   echo "kalshi_config.py" >> .gitignore
   ```

2. **Use environment variables (recommended):**
   ```python
   import os
   
   KALSHI_API_KEY = os.getenv('KALSHI_API_KEY')
   KALSHI_PRIVATE_KEY = os.getenv('KALSHI_PRIVATE_KEY')
   ```

3. **Set environment variables:**
   ```bash
   export KALSHI_API_KEY="your_key_id"
   export KALSHI_PRIVATE_KEY="your_private_key"
   ```

### Alternative: Environment Variables Setup

Create a `.env` file (don't commit to git):
```bash
# .env file
KALSHI_API_KEY=your_key_id_here
KALSHI_PRIVATE_KEY=your_private_key_here
USE_MOCK_DATA=False
```

Then update `kalshi_config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

KALSHI_API_KEY = os.getenv('KALSHI_API_KEY')
KALSHI_PRIVATE_KEY = os.getenv('KALSHI_PRIVATE_KEY')
USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'True').lower() == 'true'
```

## 🚨 Troubleshooting

### Common Issues

1. **"Invalid signature" error:**
   - Check that your private key is in correct PEM format
   - Ensure no extra spaces or characters in the key
   - Verify the key ID matches your account

2. **"Access denied" error:**
   - Verify your account is fully verified
   - Check that API access is enabled for your account
   - Some features may require account approval

3. **"Rate limit exceeded" error:**
   - The script includes built-in rate limiting
   - Kalshi has API rate limits (check their documentation)
   - Consider adding delays between requests

4. **Network connectivity issues:**
   - Check your internet connection
   - Verify you can access kalshi.com
   - Some corporate networks may block API access

### Getting Help

1. **Kalshi Documentation:** [docs.kalshi.com](https://docs.kalshi.com)
2. **Kalshi Discord:** Join their Discord server and check the `#dev` channel
3. **Support:** Contact Kalshi support through their website

## 📊 What You'll Get

With real API access, you'll be able to:

- **Fetch live market data** for NFL games
- **Get historical odds** from 2021-2024 seasons
- **Track probability changes** in real-time
- **Compare Kalshi vs Vegas** odds
- **Analyze market efficiency** and overreactions

## 🔄 Switching Between Mock and Real Data

### Using Mock Data (Default)
```python
# In kalshi_config.py
USE_MOCK_DATA = True
```

### Using Real API Data
```python
# In kalshi_config.py
USE_MOCK_DATA = False
KALSHI_API_KEY = "your_key_here"
KALSHI_PRIVATE_KEY = "your_private_key_here"
```

The script will automatically detect your configuration and use the appropriate data source.

## 📈 Next Steps

Once you have API access:

1. **Run the data fetch:**
   ```bash
   python3 run_kalshi_fetch.py    # Fetch Kalshi data
   ```

2. **Explore the results:**
   - Check `results/data/kalshi_nfl_data.csv`
   - View generated visualizations in `visualizations/`
   - Run the dashboard: `streamlit run dashboard.py`

3. **Customize your analysis:**
   - Modify the analysis scripts for your specific needs
   - Add new market types or time periods
   - Create custom visualizations
