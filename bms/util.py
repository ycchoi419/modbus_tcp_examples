def bindigits(n, bits):
    # references
    #- https://parading.tistory.com/61?category=799361
    s = bin(n & int("1"*bits, 2))[2:]    # int("1111111111111111", 2)""안의 숫자를 int단위로 2진수 표시, [2:]는 앞의 0b제거
                                         # int("111",2) 결과 값은 7, bin(int"111",2) 결과 값은 0b111.
                                         # n에다가 2진수 16bit의 최대값을 연산곱하라(Two's complement니까)

    print("s : ", s)					# 0을 채우지 않은 변환 값
    return ("{0:0>%s}" % (bits)).format(s)   #s의 결과 값의 앞에 bit 수만큼 0을 채워라.

def bindigits2(n, bits=16):
    # references
    #- https://parading.tistory.com/61?category=799361
    print("before:",bin(n))
    s = bin(n & int("1"*bits, 2))[3:]      # int("1111111111111111", 2)""안의 숫자를 int단위로 2진수 표시, [2:]는 앞의 0b제거
                                           # 추가로 MSB를 제거하기 위해 [3:0]
                                           # int("111",2) 결과 값은 7, bin(int"111",2) 결과 값은 0b111.
                                           # n에다가 2진수 16bit의 최대값을 연산곱하라(Two's complement니까)
    print("after:", s)
    return ("{0:0>%s}" % (bits-1)).format(s) # s의 결과 값의 앞에 bit 수만큼 0을 채워라.

def _to_int(val, nbits):
    i = int(val, 16)
    if i >= 2 ** (nbits - 1):
        i -= 2 ** nbits
    return i

def _to_int2(val, nbits):
    i = int(val, 2)
    if i >= 2 ** (nbits - 1):
        i -= 2 ** nbits
    return i

def to_hex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits)).lstrip('0x')

def cut_msb(n,bit):
    s=bin(n)[2:]
    print("s:",s)
    return ("{0:0>%s}" % (bit)).format(s)
