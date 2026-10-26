# 📱 Samsung Galaxy S25 FE – Instagram Reels Scrubbing Glitch Fix

Fixes the neon pink/white blocky pixelation and frame-buffer corruption that happens when fast-forwarding or scrubbing through Instagram Reels on the **Samsung Galaxy S25 FE** (and other Exynos devices)[cite: 1].

## 🚀 Patch Online in Your Phone Browser (No PC or Root Needed)

Click the **Open in Colab** button below to patch any official Instagram `.apkm` right in your mobile or desktop browser using Google's free cloud servers:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Sanu0121/s25fe-instagram-reels-fix/blob/main/S25FE_Instagram_Patcher.ipynb)

---

## 🔍 Why This Glitch Happens
Instagram serves heavily compressed 10-bit AV1 (`video/av01`) video streams for Reels. When you drag the progress bar rapidly between keyframes, the Galaxy S25 FE's hardware video decoder (`c2.exynos.av1.decoder`) fails to flush the previous frame buffer and loses color-space sync, causing the video layer to break up into pink and white blocks[cite: 1].

## 🛠️ How This Fix Works (Zero Mod Bloat)
Unlike third-party mods or patch managers (like Morphe/ReVanced) that inject extra `.dex` files and hook frameworks that Meta's anti-bot security actively flags, this script performs a **pure 10-byte in-place string replacement** inside the official Instagram APK:
* Replaces `video/av01` with `video/av00` (forcing Instagram to request clean, standard **H.264 / VP9** video streams from Meta's servers).
* Replaces `c2.exynos.` with `c2.android` as a fallback.
* **Zero added classes, zero mod menus, and identical DEX file sizes to official Instagram.**
* Generates a **unique, private signing key (`my-instagram.jks`)** just for your phone so you don't share an APK signature with anyone else.

---

## 📋 Step-by-Step Instructions (On Your Phone)

### Step 1: Download Stock Instagram from APKMirror
1. Go to **[APKMirror (Instagram)](https://www.apkmirror.com/apk/instagram/instagram-instagram/)** in your phone browser.
2. Download the latest stable **`.apkm` bundle** (`arm64-v8a`, `nodpi` or `480-640dpi`).

### Step 2: Run the 1-Click Google Colab Patcher
1. Tap the **[Open in Colab](https://colab.research.google.com/github/YOUR_GITHUB_USERNAME/s25fe-instagram-reels-fix/blob/main/S25FE_Instagram_Patcher.ipynb)** button at the top of this page (sign into any Google account if prompted).
2. Tap the **Play button (▶️)** next to *"Tap the Play Button Here to Upload & Patch Instagram"*. *(If a pop-up says "This notebook was not authored by Google", tap **Run anyway**).*
3. Tap the **Choose Files** button that appears beneath the cell and select your downloaded **Instagram `.apkm`** file.
4. Wait ~60 seconds while the cloud server uploads, merges, patches, and signs your APK.
5. Your browser will automatically download **two files** to your phone:
   * **`instagram-s25fe-fixed.apk`** (your fixed Instagram app)
   * **`my-instagram.jks`** (your personal cryptographic signing key — **keep this file safe!**)

### Step 3: Install on Your Galaxy S25 FE
1. **Temporarily turn off Samsung Auto Blocker:** Go to **Settings > Security and privacy > Auto Blocker** and toggle it **Off** (required by One UI to install apps outside the Play Store).
2. **Choose how you want to install it:**
   * **Option A (Safest for Main Account — Dual Install via Secure Folder):** Keep the official Play Store Instagram on your home screen, copy `instagram-s25fe-fixed.apk` into **Samsung Secure Folder**, and install it there.
   * **Option B (Main Profile Install):** Uninstall the Play Store Instagram app, then tap `instagram-s25fe-fixed.apk` in your phone's **My Files > Downloads** folder to install it. *(If Google Play Protect prompts you, tap **More details > Install anyway**).*
3. **Disable Play Store Auto-Updates:** Open the Google Play Store $\rightarrow$ search **Instagram** $\rightarrow$ tap the **three dots (⋮)** in the top right $\rightarrow$ uncheck **Enable auto update**.

---

## 🔄 The Golden Rule for Future Updates (Never Uninstall Again!)
Whenever you want to update Instagram in the future:
1. **Do NOT uninstall Instagram from your phone.** Uninstalling resets your Android App ID and forces a fresh login, which can trigger Instagram's automated video-selfie bot verification.
2. Open the Google Colab link, tap **Play (▶️)**, and when you tap **Choose Files**, select **BOTH** the new Instagram `.apkm` **AND** the **`my-instagram.jks`** file you saved from your first run.
3. Because the script signs the new version with your exact same `my-instagram.jks` key, you can install the new `instagram-s25fe-fixed.apk` **directly on top** of your existing app as a normal update without ever logging out!
