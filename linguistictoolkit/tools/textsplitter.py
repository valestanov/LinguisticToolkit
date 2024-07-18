from typing import List, Dict

class Lemma:
    def __init__(self, original: str, for_match: str = None, in_dict: bool = None, is_lang: bool = None, properties = None, dict_content = None, pos: int = None):
        self.original = original  # 原始单词
        self.for_match = for_match if for_match is not None else self.original.lower()  # 用于匹配的单词，默认为小写的原始单词
        self.in_dict = in_dict  # 是否在字典中
        self.is_lang = is_lang
        self.properties = properties if properties is not None else {} # 属性
        self.dict_content = dict_content if dict_content is not None else {}  # 字典内容
        self.pos = pos  # 单词在句子中的位置
        self.isFocus = False #是否当前光标聚焦

class SentenceSplitter:
    def __init__(self, word_list: List[Lemma]):
        # word_list 是包含 Lemma 类元素的列表
        self.word_list = word_list
        self._update_positions()

    def __iter__(self):
        return iter(self.word_list)

    def __getitem__(self, index):
        return self.word_list[index]

    def _update_positions(self):
        """更新每个单词在句子中的位置，用于决定光标位置"""
        current_pos = 0
        for word in self.word_list:
            word.pos = current_pos
            current_pos += len(word.original)

    def compare_entry(self, entry: str, start_index: int, word_count: int) -> int:
        """比较给定的 entry 与 word_list 中从 start_index 开始的 word_count 个单词的匹配情况"""
        end_index = start_index + word_count
        words_to_compare = self.word_list[start_index:end_index]
        
        if any(w.in_dict for w in words_to_compare):
            # 遇到了已经检查过的单词，停止比较
            return 0
        
        combined_word = ''.join(w.for_match for w in words_to_compare)
        
        if combined_word == entry:
            # 完全匹配
            return 1
        elif combined_word == entry[:len(combined_word)]:
            # 部分匹配，继续比较
            return 2
        else:
            # 不匹配
            return 0

    def compare_vocabulary(self, vocabulary: List[str]):
        """比较单词列表与字典词汇"""
        sorted_vocab = sorted(vocabulary, key=len, reverse=True)
        full_match_string = ''.join(w.for_match for w in self.word_list)
        total_words = len(self.word_list)
        
        for entry in sorted_vocab:
            if entry in full_match_string:
                current_index = 0
                while current_index < total_words:
                    for word_count in range(1, total_words - current_index + 1):
                        match_result = self.compare_entry(entry, current_index, word_count)
                        
                        if match_result == 0:
                            break  # 停止当前起点的匹配，进行下一个起点的匹配
                        elif match_result == 2:
                            continue  # 部分匹配，继续拉伸匹配
                        elif match_result == 1:
                            # 完全匹配
                            end_index = current_index + word_count
                            matched_words = self.word_list[current_index:end_index]
                            new_original = ''.join(w.original for w in matched_words)
                            new_for_match = ''.join(w.for_match for w in matched_words)
                            new_properties = self.word_list[current_index].properties
                            new_is_lang = self.word_list[current_index].is_lang
                            new_word = Lemma(new_original, for_match=new_for_match, in_dict=True, is_lang = new_is_lang, properties=new_properties)
                            
                            # 更新单词列表
                            self.word_list = self.word_list[:current_index] + [new_word] + self.word_list[end_index:]
                            self._update_positions()
                            total_words = len(self.word_list)
                            break  # 重新从下一个起点开始匹配
                    current_index += 1
        return None

    def set_word_focus(self, pos: int) -> int:
        for word in self.word_list:
            if word.pos <= pos < word.pos + len(word.original):
                word.isFocus = True
            else:
                word.isFocus = False
