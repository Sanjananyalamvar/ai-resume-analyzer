def semantic_available():
    try:
        import sentence_transformers  # noqa
        return True
    except Exception: return False

def semantic_scores(text, roles_df):
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        role_text=[]
        for _,r in roles_df.iterrows():
            req=r['required_skills'] if isinstance(r['required_skills'],list) else str(r['required_skills']).split('|')
            role_text.append(str(r.get('role',''))+' '+' '.join(req)+' '+str(r.get('keywords','')))
        emb=model.encode([text]+role_text,normalize_embeddings=True)
        return [float(x) for x in cosine_similarity([emb[0]],emb[1:])[0]]
    except Exception: return None
