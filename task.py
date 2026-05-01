import json, base64, os, requests

KP = [8, 201, 185, 57, 113, 84, 216, 128, 250, 235, 169, 101, 225, 211, 54, 48, 37, 220, 196, 86, 131, 117, 95, 74, 56, 50, 213, 69, 169, 34, 159, 98, 221, 201, 9, 6, 29, 57, 233, 161, 24, 32, 230, 188, 30, 178, 231, 237, 130, 251, 141, 81, 155, 163, 209, 5, 109, 190, 51, 98, 163, 170, 242, 90]

print("=== Using existing keypair ===")
print(f"Public Key: Fvku5CNSZAsV1yJiHK9Ji78oSGKYHpNT3pBbMztdaw21")

# Try multiple faucets  
print("\n=== Trying Devnet Faucets ===")
faucets = [
    ("Solana official", f"https://api.devnet.solana.com", 
     {"jsonrpc":"2.0","method":"requestAirdrop","params":["Fvku5CNSZAsV1yJiHK9Ji78oSGKYHpNT3pBbMztdaw21",1000000000],"id":1}),
    ("QuickNode", "https://api.devnet.solana.com",
     {"jsonrpc":"2.0","method":"requestAirdrop","params":["Fvku5CNSZAsV1yJiHK9Ji78oSGKYHpNT3pBbMztdaw21",1000000000],"id":1}),
]

for name, url, payload in faucets:
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"{name}: {r.status_code} - {r.text[:200]}")
    except Exception as e:
        print(f"{name}: {e}")

# Also try HTTP faucets
print("\n=== HTTP Faucets ===")
http_faucets = [
    f"https://faucet.solana.com/api/request?address={pubkey}&amount=1000000000",
    f"https://solfaucet.com/api/drip?address={pubkey}&amount=1&network=devnet",
]

for url in http_faucets:
    try:
        r = requests.get(url, timeout=10)
        print(f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"HTTP: {e}")

# Save result
with open("result.txt", "w") as f:
    f.write(f"PUBKEY: Fvku5CNSZAsV1yJiHK9Ji78oSGKYHpNT3pBbMztdaw21\n")
    f.write(f"ATTEMPTED_FAUCETS: done\n")
    f.write("NEXT: If got SOL, run protocol interactions\n")
