import subprocess, json, os, time

print("=== Installing Solana CLI ===")
subprocess.run("sh -c '$(curl -sSfL https://release.anza.xyz/v1.18.18/install)'", shell=True, timeout=60)
os.environ['PATH'] += ':/home/runner/.local/share/solana/install/active_release/bin'

# Generate keypair or use provided one
print("\n=== Generating Solana Keypair ===")
result = subprocess.run("solana-keygen new --no-bip39-passphrase --force -o keypair.json", 
                       shell=True, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)

# Get public key
result = subprocess.run("solana-keygen pubkey keypair.json", shell=True, capture_output=True, text=True)
pubkey = result.stdout.strip()
print(f"Public Key: {pubkey}")

# Try multiple devnet faucets
print("\n=== Trying Devnet Faucets ===")
faucets = [
    f"solana airdrop 1 {pubkey} --url devnet",
    f"curl -s -X POST https://faucet.solana.com -d '{{\"jsonrpc\":\"2.0\",\"method\":\"requestAirdrop\",\"params\":[\"{pubkey}\",1000000000],\"id\":1}}' -H 'Content-Type: application/json'",
    f"curl -s 'https://solfaucet.com/api/drip?address={pubkey}&amount=1&network=devnet'",
]

for cmd in faucets:
    print(f"\n> {cmd[:80]}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
    print(result.stdout[:300])
    if result.stderr:
        print(f"ERR: {result.stderr[:200]}")

# Check balance
time.sleep(5)
result = subprocess.run(f"solana balance {pubkey} --url devnet", shell=True, capture_output=True, text=True)
print(f"\n=== Balance ===")
print(result.stdout)

# Save keypair for later use
with open("keypair.json") as f:
    kp = f.read()
print(f"\n=== KEYPAIR (save this) ===")
print(kp[:200])

# List available programs for airdrop farming
print("\n=== Current Solana Protocols (potential airdrops) ===")
protocols = ["Jupiter", "Jito", "Marginfi", "Kamino", "Drift", "Zeta", "Parcl", "Tensor"]
for p in protocols:
    print(f"  - {p}")

# Save results
with open("result.txt", "w") as f:
    f.write(f"PUBKEY: {pubkey}\n")
    f.write(f"KEYPAIR_JSON: {kp}\n")
    f.write(f"BALANCE: {result.stdout.strip()}\n")
    f.write("Next: Use this keypair to interact with Solana protocols for airdrop eligibility\n")
