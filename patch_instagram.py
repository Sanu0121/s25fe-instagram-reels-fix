#!/usr/bin/env python3
"""
Samsung Galaxy S25 FE - Offline PC Instagram Reels Glitch Patcher
Fixes the pink/white macroblocking glitch when scrubbing Reels on Exynos devices
by replacing 'video/av01' -> 'video/av00' and 'c2.exynos.' -> 'c2.android' in-place.
"""

import os
import sys
import glob
import struct
import zlib
import hashlib
import zipfile
import subprocess
import urllib.request

APKEDITOR_URL = "https://github.com/REAndroid/APKEditor/releases/download/V1.4.9/APKEditor-1.4.9.jar"
UBERSIGNER_URL = "https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar"

APKEDITOR_JAR = "APKEditor.jar"
UBERSIGNER_JAR = "uber-apk-signer.jar"
KEYSTORE_FILE = "my-instagram.jks"

def ensure_tool(url: str, filename: str):
    if not os.path.exists(filename):
        print(f"[*] '{filename}' not found locally. Downloading once for offline use...")
        try:
            urllib.request.urlretrieve(url, filename)
            print(f"    Saved {filename} (future runs will work 100% offline).")
        except Exception as e:
            print(f"\n[!] Failed to download {filename}: {e}")
            print(f"    For strictly offline setup, manually download:\n    {url}\n    and save it in this folder as '{filename}'.")
            sys.exit(1)

def ensure_keystore():
    if not os.path.exists(KEYSTORE_FILE):
        print(f"[*] Generating your personal signing key ({KEYSTORE_FILE})...")
        subprocess.run([
            "keytool", "-genkeypair", "-v",
            "-keystore", KEYSTORE_FILE,
            "-alias", "igkey",
            "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
            "-storepass", "instagram123", "-keypass", "instagram123",
            "-dname", "CN=User, OU=Mobile, O=Personal, L=City, S=State, C=US"
        ], check=True)
        print(f"    [IMPORTANT] Keep '{KEYSTORE_FILE}' in this folder! Reusing it lets you")
        print("    update future Instagram versions directly without uninstalling or logging out.")
    else:
        print(f"[*] Using existing personal keystore: {KEYSTORE_FILE}")

def patch_dex_bytes(data: bytearray, name: str) -> bytes:
    modified = False
    replacements = [
        (b"video/av01", b"video/av00"),
        (b"c2.exynos.", b"c2.android")
    ]
    for old, new in replacements:
        if old in data:
            count = data.count(old)
            data = bytearray(bytes(data).replace(old, new))
            print(f"    [{name}] Patched {count}x: {old.decode()} -> {new.decode()}")
            modified = True

    if modified:
        # Recompute Android DEX SHA-1 signature (bytes 12..32)
        data[12:32] = hashlib.sha1(data[32:]).digest()
        # Recompute Android DEX Adler32 checksum (bytes 8..12)
        checksum = zlib.adler32(data[12:]) & 0xFFFFFFFF
        data[8:12] = struct.pack("<I", checksum)
    return bytes(data)

def main():
    print("=== Galaxy S25 FE Instagram Reels Glitch Patcher (Offline PC Edition) ===\n")

    # Find stock .apkm or .apk in current directory
    candidates = [
        f for f in glob.glob("*.apkm") + glob.glob("*.apk")
        if not f.startswith(("merged_", "patched_", "instagram-s25fe-fixed"))
    ]
    if not candidates:
        print("[!] No Instagram .apkm or .apk file found in this folder!")
        print("    1. Download the stock Instagram .apkm (arm64-v8a) from APKMirror.")
        print("    2. Place it in this exact folder alongside patch_instagram.py.")
        print("    3. Run 'python patch_instagram.py' again.")
        sys.exit(1)

    # Pick the newest file if multiple exist
    input_file = max(candidates, key=os.path.getmtime)
    print(f"[*] Found input package: {input_file}")

    ensure_tool(APKEDITOR_URL, APKEDITOR_JAR)
    ensure_tool(UBERSIGNER_URL, UBERSIGNER_JAR)
    ensure_keystore()

    # Step 1: Merge .apkm bundle into standalone .apk
    working_apk = "merged_temp.apk"
    if input_file.lower().endswith(".apkm"):
        if os.path.exists(working_apk):
            os.remove(working_apk)
        print("\n[*] Step 1/3: Merging .apkm bundle into a standalone APK...")
        subprocess.run(["java", "-jar", APKEDITOR_JAR, "m", "-i", input_file, "-o", working_apk], check=True)
    else:
        working_apk = input_file

    # Step 2: Binary patch classes*.dex in memory
    unaligned_apk = "patched_unaligned.apk"
    print("\n[*] Step 2/3: Patching Exynos AV1/HEVC decoder strings in DEX files...")
    with zipfile.ZipFile(working_apk, "r") as zin, zipfile.ZipFile(unaligned_apk, "w") as zout:
        for item in zin.infolist():
            raw = zin.read(item.filename)
            if item.filename.startswith("classes") and item.filename.endswith(".dex"):
                raw = patch_dex_bytes(bytearray(raw), item.filename)
            zout.writestr(item, raw, compress_type=item.compress_type)

    # Step 3: Zipalign & Sign with personal keystore
    print("\n[*] Step 3/3: Zipaligning and signing APK...")
    subprocess.run([
        "java", "-jar", UBERSIGNER_JAR,
        "-a", unaligned_apk,
        "--ks", KEYSTORE_FILE,
        "--ksAlias", "igkey",
        "--ksPass", "instagram123",
        "--ksKeyPass", "instagram123",
        "--allowResign",
        "--out", "."
    ], check=True)

    final_name = "instagram-s25fe-fixed.apk"
    signed_output = "patched_unaligned-aligned-signed.apk"
    if os.path.exists(signed_output):
        if os.path.exists(final_name):
            os.remove(final_name)
        os.rename(signed_output, final_name)

    # Clean up temporary build files
    for temp in ["merged_temp.apk", unaligned_apk, "patched_unaligned-aligned-signed.apk.idsig"]:
        if os.path.exists(temp):
            os.remove(temp)

    print(f"\n[SUCCESS] Created '{final_name}'!")
    print(" -> First time installing? Uninstall Play Store Instagram, then install this APK.")
    print(" -> Updating an existing install? Do NOT uninstall! Just install on top (or run: adb install -r instagram-s25fe-fixed.apk)")

if __name__ == "__main__":
    main()
