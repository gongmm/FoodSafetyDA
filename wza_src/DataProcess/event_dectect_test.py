import os
import gensim
from doc_2_vec import sent2vec

model_dir = 'model'


def test_doc_sim(doc1, doc2):
    i = 0
    model_path = os.path.join(model_dir, "doc2vec" + str(i) + ".model")
    model = gensim.models.Doc2Vec.load(model_path)
    doc1 = doc1.split()
    doc2 = doc2.split()
    vec1_1 = model.infer_vector(doc1)
    vec2_1 = model.infer_vector(doc2)
    vec1_2 = sent2vec(model, doc1)
    vec2_2 = sent2vec(model, doc2)
    sim1 = test_get_sim(vec1_1, vec2_1)
    print(sim1)
    sim2 = test_get_sim(vec1_2, vec2_2)
    print(sim2)


def test_get_sim(a_vect, b_vect):
    dot_val = 0.0
    a_norm = 0.0
    b_norm = 0.0
    cos = None
    for a, b in zip(a_vect, b_vect):
        dot_val += a * b
        a_norm += a ** 2
        b_norm += b ** 2
    if a_norm == 0.0 or b_norm == 0.0:
        cos = -1
    else:
        cos = dot_val / ((a_norm * b_norm) ** 0.5)
    return cos