"""Cryptographic primitives: RSA 2048, AES-GCM ephemeral session keys, packet format

Uses `cryptography` package.
"""
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.fernet import Fernet
import os
import json
from typing import Tuple

from utils import b64enc, b64dec, sha256_hex, gen_packet_id
from config import MASTER_KEY_FILE


def ensure_master_key() -> bytes:
    """Load or create a Fernet master key stored in MASTER_KEY_FILE"""
    if not MASTER_KEY_FILE.exists():
        key = Fernet.generate_key()
        MASTER_KEY_FILE.write_bytes(key)
        return key
    return MASTER_KEY_FILE.read_bytes()


def generate_rsa_keypair() -> Tuple[bytes, bytes]:
    """Generate RSA 2048 keypair and return (public_pem, private_pem)"""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return public_pem, private_pem


def encrypt_private_pem(private_pem: bytes) -> bytes:
    key = ensure_master_key()
    f = Fernet(key)
    return f.encrypt(private_pem)


def decrypt_private_pem(encrypted_pem: bytes) -> bytes:
    key = ensure_master_key()
    f = Fernet(key)
    return f.decrypt(encrypted_pem)


def encrypt_packet(receiver_public_pem: bytes, plaintext: str, sender_pub_pem: bytes = None) -> str:
    """Create encrypted packet JSON string:
    fields: packet_id, enc_key (rsa-encrypted b64), nonce b64, ciphertext b64, sha256, sender_pub(optional), ts
    """
    # AES ephemeral key
    aes_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext.encode(), None)  # includes tag

    # RSA-encrypt AES key for receiver
    pub = serialization.load_pem_public_key(receiver_public_pem)
    enc_key = pub.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    packet = {
        "packet_id": gen_packet_id(),
        "enc_key": b64enc(enc_key),
        "nonce": b64enc(nonce),
        "ciphertext": b64enc(ct),
        "sha256": sha256_hex(ct),
        "sender_pub": b64enc(sender_pub_pem) if sender_pub_pem else None,
    }

    # Also include an encrypted AES key for the sender so the sender can decrypt their own sent message
    if sender_pub_pem:
        sender_pub = serialization.load_pem_public_key(sender_pub_pem)
        enc_key_sender = sender_pub.encrypt(
            aes_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        )
        packet["enc_key_sender"] = b64enc(enc_key_sender)

    return json.dumps(packet)


def decrypt_packet(encrypted_packet_json: str, receiver_private_pem: bytes) -> str:
    """Decrypt the packet JSON (string) using receiver's private pem (bytes) and return plaintext. Raises on tamper."""
    packet = json.loads(encrypted_packet_json)
    enc_key = b64dec(packet["enc_key"])
    nonce = b64dec(packet["nonce"])
    ct = b64dec(packet["ciphertext"])

    # RSA-decrypt AES key. Try the primary enc_key first; if that fails and the packet
    # contains an `enc_key_sender` (a copy encrypted to the sender's public key) try that as a fallback.
    priv = serialization.load_pem_private_key(receiver_private_pem, password=None)
    aes_key = None
    last_exc = None

    for keyfield in ("enc_key", "enc_key_sender"):
        enc_b64 = packet.get(keyfield)
        if not enc_b64:
            continue
        try:
            candidate = b64dec(enc_b64)
            aes_key = priv.decrypt(
                candidate,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
            )
            break
        except Exception as e:
            last_exc = e
            # try next keyfield

    if aes_key is None:
        raise ValueError("Failed to decrypt AES key with the provided private key") from last_exc

    # verify sha
    if sha256_hex(ct) != packet.get("sha256"):
        raise ValueError("Message tampering detected: SHA mismatch")

    aesgcm = AESGCM(aes_key)
    pt = aesgcm.decrypt(nonce, ct, None)
    return pt.decode()
