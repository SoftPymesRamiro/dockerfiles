# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# Utils module
# All credits by SoftPymes Plus
# 
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from Crypto.Cipher import AES
import base64
import pyDes
import binascii
import io


class CryptoTools(object):
    """
        Clase con 2 diferentes metodos de encriptacion, el primero se usa en el licenciamiento y el ultimo se usa en
        pymes+.
        Ejemplo (licenciamiento):
        c = CryptoTools()
        print c.encrypt("12345")
        print str(c.decrypt("B1JuYIM2sI6XFNk+YWMd4w==")).rstrip()

        Ejemplo (pymes+):
        key = "ADMINISTRADOR".ljust(8, "F")
        print encrypt_pymes_plus("12345", key)
    """
    def __init__(self, key="LWaElRRz3V418Izu71TwkYeB2mBN8UFd", iv="EwTjpnpTwx4lcr7/DK20Nw=="):
        self.key = key
        self.iv = base64.b64decode(iv)

    def encrypt(self, s):
        """Encript string data

            :param s: input word
            return word: encripted base64
        """
        m = AES.new(self.key, AES.MODE_CBC, self.iv)
        m.block_size = 128
        encoder = PKCS7Encoder()
        pad_text = encoder.encode(s)
        c = m.encrypt(pad_text)
        base64_ciphertext = base64.encodestring(c)
        return base64_ciphertext

    def decrypt(self, s):
        """Decript string data

            :param s: input word
            return word: decripted base64
        """
        pad_text2 = base64.decodestring(s)
        m = AES.new(self.key, AES.MODE_CBC, self.iv)
        decry = m.decrypt(pad_text2)
        return decry


    @staticmethod
    def encrypt_pymes_plus(s, k):
        """Metodo de encriptacion que usa la version pymes+. 
            Este metodo se usara para migrar los usuarios
            
            :param s
            :param k
            return word: base64
        """
        k = k[:8]
        k = pyDes.des(k, pyDes.CBC, "\x0A\x14\x1E\x28\x32\x3C\x46\x50", pad=None, padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(s)
        return base64.b64encode(d).rstrip()


class PKCS7Encoder(object):
    '''
    RFC 2315: PKCS#7 page 21
    Some content-encryption algorithms assume the
    input length is a multiple of k octets, where k > 1, and
    let the application define a method for handling inputs
    whose lengths are not a multiple of k octets. For such
    algorithms, the method shall be to pad the input at the
    trailing end with k - (l mod k) octets all having value k -
    (l mod k), where l is the length of the input. In other
    words, the input is padded at the trailing end with one of
    the following strings:

             01 -- if l mod k = k-1
            02 02 -- if l mod k = k-2
                        .
                        .
                        .
          k k ... k k -- if l mod k = 0

    The padding can be removed unambiguously since all input is
    padded and no padding string is a suffix of another. This
    padding method is well-defined if and only if k < 256;
    methods for larger k are an open issue for further study.
    '''
    def __init__(self, k=16):
        self.k = k

    ## @param text The padded text for which the padding is to be removed.
    # @exception ValueError Raised when the input padding is missing or corrupt.
    def decode(self, text):
        '''
        Remove the PKCS#7 padding from a text string
        '''
        nl = len(text)
        val = int(binascii.hexlify(text[-1]), 16)
        if val > self.k:
            raise ValueError('Input is not padded or padding is corrupt')

        l = nl - val
        return text[:l]

    ## @param text The text to encode.
    def encode(self, text):
        '''
        Pad an input string according to PKCS#7
        '''
        l = len(text)
        output = io.StringIO()
        val = self.k - (l % self.k)
        for _ in range(val):
            output.write('%02x' % val)
        return text + binascii.unhexlify(output.getvalue())


