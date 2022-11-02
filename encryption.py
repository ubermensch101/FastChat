import rsa


def genprivpubkey():
	(pubkey, privkey) = rsa.newkeys(1024)
	return (pubkey, privkey)


mes = b'my top secret'
def encrypt(message, pubkey):
	crypto = rsa.encrypt(message,pubkey)
	return crypto

#print(len(crypto))

def decrypt(message, privkey):
	decrypt = rsa.decrypt(message,privkey)
	return decrypt

pubkey, privatekey = genprivpubkey()

a=encrypt(mes, pubkey)
print(str(decrypt(a, privatekey))[2:-1])

