# Ücretsiz Türkçe ses (Microsoft Edge sesli okuma) + kelime zamanları.
# Kullanım: python3 edge.py <ses> <hız> <ton> <ses_seviyesi> <çıktı.mp3>   (metin stdin'den, çıktı: stdout'ta JSON kelime listesi)
import asyncio, json, os, ssl, sys
try:
    import edge_tts
    import edge_tts.communicate as ec
except ImportError:
    sys.stderr.write("edge-tts kurulu değil. Şunu çalıştır: pip3 install edge-tts\n"); sys.exit(2)
ca = os.environ.get("EDGE_CA_BUNDLE") or ("/root/.ccr/ca-bundle.crt" if os.path.exists("/root/.ccr/ca-bundle.crt") else None)
if ca: ec._SSL_CTX = ssl.create_default_context(cafile=ca)  # sertifika doğrulaması açık kalır

async def main(voice, rate, pitch, volume, out):
    text = sys.stdin.read().strip(); words = []
    c = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume, boundary="WordBoundary")
    with open(out, "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"w": ch["text"], "start": ch["offset"] / 1e7, "end": (ch["offset"] + ch["duration"]) / 1e7})
    print(json.dumps(words, ensure_ascii=False))

voice, rate, pitch, volume, out = sys.argv[1:6]
asyncio.run(main(voice, rate, pitch, volume, out))
