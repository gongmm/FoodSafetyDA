import  pickle
with open ('../maps.pkl','rb') as f:
    char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
    print (char_to_id)