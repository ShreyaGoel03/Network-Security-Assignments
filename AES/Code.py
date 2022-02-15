# -*- coding: utf-8 -*-
"""NS Assignment-2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j4VQwCnPMBuo3DbaigHJKqqhzwXrVHai

# **Key Expansion**
"""

char_to_hexadecimal = {'A':'00', 'B':'01', 'C':'02', 'D':'03', 'E':'04', 'F':'05', 'G':'06', 'H':'07', 
                'I':'08', 'J':'09', 'K':'0A', 'L':'0B', 'M':'0C', 'N':'0D', 'O':'0E', 'P':'0F', 
                'Q':'10', 'R':'11', 'S':'12', 'T':'13', 'U':'14', 'V':'15', 'W':'16', 'X':'17',
                'Y':'18','Z':'19','a':'00', 'b':'01', 'c':'02', 'd':'03', 'e':'04', 'f':'05', 'g':'06', 'h':'07', 
                'i':'08', 'j':'09', 'k':'0A', 'l':'0B', 'm':'0C', 'n':'0D', 'o':'0E', 'p':'0F', 
                'q':'10', 'r':'11', 's':'12', 't':'13', 'u':'14', 'v':'15', 'w':'16', 'x':'17',
                'y':'18','z':'19'}

hexadecimal_to_char = {'0':'A', '1':'B', '2':'C', '3':'D', '4':'E', '5':'F', '6':'G', '7':'H', 
                '8':'I', '9':'J', 'A':'K', 'B':'L', 'C':'M', 'D':'N', 'E':'O', 'F':'P', 
                '10':'Q', '11':'R', '12':'S', '13':'T', '14':'U', '15':'V', '16':'W', '17':'X',
                '18':'Y','19':'Z','a':'K', 'b':'L', 'c':'M', 'd':'N', 'e':'O', 'f':'P',}

hex_to_binary = {'0':'0000', '1':'0001','2':'0010','3':'0011','4':'0100','5':'0101','6':'0110','7':'0111',
                 '8':'1000','9':'1001','A':'1010', 'B':'1011', 'C':'1100', 'D':'1101', 'E':'1110', 'F':'1111',
                 'a':'1010', 'b':'1011', 'c':'1100', 'd':'1101', 'e':'1110', 'f':'1111'}

#Keys Substitution Boxes
s_box_key = {'0000':'9', '0001':'4','0010':'A','0011':'B','0100':'D','0101':'1','0110':'8','0111':'5',
            '1000':'6','1001':'2','1010':'0','1011':'3','1100':'C','1101':'E','1110':'F','1111':'7'}

inverse_s_box_key = {'0000': 'A', '0001':'5','0010':'9','0011':'B','0100':'1','0101':'7','0110':'8','0111':'F',
                 '1000':'6','1001':'0','1010':'2', '1011':'3', '1100':'C', '1101':'4', '1110':'D', '1111':'E'}

rc_j = {1:'01', 2:'02', 3:'04', 4:'08', 5:'10', 6:'20', 7:'40', 8:'80', 9:'1B', 10:'36'}

#Left rotate the string in key
def left_rotate(word,num):
  length = len(word)
  word[:] = word[num:length] + word[0:num]
  return word

#Calculating Xor of 2 values
def calculate_xor(list1,list2):
  xor_values = ['','','','']
  for i in range(0,len(list1)):
    a_1 = '0x' + list1[i] #Converting into hexa
    i_1 = int(a_1,16)
    a_2 = '0x' + list2[i]
    i_2 = int(a_2,16)
    a_3 = hex(i_1 ^ i_2)
    xor_values[i] = a_3[2:]
  return xor_values

#G_ Function used
def function_g(word,round_no):
  rotated_word = left_rotate(word,1) #Rotate by 1 byte

  b_dash = ['','','','']
  for i in range(0,4):
    character = rotated_word[i]
    if(len(character) == 1):
      character = '0'+character
    binary_1 = hex_to_binary[character[0]]
    binary_2 = hex_to_binary[character[1]]
    substituted_byte = s_box_key[binary_1] + s_box_key[binary_2] #Substituting the value
    b_dash[i] = substituted_byte
  
  rc_value = [rc_j[round_no], '00','00','00'] #Calculating the RC value
  xor_values = calculate_xor(rc_value,b_dash) #Xor of RC and the substituted obtained value
  return xor_values

function_g(['03', '05', '06', '07'],1)

