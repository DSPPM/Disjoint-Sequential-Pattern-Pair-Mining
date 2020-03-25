import time

def dict_add(dic, key, value) :
  if key in dic.keys() :
    dic[key].add(value)
  else :
    dic[key] = set(value)

def dict_in(dic, key, value) :
  if not key in dic.keys() :
    return False 
  return value in dic[key]
  
hash_table = {}
support_table = {}
result = []
candidate_item = set([])
closed = []

diamonds = []
with open('dummy_diamond_11.txt', 'r', encoding = 'utf-8') as file :
  x = file.readline()
  y = file.readline()
  z = file.readline()  
  while len(x) > 0 and len(y) > 0 :
    diamonds.append((x, y))
    x = file.readline()
    y = file.readline() 
    z = file.readline() 
    
for (x, y) in diamonds :
  lstx = x.strip().split(' ')
  lsty = y.strip().split(' ')
  
  lstx2 = lstx[1].split('---->')    
  lsty2 = lsty[1].split('---->')  
  for item in lstx2 :
    candidate_item.add(item)    
  for item in lsty2 :
    candidate_item.add(item)
    
  result.append((int(lstx[0]), lstx2, int(lsty[0]), lsty2))
  dict_add(hash_table, lsty[1].strip(), lstx[1].strip())
  dict_add(hash_table, lstx[1].strip(), lsty[1].strip())
  support_table[lstx[1].strip()] = int(lstx[0])
  support_table[lsty[1].strip()] = int(lsty[0])

print(len(diamonds))
  
maximal_set = []
closed_set = []

starttime = time.time()
for (supportx, patternx, supporty, patterny) in result :
  ori_patternx = '---->'.join(patternx)
  ori_patterny = '---->'.join(patterny)
  max = True 
  closed = True
  
  for pos in range(len(patternx)) :
    for item in candidate_item :
      extend = '---->'.join(patternx[ : pos] + [item] + patternx[pos : ])
      
      if dict_in(hash_table, ori_patterny, extend) :
        max = False
        extend_support = support_table[extend]
        if extend_support >= supportx :
          closed = False
          break
    if not closed :
      break
      
  for pos in range(len(patterny)) :
    for item in candidate_item :
      extend = '---->'.join(patterny[ : pos] + [item] + patterny[pos : ])
      
      if dict_in(hash_table, ori_patternx, extend) :
        max = False
        extend_support = support_table[extend]
        if extend_support >= supporty :
          closed = False
          break
    if not closed :
      break
  
  if max :
    maximal_set.append((supportx, patternx, supporty, patterny))
  elif closed :
    closed_set.append((supportx, patternx, supporty, patterny))
endtime = time.time()

print((endtime - starttime))
print(len(maximal_set), len(closed_set), len(result))
with open('dummy_maximal11.txt', 'w', encoding = 'utf-8') as file:
  for pair in maximal_set :
    supp1, seq1, supp2, seq2 = pair
    file.write(str(supp1) + ' ' + '---->'.join(seq1) + '\n')
    file.write(str(supp2) + ' ' + '---->'.join(seq2) + '\n')
    file.write('\n')
with open('dummy_closed11.txt', 'w', encoding = 'utf-8') as file:
  for pair in closed_set :
    supp1, seq1, supp2, seq2 = pair
    file.write(str(supp1) + ' ' + '---->'.join(seq1) + '\n')
    file.write(str(supp2) + ' ' + '---->'.join(seq2) + '\n')
    file.write('\n')
