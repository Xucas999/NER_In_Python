import spacy
import json
import random

from spacy.training import Example


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def save_data(file,data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def train_spacy(data,iterations):
    TRAIN_DATA = data
    nlp = spacy.blank("en")
    if "ner" not in nlp.pipe_names:
        nlp.add_pipe("ner",last=True)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            nlp.get_pipe("ner").add_label(ent[2])
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting Iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc,annotations)
                nlp.update(
                    [example],
                    drop=0.2,
                    sgd=optimizer,
                    losses=losses
                )
            print(losses)
    return (nlp)

#TRAIN_DATA = load_data("hp_training_data.json")
#nlp = train_spacy(TRAIN_DATA, 30)
#nlp.to_disk("hp_ner_model")

test = "The series follows the life of a boy named Harry James Potter. In the first book, Harry Potter and the Philosopher's Stone, Harry lives in a cupboard under the stairs in the house of the Dursleys, his aunt, uncle and cousin, who all treat him poorly. At the age of 11, Harry discovers that he is a wizard. He meets a half-giant named Hagrid who gives him a letter of acceptance to attend the Hogwarts School of Witchcraft and Wizardry. Harry learns that his parents, Lily and James Potter, also had magical powers, and were murdered by the dark wizard Lord Voldemort when Harry was a baby. When Voldemort attempted to kill Harry, his curse rebounded, seemingly killing Voldemort, and Harry survived with a lightning-shaped scar on his forehead. The event made Harry famous among the community of wizards and witches. Harry becomes a student at Hogwarts and is sorted into Gryffindor House. He gains the friendship of Ron Weasley, a member of a large but poor wizarding family, and Hermione Granger, a witch of non-magical, or Muggle, parentage. The trio develop an enmity with the rich pure-blood student Draco Malfoy. Harry encounters the school's headmaster, Albus Dumbledore; the potions professor, Severus Snape, who displays a dislike for him; and the Defence Against the Dark Arts teacher, Quirinus Quirrell. Quirrell turns out to be allied with Voldemort, who is still alive as a weak spirit. The first book concludes with Harry's confrontation with Voldemort, who, in his quest to regain a body, yearns to possess the Philosopher's Stone, a substance that bestows everlasting life. Harry Potter and the Chamber of Secrets describes Harry's second year at Hogwarts. Students are attacked and petrified by an unknown creature; wizards of Muggle parentage are the primary targets. The attacks appear related to the mythical Chamber of Secrets and resemble attacks fifty years earlier. Harry discovers an ability to speak the snake language Parseltongue, which he learns is rare and associated with the Dark Arts. When Hermione is attacked and Ron's younger sister, Ginny Weasley, abducted, Harry and Ron uncover the chamber's secrets and enter it. Harry discovers that Ginny was possessed by an old diary, inside which the memory of Tom Marvolo Riddle, Voldemort's younger self, resides. On Voldemort's behalf, Ginny opened the chamber and unleashed the basilisk, an ancient monster that kills or petrifies those who make direct or indirect eye contact, respectively. With the help of Dumbledore's phoenix, Fawkes, and the Sword of Gryffindor, Harry slays the basilisk and destroys the diary. In the third novel, Harry Potter and the Prisoner of Azkaban, Harry learns that he is targeted by Sirius Black, an escaped convict who allegedly assisted in his parents' murder. Dementors, creatures that feed on despair, search for Sirius and guards the school. As Harry struggles with his reaction to the dementors, he reaches out to Remus Lupin, a new professor who teaches him the Patronus charm. On a windy night, Ron is dragged by a black dog into the Shrieking Shack, a haunted house, and Harry and Hermione follow. The dog is revealed to be Sirius Black. Lupin enters the shack and explains that Sirius was James Potter's best friend; he was framed by another friend of James, Peter Pettigrew, who hides as Ron's pet rat, Scabbers. As the full moon rises, Lupin transforms into a werewolf and bounds away, and the group chase after him. They are surrounded by dementors, but are saved by a figure resembling James who casts a stag Patronus. This is later revealed to be a future version of Harry, who traveled back in time with Hermione using a device called a Time Turner. The duo help Sirius escape on a Hippogriff, while Pettigrew escapes."

import re

def clean_text(text):
    cleaned = re.sub(r"[\(\[].*?[\)\]]", "", text)
    return cleaned

test = clean_text(test)

nlp = spacy.load("hp_ner_model")
doc = nlp(test)
for ent in doc.ents:
    print(ent.text,ent.label_)