> ## ⚠️ CRITICAL ACCOUNT SAFETY WARNING (DO NOT USE ON MAIN ACCOUNTS)
> **Update (October 2026):** Extended stability testing confirmed that even a pure 10-byte binary patch with zero third-party frameworks (no Morphe/ReVanced code) eventually triggers **Meta's automated video-selfie bot verification (~24–30 hours after login)**.
> 
> **Why?** Instagram v450+ enforces strict **Google Play Integrity (`appRecognitionVerdict`)** checks on the APK's cryptographic signature. Because Android requires any modified APK on a non-rooted device to be re-signed with a custom key, Meta's servers flag the custom certificate hash as an `UNRECOGNIZED_VERSION`.
> 
> **Recommendation:** Do **NOT** log into a re-signed Instagram APK with an account you care about. This repository is preserved strictly for technical reference demonstrating that the Galaxy S25 FE's Reels scrubbing glitch is caused by `c2.exynos.av1.decoder` failing on 10-bit `video/av01` streams.

# 📱 Samsung Galaxy S25 FE – Instagram Reels Scrubbing Glitch Fix

Fixes the neon pink/white blocky pixelation and frame-buffer corruption that happens when fast-forwarding or scrubbing through Instagram Reels on the **Samsung Galaxy S25 FE** (and other Exynos devices).

## 🚀 Method 1: Patch in Your Phone Browser (Google Colab — No PC Needed)

Click the **Open in Colab** button below to patch any official Instagram `.apkm` directly in your mobile or desktop browser:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Sanu0121/s25fe-instagram-reels-fix/blob/main/S25FE_Instagram_Patcher.ipynb)

### Step-by-Step (Phone Browser):
1. **Download Stock Instagram:** Go to **[APKMirror (Instagram)](https://www.apkmirror.com/apk/instagram/instagram-instagram/)** and download the latest stable **`.apkm` bundle** (`arm64-v8a`, `nodpi` or `480-640dpi`).
2. **Open the Cloud Patcher:** Tap the **[Open in Colab](https://colab.research.google.com/github/Sanu0121/s25fe-instagram-reels-fix/blob/main/S25FE_Instagram_Patcher.ipynb)** button above and tap the **Play button (▶️)**. *(If prompted "This notebook was not authored by Google", tap **Run anyway**).*
3. **Upload Box 1 (Required):** Tap **Choose Files** and select your downloaded **Instagram `.apkm`** file.
4. **Upload Box 2 (Optional Keystore for Updates):**
   * **First-time users:** Simply tap **Cancel upload**! The script will generate a brand-new `my-instagram.jks` key for you and download both `instagram-s25fe-fixed.apk` and `my-instagram.jks` to your phone when finished.
   * **Updating users:** Tap **Choose Files** and select the **`my-instagram.jks`** file you saved from your first run so your updated APK matches your existing signature.

---

## 💻 Method 2: Offline PC Patcher (`patch_instagram.py`)

Prefer to patch locally on your Windows, Mac, or Linux PC without using Google Colab?

### Prerequisites:
* **Python 3** (`python --version`)
* **Java JDK 8+** (`java -version` and `keytool` in PATH)

### Step-by-Step (Offline PC):
1. Create a folder on your PC and download **[`patch_instagram.py`](./patch_instagram.py)** into it.
2. Download the latest stock **Instagram `.apkm` (`arm64-v8a`)** from APKMirror and drop it into that same folder.
3. Open a terminal / Command Prompt in that folder and run:
   ```bash
   python patch_instagram.py
