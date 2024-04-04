import re

class MixedRegexpParser:
    def __init__(self, pattern):
        self.pattern = pattern
        self.pattern = re.sub(r"<'([^,]+)','([^>]+)'>", r"<'\1','(?:[^']+,)?\2(?:,[^']+)?'>", self.pattern)
        self.pattern = re.compile(self.pattern)
        
    def parse(self, tags):
        text = ''.join(f"<'{tag[0]}','{tag[1]}'>" for tag in tags)
        matches = self.pattern.findall(text)
        if matches:
            parsed_matches = []
            if isinstance(matches[0], str):
                matches = [matches]
            for match in matches[0]:
                parsed_matches.append([])
                for item in match[1:-1].split('><'):
                    word, tag = item.split("','")
                    word = word[1:]
                    tag = tag[:-1]
                    parsed_matches[-1].append((word, tag))
            named_groups = {}
            for group in self.pattern.groupindex:
                named_groups[group] = parsed_matches[self.pattern.groupindex[group] - 1]
            return parsed_matches, named_groups