def key_expansion(key):
  #Generation of w0,w1,w2,w3 - Round0
  w = [[],[],[],[]]         #Key input - 32 bytes - break into 4 parts
  for i in range(0,16,4): 
    s = key[i:i+4]
    hexa_w = ['','','',''] #Converting 4characters key to hexadecimal
    for j in range(0,4):
      s = s.upper()
      char_value = char_to_hexadecimal[s[j]]
      hexa_w[j] = char_value
    w[int(i/4)] = hexa_w

  subkey = [] # Storing 44 keys
  subkey.append(w)

  for i in range(1,11):
    w_3 = subkey[i-1][3] # Extracting last key 
    calculated = [[]]
    g_value = function_g(w_3,i) #Generating g function
    calculated[0] = g_value
    w_list = []

    for k in range(0,4):
      w_0 = subkey[i-1][0]
      w_4 = calculate_xor(w_0, calculated[0]) #XOR of keys upper and current
      calculated[0] = w_4
      w_list.append(w_4)

    subkey.append(w_list)
  print(subkey)
  return subkey

subkey = key_expansion("qwertyuiopasdfgh")

"""### **Encryption**"""

import numpy as np

#Substitution Box
s_box = [
    ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'],
    ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
    ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
    ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
    ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
    ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
    ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
    ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
    ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
    ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
    ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
    ['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
    ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
    ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
    ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
    ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']
]

#Mix Column Matrix
mix_column_matrix = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]
#Inverse Mix Column Matrix
inverse_mix_columns_matrix = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]

#Inverse Substitutiion Box
inv_s_box = [
    ['52', '09', '6A', 'D5', '30', '36', 'A5', '38', 'BF', '40', 'A3', '9E', '81', 'F3', 'D7', 'FB'],
   [ '7C', 'E3', '39', '82', '9B', '2F', 'FF', '87', '34', '8E', '43', '44', 'C4', 'DE', 'E9', 'CB'],
   [ '54', '7B', '94', '32', 'A6', 'C2', '23', '3D', 'EE', '4C', '95', '0B', '42', 'FA', 'C3', '4E'],
   [ '08', '2E', 'A1', '66', '28', 'D9', '24', 'B2', '76', '5B', 'A2', '49', '6D', '8B', 'D1', '25'],
   [ '72', 'F8', 'F6', '64', '86', '68', '98', '16', 'D4', 'A4', '5C', 'CC', '5D', '65', 'B6', '92'],
   [ '6C', '70', '48', '50', 'FD', 'ED', 'B9', 'DA', '5E', '15', '46', '57', 'A7', '8D', '9D', '84'],
   [ '90', 'D8', 'AB', '00', '8C', 'BC', 'D3', '0A', 'F7', 'E4', '58', '05', 'B8', 'B3', '45', '06'],
   [ 'D0', '2C', '1E', '8F', 'CA', '3F', '0F', '02', 'C1', 'AF', 'BD', '03', '01', '13', '8A', '6B'],
   [ '3A', '91', '11', '41', '4F', '67', 'DC', 'EA', '97', 'F2', 'CF', 'CE', 'F0', 'B4', 'E6', '73'],
   [ '96', 'AC', '74', '22', 'E7', 'AD', '35', '85', 'E2', 'F9', '37', 'E8', '1C', '75', 'DF', '6E'],
   [ '47', 'F1', '1A', '71', '1D', '29', 'C5', '89', '6F', 'B7', '62', '0E', 'AA', '18', 'BE', '1B'],
   [ 'FC', '56', '3E', '4B', 'C6', 'D2', '79', '20', '9A', 'DB', 'C0', 'FE', '78', 'CD', '5A', 'F4'],
   [ '1F', 'DD', 'A8', '33', '88', '07', 'C7', '31', 'B1', '12', '10', '59', '27', '80', 'EC', '5F'],
   [ '60', '51', '7F', 'A9', '19', 'B5', '4A', '0D', '2D', 'E5', '7A', '9F', '93', 'C9', '9C', 'EF'],
   [ 'A0', 'E0', '3B', '4D', 'AE', '2A', 'F5', 'B0', 'C8', 'EB', 'BB', '3C', '83', '53', '99', '61'],
   [ '17', '2B', '04', '7E', 'BA', '77', 'D6', '26', 'E1', '69', '14', '63', '55', '21', '0C', '7D']
]

