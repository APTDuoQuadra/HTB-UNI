from Crypto.Cipher import AES
from random import randint, randbytes,seed
from hashlib import md5

ciphertext = "1aaad05f3f187bcbb3fb5c9e233ea339082062fc10a59604d96bcc38d0af92cd842ad7301b5b72bd5378265dae0bc1c1e9f09a90c97b35cfadbcfe259021ce495e9b91d29f563ae7d49b66296f15e7999c9e547fac6f1a2ee682579143da511475ea791d24b5df6affb33147d57718eaa5b1b578230d97f395c458fc2c9c36525db1ba7b1097ad8f5df079994b383b32695ed9a372ea9a0eb1c6c18b3d3d43bd2db598667ef4f80845424d6c75abc88b59ef7c119d505cd696ed01c65f374a0df3f331d7347052faab63f76f587400b6a6f8b718df1db9cebe46a4ec6529bc226627d39baca7716a4c11be6f884c371b08d87c9e432af58c030382b737b9bb63045268a18455b9f1c4011a984a818a5427231320ee7eca39bdfe175333341b7c"

x = 21202245407317581090
y = 11086299714260406068
prime = 92434467187580489687

k = 10

known_coeffs = [93526756371754197321930622219489764824]

def compute_coeff(previous):
    return int(md5(previous.to_bytes(32, byteorder="big")).hexdigest(), 16)

for _ in range(k - 2):
    known_coeffs.append(compute_coeff(known_coeffs[-1]))

assert len(known_coeffs) == k - 1

sum = 0
for i in range(len(known_coeffs)):
    sum += known_coeffs[i] * (x ** (i + 1))

# y = sum + first_coeff mod prime
first_coeff = prime - (sum % prime) + y

assert compute_coeff(first_coeff) == known_coeffs[0]

# Get the flag!

seed(first_coeff)
key = randbytes(16)
aes = AES.new(key, AES.MODE_ECB)
flag = bytes.fromhex(ciphertext)
flag = aes.decrypt(flag)[:-8]

print(flag.decode())
