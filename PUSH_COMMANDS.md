# Push to GitHub - Ready to Run

## After you get your Personal Access Token:

Replace `YOUR_TOKEN_HERE` below with your actual token and run:

```bash
cd /Users/evanwyloge/snow-conditions-data

# Remove old remote
git remote remove origin

# Add remote with token
git remote add origin https://YOUR_TOKEN_HERE@github.com/gazette-evn/colorado-snow-conditions.git

# Push
git push -u origin main
```

## Or use credential helper:

```bash
cd /Users/evanwyloge/snow-conditions-data

# Store credentials
git config credential.helper store

# Push (will prompt for username and token)
git push -u origin main
```

When prompted:
- **Username:** gazette-evn
- **Password:** [paste your token]

---

## Get Your Token Here:
https://github.com/settings/tokens

Scopes needed:
- ✅ repo
- ✅ workflow

---

Once pushed, go to:
https://github.com/gazette-evn/colorado-snow-conditions/actions

And run the "Test Colorado Ski Scraper" workflow!

