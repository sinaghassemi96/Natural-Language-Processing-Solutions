# Report
## Description
This module is for extracting tasks from text data using regular expressions and classical models.
## Installation
- Install the requirements:
Currently, the only requirement is `hazm` which can be installed using the following command:
```
pip install -r requirements.txt
```
## Usage
- Run the following command to extract tasks from the text:
```python
text = '''
باید تسک حل تمرین دوم درس را در یک آذر شروع کنیم و تا ده آذر تمام کنیم.
برای اینکار باید اول موضوع را مشخص کنیم و بعد پیاده‌سازی را انجام دهیم.
افراد مسئول حل این تمرین آرش و ریحانه هستن.
ددلاین تسک به 15 آذر منتقل شد.
تسک حل تمرین دوم درس تمام شد.
'''
tasks = TaskExtractor().run(text)
```
This code results in:
```json
[{
    "name": "حل تمرین دوم درس",
    "subtasks": [
        "موضوع را مشخص کنیم",
        "پیاده‌سازی را انجام دهیم"
    ],
    "assignees": [
        "آرش",
        "ریحانه"
    ],
    "start_date": "یک آذر",
    "end_date": "۱۵ آذر",
    "is_done": true
}]
```
## Explaination
We work using regular expressions. We wanted to enhance the quality of results since the patterns were quite diverse and using blind regular expressions would result in a lot of false positives. We used the POS tagger of `hazm` to extract the verbs and nouns and then used them in our regular expressions. We also used the `hazm`'s `normalizer` to normalize the text before extracting the tasks. To use tags along with regular expression we developed `MixedRegexParser` class to parse patterns with tags. Imagine a pattern like this:
```
I love to eat {NOUN} with {NOUN}
```
this pattern matches `I love to eat pizza with soda` but not `I love to eat delicious and pretty`. We used this class to parse the patterns and then used the parsed patterns to extract the tasks. for example a pattern like this:
```
تسک {NP} به {DATE} منتقل شد
```
would match `تسک حل تمرین دوم به ۱۵ آذر منتقل شد` but not `تسک حل تمرین دوم به علی منتقل شد`. We defined patterns starting from `NOUN` and `ADJ` to `NP`, `NP_GROUP` and `DATETIME` to define more complex patterns like `TASK_DECLARATION` and `TASK_DEADLINE_UPDATE`.
the code was written with clean code and clarity in mind. We tried to make the code as readable as possible. We also used `unittest` to test the code and make sure that it works as expected. More patterns can easily be added to the `patterns.py` file and the code would work as expected since the extraction is done using regular expressions group names.
```
{AGG_WORDS('NOUN', TASK_WORDS)}(?P<NAME>{NP}){ADP}(?<END_DATE>{DATE}){VP}
```
`AGG_WORDS` matches multiple words in the list which is `TASK_WORDS` that includes `تسک` and `وظیفه` with the given tag. `VP` matches a verb phrase and `ADP` matches a preposition. `NP` matches a noun phrase and `DATE` matches a date. `NAME` and `END_DATE` are the group names that are used to extract the name and end date of the task.
