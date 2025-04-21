import os
import nltk
import inflect
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# 下载所需的资源
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('stopwords')

p = inflect.engine()

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def process_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    filtered_tokens = []
    
    for word, tag in pos_tags:
        wn_tag = get_wordnet_pos(tag)
        if wn_tag: 
            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if wn_tag == wordnet.NOUN:
                # 把复数转成单数
                try:
                    singular = p.singular_noun(word)
                    #print(singular, word)
                    if sigular == False:
                        lemma = word
                    else:
                        #print(word, singular)
                        lemma = singular

                except BaseException:
                    pass

            filtered_tokens.append(lemma.lower())
    
    # 去掉标点符号和停用词
    filtered_tokens = [word for word in filtered_tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in filtered_tokens if word not in stop_words]
    
    return filtered_tokens

def count_words_in_directory(directory):
    word_count = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'content':
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    words = process_text(text)
                    for word in words:
                        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def main():
    directory = 'web_data'  # 请替换成你的数据目录
    word_count = count_words_in_directory(directory)
    word_num = len(word_count)
    print(word_num)
    for word, count in word_count.items():
        if 20 / 100000 <= count / float(word_num): #<= 1000 / 100000:
            print(f"{word} {count}")

if __name__ == "__main__":
    main()

