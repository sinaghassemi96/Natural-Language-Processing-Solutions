from hazm import Normalizer

from task_extractor.extractor import TaskExtractor

normalizer = Normalizer()

# sent = 'یادم‌ باشه هر روز ساعت 12 ظهر به یادگیری برنامه‌نویسی بپردازم.'
# sent = 'جلسه اسکرام روزانه‌ام را لغو کن.'
# sent = 'کار تماس با دوستم انجام شد.'
# sent = 'زمان تماس با دوستم در 12 فروردین را به 9:30 شب تغییر بده.'
sent = 'برنامه هفتگی‌ام را نشان بده.'
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