"""
Given two strings s and t, does s occur as a substring of t?

• Compare h(s) == h(t[i : i + len(s)])
• If hash values match, check strings
• O(|s| + |t| · cost(h))
    - with rolling hash O(|s|+|t|))
"""



def brute_search(text, sub):
    """
    brute search
    """
    text_n = len(text)
    sub_n = len(sub)

    for i in range(0, text_n - sub_n + 1):
        if text[i: i+ sub_n ] == sub:
            return True
    return False


class SlidingHash:
    """
    Rolling hash mod prime
    each char is number base 256 for ASCII
    Based:
        - hash([d3, d2, d1, d0]) = d3 · a^3 + d2 · a^2 + d1 · a^1 +d0 ·a^0) mod p
    """


    def __init__(self, base, prime):
        """
        as each character ord(char) -> base = 256
        so prime will be 251
        """
        self.hash = 0
        self.size = 0

        self.base = base
        self.prime = prime

    def append(self, value):
        """
        slide left by base (a) and add value
         - hash = [ hash * base + value ]
        """
        self.hash = ((self.hash * self.base) % self.prime + value) % self.prime
        self.size += 1

    def skip(self, value):
        self.hash = ( self.hash - value * self.base**(self.size-1) ) % self.prime
        self.size -= 1

def karp_rabin(text, sub):
    """
    - compare hashes
    - if match - compare strings
    """
    base = 256
    prime = 251

    # compute sub str hash
    sub_slide = SlidingHash(base, prime)
    for ch in sub:
        sub_slide.append(ord(ch))
    sub_hash = sub_slide.hash

    #init text slide sub
    slide = SlidingHash(base, prime)
    for i in range(len(sub)):
        slide.append(ord(text[i]))
    if slide.hash == sub_hash:
        if text[: len(sub)] == sub:
            return True

    # check sliding window
    for i in range(len(sub), len(text)):
        slide.skip(ord(text[i-len(sub)]))
        slide.append(ord(text[i]))

        if slide.hash == sub_hash:
            if text[i-len(sub) + 1: i + 1] == sub:
                return True
    return False

if __name__ == '__main__':
    text = "abcdefg"
    assert brute_search(text, 'fg') == True


    assert karp_rabin(text, 'ab') == True
    assert karp_rabin(text, 'de') == True
    assert karp_rabin(text, 'fg') == True

    assert karp_rabin(text, 'xx') == False
    assert karp_rabin(text, '1') == False
    assert karp_rabin(text, 'x') == False
