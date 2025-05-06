import re
from typing import Callable, Optional, Dict, List
from linguistictoolkit.tools.langsplitter import split_text_by_char, split_text_by_word, split_text_sea_lang
from linguistictoolkit.tools.textsplitter import Lemma, SentenceSplitter
from linguistictoolkit.tools.langdeterminer import islang_by_name

class SplitterEngine:
    def __init__(self, func_list=None, lang: Optional[str] = None, islang: Optional[Callable[[str],bool]] = None):
        self.splitter_dict = {
            'char': split_text_by_char,
            'word': split_text_by_word,
            'sea': split_text_sea_lang
        }
        if func_list:
            for func in func_list:
                self.introduce_func(func)
        self.splitter = split_text_by_word
        self.lang = lang
        self.islang = islang

    def introduce_func(self, func):
        func = self._convert_to_lemma(func)
        if func is not None:
            self.splitter_dict[func.__name__] = func

    def _convert_to_lemma(self, func):
        test_str = "a"
        try:
            result = func(test_str)
            if isinstance(result, list):
                return lambda string: SentenceSplitter(func(string))
            elif isinstance(result, SentenceSplitter):
                return func
            else:
                return None
        except:
            return None
            
    def _check_empty_string(self, value: str) -> Optional[None]:
        if value.strip() == '':
            return None
        return value

    def get_splitter_dict(self):
        return list(self.splitter_dict.keys())

    def set_splitter(self, func_name: str) -> None:
        # 更新当前使用的显示函数
        if func_name not in self.splitter_dict:
            raise ValueError(f"Function {func_name} not found in splitter_dict")
        self.splitter = self.splitter_dict[func_name]

    def get_splitter_name(self) -> str:
        for name, func in self.splitter_dict.items():
            if func == self.splitter:
                return name
        return ''

    def split(self, text: str, lang: Optional[str] = None, islang: Optional[Callable[[str], bool]] = None) -> SentenceSplitter:
        if lang is None:
            lang = self.lang
        if islang is None:
            islang = self.islang
        if self.splitter is not None:
            return self.splitter(text, lang=lang, islang = islang)
        else:
            raise ValueError("No splitter function set.")

    def set_is_lang_by_regex(self, regex: str) -> None:
        normalized_regex = regex.strip().lower()
        if self._check_empty_string(regex) is None:
            self.islang = None
            return
        
        islang = islang_by_name(normalized_regex)
        if islang != None:
            self.islang = islang
            return

        self.islang = lambda x:bool(re.match(regex,x))
            
    def set_language(self, lang: str) -> None:
        self.lang = lang

