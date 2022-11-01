Part 1
In the JWT, there are three parts:
    - A header: provides information on the type of token and the signing algorithm being used
    - The payload: contains the claims, which are statements about the entity
    - The signature: consists of the encoded header, the encoded payload and a secret

Part 2
This JWT has been tampered with because the signature verification failed. The code for the signature has been changed from its intended 'comp1531' secret. 