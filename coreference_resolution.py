def resolve_coref(input_str):
    import re
    import spacy
    nlp = spacy.load('en')
    import neuralcoref
    neuralcoref.add_to_pipe(nlp)
    input_str=input_str.lower()
    doc = nlp(input_str)
    replace_coref_list=['he','she','him','her','it','his']
    if doc._.has_coref==True:
        no_of_items = len(doc._.coref_clusters)
        for i in range(no_of_items): 
            word=str(doc._.coref_clusters[i][1])
            coref=str(doc._.coref_clusters[i][0])
#            print(word)
            if word in replace_coref_list:
                input_str=re.sub(r'\b'+word+r'\b',coref,input_str)
    return input_str
            
#take_input=input('enter sent: ')
#print(resolve_coref(take_input))