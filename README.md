# Web-Multimedia-Final-Project
## Introduction
We create a tamper-proof mechanism for human-AI dialogue using serialized encryption and signature, which we drew inspiration from blockchain technology.

This system can prevent others from tampering past conversation records: If one prompt is altered, then it would be inconsistent with the signatures of the following prompts. And we can locate the source of tampering easily. Secrecy is also ensured through hashing so that third-party wouldn’t know the content of the conversation.

## Structure
The conversation involves three entities: AI, human and the third-party (could be either human or machine). AI and human have conversation, while the third-party have no idea of what they’re talking about. The third-party’s only job is to encrypt and sign. (Our entire system works via MEGA)

## Mechanism
Both side’s block (prompt + signature) are hashed. Then encrypted by public key of third-party (kept secret to itself) and appended onto the other’s prompts as signature.

## Code Files
### Main files
`user.py`: User run this file on terminal
`genai.py`: Someone run this file to act as Generative AI (implementation of ChatGPT API)
`third_party.py`: Third-party run this file (Encrypt and sign the hashed data)

### Auxiliary files
`crypto.py` includes encryption, decryption and key-generating function
`load.py` includes mega-login, upload and download function

### Others
`private_key.pem` & `public_key.pem`: Public and private keys shared by user and AI, so that they can conduct encrypted conversation

## NOTES
1. Since the files would be repeatedly uploaded/downloaded from mega, the time take for a single conversation can be very long ( > 1min )
2. third-party.py will show what stage has been processed
3. third-party.py will store the hashed data from both sides in H_A (from user) and H_B (from AI) folders. User and AI will store its “block” in A_log and B_log folders respectively.
4. **User and AI have to share the same public-private key pairs, otherwise it won’t work**
5. **type “stop” in the user UI will kill three execution (user, genai and the third-party) all at once.**