class LookupEngine:
    def __init__(self, func_list=None, dictionary_file=None, general_func_list = None, index_column=1):
        self.introduced_func_list = {"默认": self.default_func}
        if func_list:
            for func in func_list:
                self.introduce_func(func)
        
        self.general_func_list = {}
        if general_func_list:
            for func in general_func_list:
                self.introduce_gen_func(func)

        self.func_list = self.introduced_func_list
        self.key_func_list = []
        self.dictionary_file = dictionary_file
        if self.dictionary_file:
            self.dictionary_file = self.dictionary_file.strip()
        self.dictionary = {}
        self.index_column = index_column
        self.cache_dictionary = {}
        self.vocab = []
        self.load_dictionary()

    def default_func(self):
        return None

    def introduce_func(self, func):
        func = self._convert_to_lemma(func)
        if func is not None:
            self.introduced_func_list[func.__name__] = func

    def introduce_gen_func(self, func):
        func = self._convert_to_lemma(func)
        if func is not None:
            self.general_func_list[func.__name__] = func
    
    def _convert_to_lemma(self, func):
        test_str = "a"
        test_lemma = Lemma("a")
        try:
            result = func(test_str)
            return lambda lemma: func(lemma.original)
        except:
            try:
                result = func(test_lemma)
                return func
            except:
                return None

    def renew_vocab(self):
        self.vocab = list(self.dictionary.keys())

    def clear_cache(self):
        self.cache_dictionary = {}

    def load_dictionary(self):
        try:
            import pandas as pd

            #防止错误的处理"Nan","Na"等字符
            default_nan_values = ['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A N/A', '#N/A', 'N/A', 'n/a', '#NA', '']

            if self.dictionary_file.endswith('.xls') or self.dictionary_file.endswith('.xlsx'):
                df = pd.read_excel(self.dictionary_file,sheet_name=0,na_values=default_nan_values, keep_default_na=False)
            elif self.dictionary_file.endswith('.txt'):
                df = pd.read_csv(self.dictionary_file, encoding='utf-8', delimiter='\t',na_values=default_nan_values, keep_default_na=False)
            elif self.dictionary_file.endswith('.csv'):
                df = pd.read_csv(self.dictionary_file, encoding='utf-8',na_values=default_nan_values, keep_default_na=False)
            else:
                raise ValueError("Unsupported file type")
        except Exception as e:
            raise_flag = False
            if (self.dictionary_file and self.dictionary_file.strip()):
                raise_flag = True
            self.dictionary_file = None
            self.dictionary = {}
            self.func_list = self.introduced_func_list
            self.renew_vocab()
            if raise_flag:
                raise e
            else:
                return

        df.dropna(how = 'all',inplace = True)
        rows = df.values.tolist()
        max_columns = max(len(row) for row in rows)

        log_info = ''

        for row in rows:
            key = row[self.index_column - 1]
            try:
                if (key and key.strip()):
                    #藏语特殊处理
                    key = key.strip('་ ')
                    if key not in self.dictionary:
                        self.dictionary[key] = {f"列{i+1}": str(row[i]) for i in range(len(row))}
                    else:
                        for i in range(len(row)):
                            if f"列{i+1}" not in self.dictionary[key]:
                                self.dictionary[key][f"列{i+1}"] = str(row[i])
                            else:
                                self.dictionary[key][f"列{i+1}"] += ("|" + str(row[i]))
            except Exception as e:
                log_info += f'读取失败：{key}, {str(row)}'
                continue
        
        if log_info != "":
            raise ValueError(f"部分数据读取失败：\n{log_info}")


        def create_func(column):
            return lambda lemma: self.dictionary.get(lemma.for_match, {}).get(column, lemma.original)

        self.func_list = {f"列{i+1}": create_func(f"列{i+1}") for i in range(max_columns)}
        self.func_list.update(self.introduced_func_list)

        self.renew_vocab()

    def update_dictionary_file(self, new_dictionary_file, new_index_column=1):
        if new_dictionary_file:
            self.dictionary_file = new_dictionary_file
        else:
            self.dictionary_file = None
        if new_index_column:
            self.index_column = new_index_column
        self.dictionary = {}
        self.load_dictionary()
        self.clear_cache()

    def update_key_func_list(self, key_func_list):
        for _, func in key_func_list:
            if func not in self.func_list:
                raise ValueError(f"Function {func} not found in func_list")
        self.key_func_list = key_func_list
        self.clear_cache()
        
    def lookup_word(self, lemma):
        for key, func in self.key_func_list:
            try:
                lemma.dict_content[key] = self.func_list[func](lemma)
            except:
                lemma.dict_content[key] = lemma.original

    def lookup(self, split_text):
        split_text.compare_vocabulary(self.vocab)
        for lemma in split_text:
            if lemma.original in self.cache_dictionary:
                lemma.dict_content = self.cache_dictionary[lemma.original]
            else:
                self.lookup_word(lemma)
                self.cache_dictionary[lemma.original] = lemma.dict_content
            for func in self.general_func_list.values():
                func(lemma)

    def get_func_list(self) -> List[str]:
        # 获取函数列表
        return list(self.func_list.keys())
        
