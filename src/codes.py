
from src.config import N_BITS, CHARSET, BITS_X_CHAR


class Code:

    def __init__(self, epoch_end):

        self.epoch_end = epoch_end

    def encode(self, msg):
        if len(msg) != N_BITS//BITS_X_CHAR:
            print(f'ERROR: {N_BITS//BITS_X_CHAR} characters are expected')
            return

        # Convertimos el mensaje en un vector de bits
        enc = [CHARSET.index(ch) for ch in msg.lower()]
        bits = ''.join([bin(n)[2:].zfill(BITS_X_CHAR) for n in enc])
        print(bits)
        offset = int(bits, 2)
        print(f'offset: {offset}')

        return self.epoch_end-offset

    def decode(self, epoch):
        offset = self.epoch_end-epoch
        print(f'offset: {offset}')

        bit_str = bin(offset)[2:].zfill(N_BITS)
        msg = ''
        for i in range(0, N_BITS, BITS_X_CHAR):
            msg += CHARSET[int(bit_str[i:i+BITS_X_CHAR], 2)]
        return msg.upper()
