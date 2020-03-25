import time
def dict_add(dic, key, value) :
  if key in dic.keys() :
    dic[key] += value
  else :
    dic[key] = value
  
def set_value(dic, a, b, value) :
  if a in dic.keys() :
    dic[a][b] = value 
  else :
    dic[a] = {}
    dic[a][b] = value

def check_prime(a, b, prime) :
  for item in a[1 : -1] :
    for item2 in b[1 : -1] :
      if not item in prime.keys() or not item2 in prime[item].keys() :
        return False
  return True
  
length_map = {}
groups = []
group_primes = []
with open('st_7.txt', 'r', encoding = 'utf-8') as file :
  xx = file.readlines()

starttime = time.time()
cur_start = ''
cur_end = ''
for x in xx :
  #x = file.readline()   
  #while len(x) > 0 :
  llist = x.strip().split(' ')
  list = llist[1].strip().split('---->')
  if len(list) > 1 and ',' in list[1] :
    list2 = list[1].split(',')
    
    if list[0] != cur_start or list[2] != cur_end:
      cur_start = list[0]
      cur_end = list[2]
    #if len(group[-1]) == 0 :
    #  print(cur_start, cur_end)
      groups.append([])
      group_primes.append({})
    for item in list2 :
      for item2 in list2 :
        if item != item2 :
          set_value(group_primes[-1], item, item2, 1)
  else :
    dict_add(length_map, len(list), 1)
    if len(list) >= 3 and list[0] == cur_start and list[-1] == cur_end:
      groups[-1].append((llist[0], list))
      
    #x = file.readline()

for length in length_map.keys() :
  print(length, length_map[length])

pairs = []

for group_num, group in enumerate(groups) :
  for i, (supp1, seq1) in enumerate(group) :
    for j, (supp2, seq2) in enumerate(group[i + 1 : ], start = i + 1) :
      if check_prime(seq1, seq2, group_primes[group_num]) :
        pairs.append((seq1, seq2, supp1, supp2))
endtime = time.time()
print((endtime - starttime))        
          
with open('diamond_7.txt', 'w', encoding = 'utf-8') as file :  
  for pair in pairs :
    seq1, seq2, supp1, supp2 = pair
    file.write(supp1 + ' ' + '---->'.join(seq1) + '\n')
    file.write(supp2 + ' ' + '---->'.join(seq2) + '\n')
    file.write('\n')