character_int_value = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15, 'a':10, 'b':11, 'c':12, 'd':13, 'e':14, 'f':15}

#Add Round key
def addRound_key(list1,list2):
  result = [[],[],[],[]]
  for i in range(0,4):
    result[i] = calculate_xor(list1[i], list2[i]) #Calculating XOR of key and the input text
  return result

#Substitution
def substitution_bytes(list1):
  for i in range(0, len(list1)):
    for j in range(0, len(list1[i])):
      if (len(list1[i][j]) == 1):
        list1[i][j] = '0'+list1[i][j]
      s = list1[i][j]
      c_0 = character_int_value[s[0]]
      c_1 = character_int_value[s[1]]
      value = s_box[c_0][c_1] #Substitution using S Box
      list1[i][j] = value
  return list1
  
substitution_bytes([['EA', '04', '65', '85'], ['04', '04', '00', '17'], ['12', '12', '13', '19'], ['14', '00', '11', '19']])

#Shift left rows
def left_shift_rows(string_matrix):
  result = [['','','',''],['','','',''],['','','',''],['','','','']]
  for i in range(0,len(string_matrix)):
    current_row = string_matrix[i]
    for j in range(0,len(current_row)):
      result[i][j]=string_matrix[i][(j+i)%4] #Shifting the 2nd,3rd and 4th rows only
  return result

#Calculating the GF 2^8 multiplication
overflow_value = 0x100
modulus_value = 0x11B
def gf28_multiply(a1, b1) :
    sum_value = 0
    while (b1 > 0) :
        if (b1 & 1) :
          sum_value = sum_value ^ a1        
        b1 = b1 >> 1                      
        a1 = a1 << 1                          
        if (a1 & overflow_value) :
          a1 = a1 ^ modulus_value   
    return sum_value

#Mix Columns
def mix_Columns(state):
  result = [['','','',''],['','','',''],['','','',''],['','','','']]
  result_mat = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
  for i in range(0,len(state)):
    for j in range(0, len(state[i])):
      for k in range(0,len(state)):
        value_1 = '0x'+state[k][j]
        value_1 = int(value_1,16)
        result_mat[i][j] ^= gf28_multiply(mix_column_matrix[i][k],value_1) #Multiplying the matrices in GF(2^8)

  for i in range(0,len(state)):
    for j in range(0,len(state[i])):
      result[i][j] = str(hex(result_mat[i][j]))[2:]
  return result

mix_Columns([['87', 'F2', '4D', '97'], ['6E', '4C', '90', 'EC'], ['46', 'E7', '4A', 'C3'], ['A6', '8C', 'D8', '95']])

def convert_to_cipher(final_state):
  cipher_text = ''
  for i in range(0, len(final_state)):
    for j in range(0, len(final_state[i])):
      value_1 = '0x'+final_state[j][i]
      value_1 = int(value_1,16)
      cipher_text += chr(value_1) #Converting the hexadecimal value to character
  return cipher_text

def Encryption(original,subkey):
  original_state = [['','','',''],['','','',''],['','','',''],['','','','']]
  for i in range(0,16):
    original_state[int(i%4)][int(i/4)] = char_to_hexadecimal[original[i]]

  intermediate_states = []

  #Round0
  round0_key = subkey[0] #Subkey for round 0
  round0_state = addRound_key(round0_key, original_state)
  print("Round 0: "+ str(round0_state))
  intermediate_states.append(round0_state)

  #Round 1-9
  for round in range(1,10):
    state_1 = substitution_bytes(intermediate_states[-1])
    state_2 = left_shift_rows(state_1)
    state_3 = mix_Columns(state_2)
    state_4 = addRound_key(subkey[round],state_3)
    print("Round "+str(round) +": "+ str(state_4))
    intermediate_states.append(state_4)
  
  #Round10
  state_1 = substitution_bytes(intermediate_states[-1])
  state_2 = left_shift_rows(state_1)
  state_3 = addRound_key(subkey[10],state_2)
  print("Round 10: "+ str(state_3))
  intermediate_states.append(state_3)

  cipher_text = convert_to_cipher(intermediate_states[-1])
  print("Obtained Cipher Text: "+cipher_text)
  return cipher_text, intermediate_states[-1], intermediate_states

cipher_text,final_state, all_encrypted_states = Encryption("AAAAAAAAAAAAAAAA",subkey)

"""# **Decryption**"""

