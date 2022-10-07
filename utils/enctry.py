# 加蜜,参考https://blog.csdn.net/qq_28905087/article/details/107467795
def enctry(s):
    k = 'q%UyQ1.gJTm>|?86*|T]JMfA6?EWmL-~%=]pq!~}'
    encry_str = ""
    for i, j in zip(s, k):
        temp = str(ord(i) + ord(j)) + '%6?u!'
        encry_str = encry_str + temp
    return encry_str


def dectry(p):
    k = 'q%UyQ1.gJTm>|?86*|T]JMfA6?EWmL-~%=]pq!~}'
    dec_str = ""
    for i, j in zip(p.split("%6?u!")[:-1], k):
        temp = chr(int(i) - ord(j))
        dec_str = dec_str + temp
    return dec_str
