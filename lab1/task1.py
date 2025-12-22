def count_words(text):
    words = text.lower().split()
    result = {}

    for word in words:
        result[word] = result.get(word, 0) + 1

    return result


text = input("Введіть текст: ")

stats = count_words(text)
print("Словник слів:", stats)

frequent_words = [word for word, count in stats.items() if count > 3]
print("Слова, що зустрічаються більше 3 разів:", frequent_words)