#Inverse Substitution
def inverse_substitution_bytes(list1):
  for i in range(0, len(list1)):
    for j in range(0, len(list1[i])):
      if (len(list1[i][j]) == 1):
        list1[i][j] = '0'+list1[i][j]
      s = list1[i][j]
      c_0 = character_int_value[s[0]]
      c_1 = character_int_value[s[1]]
      value = inv_s_box[c_0][c_1] #Substituting the values from Inverse S Box
      list1[i][j] = value
  return list1
  
inverse_substitution_bytes([['87', 'F2', '4D', '97'],
 ['F2', 'F2', '63', 'F0'],
 ['C9', 'C9', '7D', 'D4'],
 ['FA', '63', '82', 'D4']])

#Right Shift
def right_shift_rows(string_matrix):
  result = [['','','',''],['','','',''],['','','',''],['','','','']]
  for i in range(0,len(string_matrix)):
    current_row = string_matrix[i]
    for j in range(0,len(current_row)):
      result[i][j]=string_matrix[i][(j-i)%4] #Shifting the 2nd,3rd and 4th rows right by 1,2,3 bytes respectively
  return result

#Inverse Mix Columns
def inverse_mix_Columns(state):
  result = [['','','',''],['','','',''],['','','',''],['','','','']]
  result_mat = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
  for i in range(0,len(state)):
    for j in range(0, len(state[i])):
      for k in range(0,len(state)):
        value_1 = '0x'+state[k][j]
        value_1 = int(value_1,16)
        result_mat[i][j] ^= gf28_multiply(inverse_mix_columns_matrix[i][k],value_1) #Multiplying the matrices in GF(2^8)

  for i in range(0,len(state)):
    for j in range(0,len(state[i])):
      result[i][j] = str(hex(result_mat[i][j]))[2:]
  # print(result)
  return result

inverse_mix_Columns([['47', '40', 'a3', '4c'],
 ['37', 'd4', '70', '9f'],
 ['94', 'e4', '3a', '42'],
 ['ed', 'a5', 'a6', 'bc']])

def convert_to_plain(final_state):
  plain_text = ''
  for i in range(0, len(final_state)):
    for j in range(0, len(final_state[i])):
      plain_text += hexadecimal_to_char[final_state[j][i]] #Converting hexadecimal to char
  return plain_text

def Decryption(ciphertext,subkey):
  original_state = [['','','',''],['','','',''],['','','',''],['','','','']]
  for i in range(0,16):
    original_state[int(i%4)][int(i/4)] = hex(ord(ciphertext[i]))[2:]


  intermediate_states = []

  #Round 10
  state_1 = addRound_key(subkey[10],original_state) #Subkeys of round 10 - Used in reverse order
  state_2 = right_shift_rows(state_1)
  state_3 = inverse_substitution_bytes(state_2)
  print("Round 1: "+str(state_3))
  intermediate_states.append(state_3)

  #Round 9-1
  for round in range(9,0,-1):
    state_1 = addRound_key(subkey[round],intermediate_states[-1])
    state_2 = inverse_mix_Columns(state_1)
    state_3 = right_shift_rows(state_2)
    state_4 = inverse_substitution_bytes(state_3)
    print("Round "+str(11-round)+" :"+str(state_4))
    intermediate_states.append(state_4)
  
  #Round 0
  round0_key = subkey[0]
  round0_state = addRound_key(round0_key, intermediate_states[-1])
  print("Round 0: "+str(round0_state))
  intermediate_states.append(round0_state) 

  plain_text = convert_to_plain(intermediate_states[-1])
  print("Decrypted Plain Text: "+plain_text)
  return plain_text, intermediate_states[-1], intermediate_states

plain_text, final_state, all_decrypted_states = Decryption(cipher_text,subkey)

if __name__ == "__main__":
  key = str(input("Enter the Key (16 characters): ")) #Enter the key
  subkey = key_expansion(key)
  print("\n\n")
  for i in range(0,2):
    print("Sequence "+str(i+1))
    print("\nEncrytion")
    plaintext = str(input("Enter the Plain Text (length 16 characters = 128 bits){}: ".format(i+1))) #Enter 5 Plain Texts
    cipher_text,final_state, all_encrypted_states = Encryption(plaintext,subkey) #Encrypting the plaintext
    print("\nDecryption")
    plain_text, final_state, all_decrypted_states = Decryption(cipher_text,subkey) #Decrypting the ciphertext
    print("\n")
    print("\n")