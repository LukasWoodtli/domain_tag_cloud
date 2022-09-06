"""Create a word cloud with given words"""
from wordcloud import WordCloud
from matplotlib import pyplot as plt


def generate_word_cloud(output_file_name, words):
    """Save an image with a word cloud with the given words and frequencies."""
    word_cloud = WordCloud().fit_words(words)
    plt.figure()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(output_file_name)
