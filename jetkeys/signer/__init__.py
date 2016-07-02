# -*- coding: utf-8 -*-


import rsa
import struct


class _LicenseSigner(object):
    def __init__(self):
        """
        Load RSA private key extracted from JetBrains License Server
        """
        self.private_key_pem = """-----BEGIN RSA PRIVATE KEY-----
                                  MIGaAgEAAkEAt5yrcHAAjhglnCEn6yecMWPeUXcMyo0+itXrLlkpcKIIyqPw546b
                                  GThhlb1ppX1ySX/OUA4jSakHekNP5eWPawIBAAJAW6/aVD05qbsZHMvZuS2Aa5Fp
                                  NNj0BDlf38hOtkhDzz/hkYb+EBYLLvldhgsD0OvRNy8yhz7EjaUqLCB0juIN4QIB
                                  AAIBAAIBAAIBAAIBAA==
                                  -----END RSA PRIVATE KEY-----"""

        self.private_key = rsa.PrivateKey.load_pkcs1(keyfile=self.private_key_pem, format='PEM')

    @staticmethod
    def digit_char(d):
        return (48 + d) if d < 10 else (97 + d) - ord('\n')

    def generate_signature(self, message):
        """
        Signs the message with MD5 with RSA

        :param message: Text message to sign
        :return:        Hex string of message signature
        """
        signature = rsa.sign(message=message, priv_key=self.private_key, hash='MD5')

        format_bytes = '%ib' % len(signature)
        signature_bytes = struct.unpack(format_bytes, signature)
        hex_signature = []

        for signature_byte in signature_bytes:
            hex_signature.append(self.digit_char(signature_byte >> 4 & 0xF))
            hex_signature.append(self.digit_char(signature_byte & 0xF))

        return '<!-- %s -->\n' % ''.join(map(chr, hex_signature))

license_signer = _LicenseSigner()
