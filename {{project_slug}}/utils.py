import json, hashlib

def jcs_dumps(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def canonicalize(env):
    e = json.loads(json.dumps(env))
    integ = e.get("integrity", {})
    if "chain_hash" in integ:
        del integ["chain_hash"]
    cp = integ.get("checkpoint")
    if isinstance(cp, dict) and "root" in cp:
        del cp["root"]
    return jcs_dumps(e).encode("utf-8")

def sha256_hex(b: bytes):
    return hashlib.sha256(b).hexdigest()

def merkle_root_hex(leaves_hex):
    if not leaves_hex:
        return sha256_hex(b"")
    level = [bytes.fromhex(h) for h in leaves_hex]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            a = level[i]
            b = level[i+1] if i+1 < len(level) else level[i]
            nxt.append(hashlib.sha256(a + b).digest())
        level = nxt
    return level[0].hex()
