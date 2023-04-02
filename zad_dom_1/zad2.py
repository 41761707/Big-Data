import sys
import re
import math
from wordcloud import WordCloud

def read_stop_words(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        return lines

def read_text(stop_words,filename):
    frequencies = {}
    f = open(filename)
    for word in f.read().split():
        if(len(word)) < 3:
             continue
        word = word.lower()
        word = re.sub(r'[^a-z0-9]+', '', word)
        if word not in stop_words:  
            if word not in frequencies:
                    frequencies[word] = 1
            else:
                    frequencies[word] = frequencies[word] + 1
    frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1],reverse=True))
    #print(frequencies)
    f.close()
    return frequencies

def word_cloud(filename_output,frequencies):
    wordcloud = WordCloud().generate_from_frequencies(frequencies)
    wordcloud.to_file(filename_output)


def main():
    filename_stop = 'Szekspir/{}'.format(sys.argv[1])
    filename_output = 'Graphs/{}'.format(sys.argv[2])
    file_number = int(sys.argv[3])
    frequencies_array = []
    stop_words = read_stop_words(filename_stop)
    for filename in ['Szekspir/hamlet.txt','Szekspir/KingLear.txt','Szekspir/Othello.txt','Szekspir/RomeoJuliet.txt']:
        frequencies_array.append(read_text(stop_words,filename))
    final_dict = {}
    sum_terms = sum(frequencies_array[file_number].values())
    for k,v in frequencies_array[file_number].items():
        if k not in final_dict:
            tf = v / sum_terms
            doc_counter = 0
            for check in frequencies_array:
                if k in check:
                    doc_counter = doc_counter+1
            idf = math.log2(len(frequencies_array)/doc_counter)
            final_dict[k] = tf * idf
    final_dict = dict(sorted(final_dict.items(), key=lambda item: item[1],reverse=True))
    word_cloud(filename_output,final_dict)



if __name__ == '__main__':
    main()