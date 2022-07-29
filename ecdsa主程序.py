def Ecdsa_Sign(m, n, G, d,k):
    e = hash(m)
    R = Multiply(k, G)
    r = R[0] % n
    s = (Gcd(k, n) * (e + d * r)) % n
    return r, s

def Ecdsa_Verify(m, n, G, r, s, P):
    e = hash(m)
    w = Gcd(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = Add(Multiply(v1, G), Multiply(v2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % n == r):
            print('true')
            return True
        else:
            print('false')
            return False

def k_Leaking(r,n,k,s,m):
    r_reverse=Gcd(r,n)
    e=hash(m)
    d=r_reverse * (k*s-e)%n
    return d

def k_Reuse(r1,s1,m1,r2,s2,m2,n):
    e1=hash(m1)
    e2=hash(m2)
    d=((s1 * e2 - s2 * e1) * Gcd((s2 * r1 - s1 * r1), n)) % n
    return d

def Use_the_Same_k(s1,m1,s2,m2,r,d1,d2,n):
    e1=hash(m1)
    e2=hash(m2)
    d2_1 = ((s2 * e1 - s1 * e2 + s2 * r * d1) * Gcd(s1 * r, n)) % n
    d1_1 = ((s1 * e2 - s2 * e1 + s1 * r * d2) * Gcd(s2 * r, n)) % n
    if(d2==d2_1 and d1_1==d1):
        print("互相计算密钥成功")
        return 1
    else:
        print("互相计算密钥错误")
        return 0

def Verify_without_m(e, n, G, r, s, P):
    w = Gcd(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = Add(Multiply(v1, G), Multiply(v2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % n == r):
            print('true')
            return True
        else:
            print('false')
            return False
            
def Pretend(r, s, n, G, P):
    u = random.randrange(1, n - 1)
    v = random.randrange(1, n - 1)
    r1 = Add(Multiply(u, G), Multiply(v, P))[0]
    e1 = (r1 * u * Gcd(v, n)) % n
    s1 = (r1 * Gcd(v, n)) % n
    Verify_without_m(e1, n, G, r1, s1, P)

def Schnorr_Sign(m, n, G, d,k):
    R = Multiply(k, G)
    e = hash(str(R[0]) + m)
    s = (k + e * d) % n
    return R, s

def Schnorr_and_ECDSA(r1, s1, R, s2, m, n):
    e1 = int(hash(m))
    e2 = int(hash(str(R[0]) + m))
    d = ((s1 * s2 - e1) * Gcd((s1 * e2 + r1), n)) % n
    return d

def Relatively_Prime(a, b):
    while a != 0:
        a, b = b % a, a
    return b

# InECC
def Add(m, n):
    if (m == 0):
        return n
    if (n == 0):
        return m
    he = []
    if (m != n):
        if (Relatively_Prime(m[0] - n[0], p) != 1 and Relatively_Prime(m[0] - n[0], p) != -1):
            return 0
        else:
            k = ((m[1] - n[1]) * Gcd(m[0] - n[0], p)) % p
    else:
        k = ((3 * (m[0] ** 2) + a) * Gcd(2 * m[1], p)) % p
    x = (k ** 2 - m[0] - n[0]) % p
    y = (k * (m[0] - x) - m[1]) % p
    he.append(x)
    he.append(y)
    return he

def Multiply(n, l):
    if n == 0:
        return 0
    if n == 1:
        return l
    t = l
    while (n >= 2):
        t = Add(t, l)
        n = n - 1
    return 

# 测试签名和验证
r,s=Ecdsa_Sign(m,n,G,d,k)
print("签名为:",r,s)
print("验证结果为：")
Ecdsa_Verify(m,n,G,r,s,P)

# 泄露k导致密钥泄露
if (d == k_Leaking(r,n,k,s,m)):
    print("验证成功")

#3 重用k导致密钥泄露
r_1,s_1=Ecdsa_Sign(m_1,n,G,d,k)
r_2,s_2=Ecdsa_Sign(m,n,G,7,k)
if (d == k_Reuse(r,s,m,r_1,s_1,m_1,n)):
    print("验证成功")

# 使用相同k，可互相计算密钥
print("4. 使用相同k，互相计算密钥---------------------------------------------")
print("验证结果为：")
Use_the_Same_k(s_1,m_1,s_2,m,r,5,7,n)

#  r,-s同样为有效签名
print("5. 测试 r,-s是否为有效签名---------------------------------------------")
print("测试结果为：")
Ecdsa_Verify(m,n,G,r,-s,P)

# 伪装中本聪
print("6. 伪装中本聪---------------------------------------------")
print("伪装是否成功：")
Pretend(r,s,n,G,P)

# Schnorr_Sign签名、ecdsa签名使用相同的d，k，导致密钥泄露

r3,s3=Schnorr_Sign(m,n,G,d,k)#第六问
d2=Schnorr_and_ECDSA(r,s,r3,s3,m,n)
print("破解是否成功：")
print(d == d2)
