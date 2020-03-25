import csv
import pickle
import time

result = []
with open('results.pkl', 'wb') as file :
  pickle.dump(result, file)
  
level = 'lv3'
full_name = 'all_trans_' + level + '.csv'
      
db = [(1, [1, 2, 3, 4, 5, 6]),
      (2, [1, 2, 1, 4, 5, 6]),
      (3, [3, 4, 5, 6]),
      (4, [2, 4, 5, 6]),
      (5, [1, 2, 4, 5, 6]),
      (6, [2, 2, 4, 5, 6])]

db = []
with open(full_name) as file :
  reader = csv.reader(file)
  for seq in reader :
    db.append(seq)
    
def dict_append(dic, key, element) :
  if key in dic.keys() :
    dic[key].append(element)
  else :
    dic[key] = [element]

def dict_add(dic, key, element) :
  if key in dic.keys() :
    dic[key].add(element)
  else :
    dic[key] = set([element])
    
def choose(cur_set, choosable_p, include_items, appear_in_sequences, min_inset_sup) :
  choosable = choosable_p.copy()
  result = []
  extended = False
  
  for item in sorted(list(choosable_p)) :
    choosable.discard(item)
    if len(appear_in_sequences[item]) >= min_inset_sup :
      extended = True
      
      choosable1 = choosable.copy()
      for seq in appear_in_sequences[item] :
        for item1 in include_items[seq] :
          choosable1.discard(item1)
          
      result.extend(choose(cur_set + [item], choosable1, include_items, appear_in_sequences, min_inset_sup))
  
  if not extended and len(cur_set) >= 2 :
    return result + [cur_set]
  else :
    return result

def mine(db_map, end_db_map, now_prefix, min_sup, min_inset_sup, available, end) :
  global db
  global result
  
  projected_db_map = {}
  projected_end_db_map = {}
  now_proj_pos = {}
  now_db_serial_num = {}
  
  for (serial_num, (seq_id, proj_pos)) in enumerate(db_map) :
    if end_db_map != {} :
      seq = db[seq_id][proj_pos : end_db_map[serial_num][1]]
    else :
      seq = db[seq_id][proj_pos : ]
      
    now_proj_pos[seq_id] = proj_pos
    now_db_serial_num[seq_id] = serial_num
    prefix_set = set([])
    
    for (item_id, item) in enumerate(seq, start = proj_pos) :
      if not item in prefix_set :
        dict_append(projected_db_map, item, (seq_id, item_id + 1))
        dict_append(projected_end_db_map, item, (seq_id, item_id + 1))
        prefix_set.add(item)
      projected_end_db_map[item][-1] = (seq_id, item_id + 1)
      
  #if len(now_prefix) > 0 and now_prefix[-1] == ['5314']:  
  #  print('SAY_HELLO', projected_end_db_map['4592'])
  #  print('SAY_HELLO', projected_db_map['4592'])
    
  for item in projected_db_map.keys() :
    if len(now_prefix) > 0 and item in now_prefix[-1] and end != '-1':
      continue
      
    now_support = len(projected_db_map[item])

    if now_support >= min_sup :
      if len(now_prefix) == 1 and end == '-1':
        include_items = {}
        appear_in_sequences = {}
        
        next_db_map = projected_db_map[item].copy()
        
        for (serial_num, (seq_id, proj_pos)) in enumerate(projected_end_db_map[item]) :
          seq = db[seq_id]
          cur_proj_pos = now_proj_pos[seq_id]
          reverse_proj_pos = proj_pos
          
          next_db_map[serial_num] = (seq_id, cur_proj_pos)        
          
          for (item_id2, item2) in enumerate(seq[cur_proj_pos : reverse_proj_pos], start = cur_proj_pos) :
            dict_add(include_items, seq_id, item2)
            dict_add(appear_in_sequences, item2, seq_id)
          
        choosable = set([])
        for item2 in appear_in_sequences :
          if len(appear_in_sequences[item2]) >= min_inset_sup :
            choosable.add(item2)
            
        choose_results = choose([], choosable, include_items, appear_in_sequences, min_inset_sup)
        
        if now_prefix[-1] == ['5314'] and item == '4765':
          print(projected_end_db_map['4592'])
          print(projected_db_map['4592'])
          print(appear_in_sequences['4592'])
          
        now_available = set([])
        if len(choose_results) > 0 :
          result.append((now_support, now_prefix + [[item]]))
          for choose_result in choose_results :
            for item2 in choose_result :
              now_available.add(item2)
              
            result.append((now_support, now_prefix + [choose_result] + [[item]]))
          
          #if now_prefix[-1] == ['5314'] :
          #  print('5400' in now_available)
          #  print(now_available)                  
          mine(next_db_map, projected_end_db_map[item], now_prefix, min_sup, min_inset_sup, now_available, item)
      else :
        if end != '-1' :
          if not item in available :
            continue
          if item != end :
            result.append((now_support, now_prefix + [[item]] + [[end]]))
            mine(projected_db_map[item], end_db_map, now_prefix + [[item]], min_sup, min_inset_sup, available, end)
        else :
          result.append((now_support, now_prefix + [[item]]))
          mine(projected_db_map[item], {}, now_prefix + [[item]], min_sup, min_inset_sup, [], '-1')
    
proj_list = [(i, 0) for (i, seq) in enumerate(db)]
    
start_time = time.time()
mine(proj_list, {}, [], 7, 7, set([]), '-1')
end_time = time.time()

print(end_time - start_time)

output_file = open('st_7.txt', 'w', encoding = 'utf-8')

address = {}
with open('places_' + level + '.txt', 'r', encoding = 'utf-8') as file :
  xx = file.readline()
  while len(xx) > 0 :
    xxx = xx.strip().split(' ')
    address[xxx[0]] = xxx[2]
    xx = file.readline()

with open('results.pkl', 'wb') as file :
  pickle.dump(result, file)
  
string_result = []
for pattern in result :
  support, seq = pattern
  string_result.append((support, '---->'.join([','.join([address[item] for item in itemset]) for itemset in seq])))
  
#string_result.sort(reverse=True)
    
for pattern in string_result :
  support, seq = pattern
  output_file.write(str(support) + ' ' + seq + '\n')
  '''
  output_file.write('---->'.join([address[s] for s in seq]) + '\n')
  output_file.write('=='.join(['(' + ','.join([address[item] for item in list(st)]) + ')' for st in interval]))
  output_file.write('\n')
  '''