
#Generation of Hash Value for the given string
#Assumption - The plaintext string is divisible by 8
def hash_value(plain):
  l = len(plain)
  rows=int(len(plain)/8)
 
  matrix=[] #To arrange the plaintext in N*8 format
  for i in range(rows):
    row=[]
    for j in range(8):
      row.append('x')
    matrix.append(row)
  
  for i in range(l): #Adding the plaintext characters in the matrix
    row = int(i/8)
    col = int(i%8)
    matrix[row][col]=plain[i] 
  hash=['a','a','a','a','a','a','a','a'] #To store the Hash Value - 8 Characters
  prev_col_val=0
  
  for i in reversed(range(8)): #Calculating the Hash Value
    col_val=0
    for j in range(rows):
      col_val=ord(matrix[j][i])-97+col_val

    col_val=col_val+prev_col_val
    col_val=col_val%26
    
    prev_col_val=col_val
    hash[i]=chr(97+col_val)
  
  str1= ""
  hash=str1.join(hash) #Returning the calculated Hash value for the input string
  return hash

"""### **Encryption and Decryption**"""

#Generating key of length equal to the plain/cipher text by repeating the sequence
def key_formation(key,size):
  key_value = []
  for i in range(0,size):
    key_value.append(key[i%4])
  return key_value

#Encryption of the Plaintext to the cipher text
#Input = (Plaintext(Concatenated Plaintext by user and its Hashed value), key)
#Output = Encrypted text 
def Encryption(plain_text, hashed_text, key):
  plaintext = list(plain_text) + list(hashed_text) #Concatenation
  key = list(key)
  
  #Formation of Key
  if len(key) != len(plain_text):
    key = key_formation(key,len(plaintext))
  
  #Encryption
  encrypted_text = []
  for i in range(0, len(plaintext)):
    encrypted_val = ((ord(key[i])-97)+ (ord(plaintext[i])-97))%26
    encrypted_text.append(chr(encrypted_val+ord('a')))

  ciphertext = ""
  return ciphertext.join(encrypted_text)

#Decryption of the CipherText to the plain text
#Input = (CipherText, key)
#Output = Decrypted Plain text 
def Decryption(encrypted_text, key):
  key = list(key)
  enrypted_text = list(encrypted_text)

  #Formation of Key
  if len(key) != len(encrypted_text):
    key = key_formation(key,len(encrypted_text))

  #Decryption
  decrypted_text = []
  for i in range(0, len(encrypted_text)):
    decrypted_val = (((ord(encrypted_text[i])-97) - (ord(key[i])-97)) + 26) %26
    decrypted_text.append(chr(decrypted_val + ord('a')))
  
  plaintext = ""
  return plaintext.join(decrypted_text)

"""### **Brute Force**"""

#Function checks whether the input key is valid or not with the help of the 5 cipher texts
def check_key(key):
  for i in range(0,5): #Iterating over 5 cipher texts
    #Decrypting each cipher text with the key
    decrypted_text = Decryption(ciphertext_list[i],key) 
    last_len = len(decrypted_text) - 8
    #Finding the hash value of the plain text 
    #obtained from the decryption above
    decrypted_hash = hash_value(decrypted_text[0:last_len]) 
    original_hash = decrypted_text[last_len:len(decrypted_text)]
    #Matching of the hashvalue of the decrypted text 
    #with the original hash(from decryption above)
    if (decrypted_hash != original_hash): 
      return False
  return True

#This function generates all the possible permuted 4 characters keys 
 #and check the original key using recursion
def generate_keys(characters, key, key_size):
  if (key_size == 0):
    #Key of size 4 is obtained which is checked if it is correct key or not
    value = check_key(key) 
    if value == True: 
      return key
    return " "

  for i in range(0,26): #Generating Keys
    new_key = key + characters[i]
    temp_key = generate_keys(characters, new_key, key_size-1) #Recursive Call
    try:
      if len(temp_key) == 4:
        return temp_key
    except:
      pass

#Functions to execute the brute force attack to discover the key
def brute_force(key_size = 4):
  #Generate Set which contains all the characters used for permuting the keys
  characters = []
  for i in range(0,26):
    characters.append(chr(i+97))
  key = generate_keys(characters,"",4) #Discovering key
  print("The Key is: ", key)

"""### **Main Function**"""

#List storing the plaintexts, hashedtexts(generated from plaintexts), ciphertexts
plaintext_list = []
hashedtext_list = []
ciphertext_list = []

#Main Calling Function
if __name__=="__main__":
  key = str(input("Enter the Key (4 characters): ")) #Enter the key
  for i in range(0,5):
    plaintext = str(input("\n\nEnter the Plain Text {}: ".format(i+1))) #Enter 5 Plain Texts
    n = len(plaintext)
    count = 0
    while (len(plaintext)%8 != 0) : #Making the plaintext length divisible by 8
        plaintext += 'x'
        count += 1
    hashed_text = hash_value(plaintext) #Generating the hash value of the plaintext
    cipher_text = Encryption(plaintext, hashed_text, key) #Encrypting the plaintext
    print("\nCipher Text (After Encryption): ", cipher_text)
    original_text = Decryption(cipher_text, key) #Decrypting the ciphertext
    print("\nOriginal Text (After Decryption): ", original_text[0:n])

    plaintext_list.append(plaintext)
    hashedtext_list.append(hashed_text)
    ciphertext_list.append(cipher_text)
  print("\n\nLaunching Brute Force Attack to discover the key")
  brute_force()
