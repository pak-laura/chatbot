
import sys
from nltk.tokenize import word_tokenize
import string
import spacy


#user = input('hello: ')
user = 'There are more things on heaven and earth, Horatio, than are dreamt of in your philosophy. It is a distutils installed project, and thus, we cannot accurately determine which files belong to it, which would lead to only a partial uninstall. Hello, please say hi without going crazy. If you cross this line, you\'re trespassing. The window was shattered. He broke the window.'


nlp = spacy.load('en_core_web_sm')
doc = nlp(user)
sentences = list(doc.sents)

for sent in sentences:
   print('\n', sent)
   sent_doc= nlp(sent.text)
   root = [token for token in sent_doc if token.dep_ == 'ROOT'][0]
   print('root is', root)

   # find subject
   subject = None
   for token in root.lefts:
      if token.dep_ in ['nsubj', 'nsubjpass']:
         subject = token
         if subject.dep_ == 'nsubjpass':
            passive = True
         else:
            passive = False
         break
   if not subject:
      print('error: did not find subject')
      continue
   print('subject =', subject, 'passive =', passive)

# first sentence
sample = nlp(sentences[0].text)
# print attributes of each token
print('\nsentence1 tokens, text lemma pos is_stop')
for token in sample:
   print(token.text, token.lemma_, token.pos_, token.is_stop)

# check for named entities
# needs the uppercase to help it
print('\nnamed entities of doc')
for ent in doc.ents:
   print(ent.text, ent.label_)

# get noun chunks
print('\nNoun Chunks of doc')
noun_chunks = list(doc.noun_chunks)
print(noun_chunks[:])








