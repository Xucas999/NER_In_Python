import json
with open ("HarryPotter.txt", "r", encoding="utf-8") as f:
    text = f.read().split("\n\n")

character_names = []
with open("characters.json", "r", encoding="utf-8") as f:
    characters = json.load(f)
    for character in characters:
        names = character.split()
        for name in names:
            if "and" != name and "the" != name and "The" != name:
                name = name.replace(",","").strip()
                character_names.append(name)


for segment in text:
    segment = segment.strip()
    segment = segment.replace("\n"," ")

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in segment:
        if ele in punc:
            segment = segment.replace(ele, "")
    words = segment.split()

    i = 0
    for word in words:
        if word in character_names:
            if words[i-1][0].isupper():
                print(f"Found Character(s): {words[i-1]} {word}")
            else:
                print(f"Found Character(s) {word}")
        i += 1
