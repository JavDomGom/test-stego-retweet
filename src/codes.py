
import os
import numpy
import numpy as np

from src.config import N_BITS, CHARSET, M_FILE, BITS_X_CHAR

SUPPORTED_CODES = ["Binary-Hamming"]

class Code:
    
    def __init__(self, code_type, epoch_end):

        if code_type not in SUPPORTED_CODES:
            raise NotImplementedError

        self.code_type = code_type
        self.epoch_end = epoch_end


    def encode(self, msg):
        if self.code_type == "Binary-Hamming":
            return self.encode_binary_hamming_code(msg)


    def decode(self, msg):
        if self.code_type == "Binary-Hamming":
            return self.decode_binary_hamming_code(msg)


    def encode_binary_hamming_code(self, msg):

        """
        He elegido 24 bits porque así podemos transmitir 3 bytes por
        cada retweet. Por lo tanto, esperamos que msg sea una variable
        de tipo bytes y que contenga solo 3.
        """
        
        if len(msg) != N_BITS//BITS_X_CHAR:
            print(f"ERROR: {N_BITS//BITS_X_CHAR} characters are expected")
            return

 
        # Convertimos el mensaje en un vector de bits
        enc = [CHARSET.index(ch) for ch in msg.lower()]
        bits = ''.join([bin(n)[2:].zfill(BITS_X_CHAR) for n in enc])
        m = np.array([int(x) for x in bits])


        """
        Lo primero que necesitamos es una matrix M que tenga todos los
        códigos posibles que se pueden usar. En este primer ejemplo
        enviaremos bytes, así que crearemos todas las combinaciones
        posibles de unos y ceros con 24 bits. 
        
        XXX: Quizás sería más interesante usar un charset como en 
        la versión anterior. Lo podemos estudiar más adelante.

        Esta matrix tendrá 24 filas de 2^24-1 columnas. Es muy grande por 
        lo que he creado un programa a parte (generate-M.py) que la crea 
        y la guarda en un archivo, para no tener que hacerlo cada vez. 
        Ocupa 385MB.

        XXX: Cada bit ocupa un byte. Con una representación a nivel de
        bit podríamos reducir la matrix a unos 48MB.
        """

        # Leemos la matriz M
        if not os.path.isfile(M_FILE):
            print("ERROR: M.npy not found, please generate it")
            return

        M = np.load("M.npy")


        """
        El segundo paso consiste en crear un vector donde cada epoch va 
        representar un 1 o un 0. Para ello basta con hacer un mod 2 del
        epoch. Como los epochs son consecutivos, nos vamos a encontrar
        con que el vector va alternando 0 y 1 continuamente: 0101010...
        Esto nos permite crear el vector de una forma muy sencilla y 
        rápida con numpy.

        XXX: En realidad, dado que usamos un offset para calcular el
        epoch (ver return del final), el valor que tenga este vector 
        nos da igual. De hecho, podríamos usar un vector aleatorio 
        generado con la contraseña.
        """
        c = np.zeros(2**N_BITS-1)
        c[::2] = 1
 


        """
        La idea del matrix embedding con códigos de Hamming binarios es 
        que el receptor pueda realizar la operación con matrices m=Ms,
        donde s es el vector de epochs, y obtenga el mensaje m de 24
        bits que le queremos transmitir.
        
        Si realizamos esta operación directamente sobre el vector de 
        epochs c, como es lógico no vamos a obtener el valor del mensaje
        que queremos, si no cualquier otro valor. Pero la teoría de los
        códigos de Hamming nos dice que si cambiamos el bit correcto
        del vector, obtendremos un vector s que al realizar Ms sí nos
        dará el valor del mensaje que queremos  transmitir.
        
        Para hacerlo tenemos que buscar que posición ocupa en la matriz
        M el vector r = m-Mc. Ese es el bit que tenemos que cambiar.
        Por convenio, consideramos que un tuit al que le hemos hecho
        retuit tiene un valor contrario al que indica su epoch mod 2.
        Por lo tanto, para transmitir 3 bytes bastará con hacer un
        retuit de un tuit con el epoch indicado.

        """

        # Buscamos el bit que hay que cambiar
        r = (m-M.dot(c))%2
        idx = np.where(np.all(M.T==r, axis=1))[0]
        if len(idx)==0:
            print("ERROR: message not found in M. Maybe M is wrong!")
            return

        idx = idx[0]

        # Negamos el bit en la posición encontrada
        s = np.array(c)
        s[idx] = 1-s[idx]

        # Verificamos que efectivamente se transmite el mensaje que queremos
        m_recovered = (M.dot(s))%2

        if not (m==m_recovered).all():
            print("ERROR: Unknown coding problem :(")
            return

        return self.epoch_end-idx
        



    def decode_binary_hamming_code(self, epoch):

        # Obtenemos M
        M = np.load("M.npy")

        # Calculamos c de la misma manera que al codificar
        c = np.zeros(2**N_BITS-1)
        c[::2] = 1
 
        # Calculamos la posición del bit que se ha modificado de c
        idx = self.epoch_end-epoch

        # Lo usamos para calcular s, igual que en la codificación
        s = np.array(c)
        s[idx] = 1-s[idx]

        # Finalmente recuperamos el mensaje
        m = (M.dot(s))%2


        bit_str = ''.join([str(b) for b in m.astype('uint8')])
        msg = ""
        for i in range(0, N_BITS, BITS_X_CHAR):
            msg += CHARSET[int(bit_str[i:i+BITS_X_CHAR],2)]

        return msg.upper()




