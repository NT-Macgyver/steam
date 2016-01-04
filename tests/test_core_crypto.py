import unittest
import mock

from steam.core import crypto


class crypto_testcase(unittest.TestCase):
    def setUp(self):
        class NotRandom:
            def read(self, n):
                return '1' * n

        def fakeNew():
            return NotRandom()

        self._oldnew = crypto.Random.new
        crypto.Random.new = fakeNew

    def tearDown(self):
        crypto.Random.new = self._oldnew

    def test_keygen(self):
        expected_key = '1' * 32
        expected_ekey = ('82a5d4d6de38e443ed3e6f0a1701a2c47bc98e0860e7883638ea5263a1744d02'
                         'f733f09bc6b0f9b2a371bbb79b639208521f88658aab38c23e181d39a58ae39e'
                         'c4e207fba822d523028d3c04e812abdc2247aa8d8e6e4a89c7a65671c5bcb329'
                         '51c6d721ccf57cc2920d6ff3b69bfb2c611b1275badcd3e37fe024c9a25bf4b0'
                         )

        key, ekey = crypto.generate_session_key()
        ekey = ekey.encode('hex')

        self.assertEqual(key, expected_key)
        self.assertEqual(ekey, expected_ekey)

    def test_keygen_with_challenge(self):
        expected_key = '1' * 32
        expected_ekey = ('d710c55122f9bf772ec9c0f21d75c05055764d5445902577340029b4707e1725'
                         'd61bec77f41b17faed6577d08c812cef76dca8b0b0b2329e1f33ea4cfa31f1e6'
                         '0babc859c55b6ac94497b5dc9b0bc89629290dc038274af4377771e088e92887'
                         '30d3906f6b698fd113ba36e3d28a5e1ce0283b27a1adda538df5dc5b179cf84f'
                         )

        key, ekey = crypto.generate_session_key('5'*16)
        ekey = ekey.encode('hex')

        self.assertEqual(key, expected_key)
        self.assertEqual(ekey, expected_ekey)


    def test_encryption(self):
        message = "My secret message"
        key = '9' * 32
        hmac = '3' * 16

        # legacy
        cyphertext = crypto.symmetric_encrypt(message, key)
        dmessage = crypto.symmetric_decrypt(cyphertext, key)

        self.assertEqual(message, dmessage)

        # with HMAC
        cyphertext = crypto.symmetric_encrypt_HMAC(message, key, hmac)
        dmessage = crypto.symmetric_decrypt_HMAC(cyphertext, key, hmac)

        self.assertEqual(message, dmessage)

        # failing HMAC check
        with self.assertRaises(RuntimeError):
            crypto.symmetric_decrypt_HMAC(cyphertext, key, '4'*16)


