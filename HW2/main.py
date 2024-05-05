from hazm import POSTagger, word_tokenize, Chunker, tree2brackets, Normalizer

from task_extractor.extractor import TaskExtractor


normalizer = Normalizer()

sent = 'یادم‌ باشه هر روز ساعت 8 صبح به جلسه اسکرام برم.'
sent = normalizer.normalize(sent)
extractor = TaskExtractor()
res = extractor.run(sent)
print(res)

# tagger = POSTagger(model='models/pos_tagger.model')
# tagged = tagger.tag(word_tokenize(sent))
# print(tagged)
#
# chunker = Chunker(model='models/chunker.model')
# print(tree2brackets(chunker.parse(tagged)))
