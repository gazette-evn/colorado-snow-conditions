# How to Debug Mapbox Style Caching Issue

## Step 1: Check What's Actually Loading

1. Open your site in a NEW incognito window: https://gazette-evn.github.io/colorado-snow-conditions
2. Press `F12` or `Cmd+Option+I` (Mac) to open Developer Tools
3. Go to **Network** tab
4. Check "Disable cache"
5. Refresh the page (`Cmd+R`)
6. Look for requests to `api.mapbox.com` or `mapbox://`
7. Check if you see the style ID: `cmi25lrgp00nf01sug74vg0pt`

## Step 2: Force Clear Everything

### Chrome/Edge/Brave:
1. Go to: `chrome://settings/clearBrowserData`
2. Select "All time"
3. Check ONLY:
   - Cached images and files
   - Hosted app data
4. Click "Clear data"
5. Close browser completely
6. Reopen in incognito

### Safari:
1. Develop menu → Empty Caches
2. Or: Safari → Clear History → All History
3. Close browser completely
4. Reopen in private window

## Step 3: Check GitHub Pages Deployment

Go to: https://github.com/gazette-evn/colorado-snow-conditions/actions

Look for the LATEST workflow run (should be from commit `83532d7`).

If it's not complete yet, WAIT for it to finish before testing.

## Step 4: Nuclear Option - Version the Style URL

If nothing else works, we can add a version parameter to force a fresh load.

This would change the map initialization to force-fetch the style.

