import sys
import re
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
    print(frequencies)
    f.close()
    return frequencies

def word_cloud(filename_output,frequencies):
    wordcloud = WordCloud().generate_from_frequencies(frequencies)
    wordcloud.to_file(filename_output)


def main():
    filename_stop = 'Szekspir/{}'.format(sys.argv[1])
    filename_text = 'Szekspir/{}'.format(sys.argv[2])
    filename_output = 'Graphs/{}'.format(sys.argv[3])
    stop_words = read_stop_words(filename_stop)
    frequencies = read_text(stop_words,filename_text)
    word_cloud(filename_output,frequencies)


if __name__ == '__main__':
    main()