class DisplayerEngine:
    def __init__(self, func_list: Optional[List[Callable]] = None, isFocus: bool = True, isNew: bool = True, format_string: str = "<span>%s</span>", font: str = "Arial", font_size: int = 16, rainbow: bool = True, spec_rules: str = "", key: str = ""):
        self.introduced_func_list = {"默认": self.default_func}
        if func_list:
            for func in func_list:
                self.introduce_func(func)
        self.func_list = self.introduced_func_list
        self.current_func = self.default_func
        self.new_word = isNew
        self.highlight = isFocus
        self.format_string = ""
        self.set_format_string(format_string)
        self.font = font
        self.font_size = font_size
        self.rainbow = rainbow
        self.spec_rules_list = self.parse_spec_rules(spec_rules)
        self.key = key

    def display_word(self, lemma: Lemma, index: int) -> str:
        # 将 Lemma 对象转换为 HTML 文本
        if self.current_func is not None:
            output = self.current_func(lemma)
        else:
            output = self.default_func(lemma)
            
        output = output.replace('\n','<br>')
        output = self.apply_rainbow(output, index)
        output = self.apply_new_word(output,lemma)
        output = self.apply_spec_rules(output,lemma)
        output = self.apply_highlight(output, lemma)
            
        return output

    def display(self, split_text: SentenceSplitter) -> str:
        output_html = ''
        # 将整个 SentenceSplitter 对象转换为 HTML 文本
        for index, lemma in enumerate(split_text):
            output_html += self.display_word(lemma, index)
        return output_html

    def get_cursor_text(self, split_text: SentenceSplitter) -> str:
        output_html = ''
        # 将整个 SentenceSplitter 对象转换为 HTML 文本
        for index, lemma in enumerate(split_text):
            output_html += self.display_word(lemma, index)
            if lemma.isFocus:
                break
            #在焦点处结束
        return output_html

    def introduce_func(self, func):
        func = self._convert_to_lemma(func)
        if func is not None:
            self.introduced_func_list[func.__name__] = func
            
    def _convert_to_lemma(self, func: Callable) -> Optional[Callable]:
        # 转换函数，确保其能处理 Lemma 对象
        test_str = "a"
        test_lemma = Lemma("a")
        try:
            result = func(test_str)
            return lambda lemma: func(self._word_text(lemma,self.key))
        except:
            try:
                result = func(test_lemma)
                return func
            except:
                return None

    def _word_text(self, lemma: Lemma, key: str) -> str:
        if key.strip() == '' or key is None:
            return lemma.original
        elif key.strip().lower() in ('for_match','for match'):
            return lemma.for_match
        else:
            if key.strip() in lemma.dict_content:
                return lemma.dict_content[key]
            else:
                return lemma.original

    def default_func(self, lemma: Lemma):
        text = self._word_text(lemma, self.key)
        output = self.format_string % text
        return output
    

    def set_format_string(self, format_string: str) -> None:
        # 设置格式化字符串，检查是否为现成的 HTML 代码
        if not (format_string.startswith('<') and format_string.endswith('>')):
            self.format_string = f"<span>{format_string}</span>"
        else:
            self.format_string = format_string

    def parse_spec_rules(self, spec_rules_str: str) -> None:
        # 解析特殊的 CSS 规则字符串
        try:
            self.spec_rules_list = []
            spec_rules = [rule_line.strip() for rule_line in spec_rules_str.split(';')]
            for rule_line in spec_rules:
                rule, prop, value = rule_line.split(':')
                rule = rule.strip().strip('"')
                prop = prop.strip().strip('"')
                if prop == 'font':
                    prop = 'font-family'
                value = value.strip().strip('"')
                self.spec_rules_list.append([rule, prop, value])
        except:
            self.spec_rules_list = {}

    def get_spec_rule(self):
        if self.spec_rules_list:
            spec_rule_string = '; '.join([': '.join(rule) for rule in self.spec_rules_list])
            return spec_rule_string
        else:
            return ''
    
    def apply_highlight(self, output: str, lemma: Lemma) -> str:
        # 应用突出显示样式
        if self.highlight:
            if lemma.isFocus:
                output = self.add_style(output, "font-weight", "bold")
            else:
                output = self.remove_style(output, "font-weight")
        return output

    def apply_rainbow(self, output: str, index: int) -> str:
        # 应用彩虹色显示
        colors = ["red", "green", "maroon", "blue", "turquoise", "purple"]
        if self.rainbow:
            color = colors[index % len(colors)]
            output = self.add_style(output, "color", color)
        return output

    def apply_new_word(self, output: str, lemma: Lemma) -> None:
        if self.new_word:
            if lemma.is_lang:
                if not lemma.in_dict:
                    output = self.remove_style(output, 'color')
                    output = self.add_style(output, 'background-color', 'red')
                    output = self.add_style(output, 'color', 'white')
        return output
    
    def apply_spec_rules(self, output: str, lemma: Lemma) -> str:
        # 应用特殊的效果，style是一个元组：(prop, value)
        if self.spec_rules_list:
            for rule, prop, style in self.spec_rules_list:
                if rule in lemma.properties.values():
                    output = self.add_style(output, prop, style)
                elif rule.lower() in lemma.for_match.lower():
                    output = self.add_style(output, prop, style)
        return output

    def add_style(self,output: str, prop: str, value: str) -> str:
        prop = prop.lower()
        value = value.lower()
        # 查找 style 属性的位置
        if 'style="' in output.lower():
            start = output.lower().find('style="') + len('style="')
            end = output.find('"', start)
            styles = output[start:end].lower().split(';')
            # 移除已有的相同属性
            styles = [style for style in styles if not style.startswith(prop)]
            styles.append(f"{prop}:{value}")
            new_style = ';'.join(styles)
            output = output[:start] + new_style + output[end:]
        else:
            # 添加 style 属性
            output = output.replace('<span', f'<span style="{prop}:{value};"')
        return output

    def remove_style(self,output: str, prop: str) -> str:
        if 'style="' in output.lower():
            start = output.lower().find('style="') + len('style="')
            end = output.find('"', start)
            styles = output[start:end].lower().split(';')
            # 移除已有的相同属性
            styles = [style for style in styles if not style.startswith(prop)]
            new_style = ';'.join(styles)
            if new_style:
                output = output[:start] + new_style + output[end:]
            else:
                # 移除 style 属性
                style_start = output.find('style="') - 1
                output = output[:style_start] + output[end + 1:]
        return output
        
    def set_func(self, func_name: str) -> None:
        # 更新当前使用的显示函数
        if func_name not in self.func_list:
            raise ValueError(f"Function {func_name} not found in func_list")
        self.current_func = self.func_list[func_name]

    def get_func_list(self) -> List[str]:
        # 获取函数列表
        return list(self.func_list.keys())

    
