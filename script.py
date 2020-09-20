from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch


tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/bert-medium-finetuned-squadv2")
model = AutoModelForQuestionAnswering.from_pretrained(
    "mrm8488/bert-medium-finetuned-squadv2")


def answer_question(question, answer_text):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.


    Maximum length after tokenization can only be 512 so this strips off anything greater than that.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.

    ref_len = len(answer_text.split(' '))
    print('Before tokenization, length of input text (reference) is {}'.format(ref_len))

    print(answer_text)

    print(len(answer_text))

    input_ids = tokenizer.encode(question, answer_text)

    print('After tokenization, length is {}'.format(len(input_ids)))

    # ======== Cut off larger paragraphs limited till 512 in length ========
    max_ref_len = min(512, len(input_ids))
    input_ids = input_ids[:max_ref_len]

    # Report how long the input sequence is.
    print('Query has {:,} tokens.\n'.format(len(input_ids)))

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    # ======== Evaluate ========
    # Run our example question through the model.
    start_scores, end_scores = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                                     token_type_ids=torch.tensor([segment_ids]))  # The segment IDs to differentiate question from answer_text

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):

        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]

        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]

    return answer


abstract = '''
Gandalf is a protagonist in J. R. R. Tolkien's novels The Hobbit and The Lord of the Rings. He is a wizard, one of the Istari order, and the leader and mentor of the Fellowship of the Ring. Tolkien took the name "Gandalf" from the Old Norse "Catalogue of Dwarves" (Dvergatal) in the Völuspá.
As a wizard and the bearer of a Ring of Power, Gandalf has great power, but works mostly by encouraging and persuading. He sets out as Gandalf the Grey, possessing great knowledge, and travelling continually, always focused on the mission to counter the Dark Lord Sauron. He is associated with fire, his ring being Narya, the Ring of Fire, and he both delights in fireworks to entertain the hobbits of the Shire, and in great need uses fire as a weapon. As one of the Maiar he is an immortal spirit, but being in a physical body on Middle-earth, he can be killed in battle, as he is by the Balrog from Moria. He is sent back to Middle-earth to complete his mission, now as Gandalf the White and leader of the Istari.
s explained in The Fellowship of the Ring, Gandalf spends the years between The Hobbit and The Lord of the Rings traveling Middle-earth in search of information on Sauron's resurgence and Bilbo Baggins's mysterious ring, spurred particularly by Bilbo's initial misleading story of how he had obtained it as a "present" from Gollum. During this period, he befriends Aragorn and first becomes suspicious of Saruman. He spends as much time as he can in the Shire, strengthening his friendship with Bilbo and Frodo, Bilbo's orphaned cousin and adopted heir.[T 11]

Gandalf returns to the Shire for Bilbo's "eleventy-first" (111th) birthday party, bringing many fireworks for the occasion. After Bilbo, as a prank on his guests, puts on the Ring and disappears, Gandalf strongly encourages his old friend to leave the ring to Frodo, as they had planned. Bilbo becomes hostile and accuses Gandalf of trying to steal the ring. Alarmed, Gandalf impresses on Bilbo the foolishness of this accusation. Coming to his senses, Bilbo admits that the ring has been troubling him, and leaves it behind for Frodo as he departs for Rivendell.[T 12]

Over the next 17 years, Gandalf travels extensively, searching for answers on the ring. He finds some answers in Isildur's scroll, in the archives of Minas Tirith. He also wants to question Gollum, who had borne the ring for many years. Gandalf searches long and hard for Gollum, and often has the assistance of Aragorn. Aragorn eventually succeeds in finding Gollum. Gandalf questions Gollum, threatening him with fire when he proves unwilling to speak. Gandalf learns that Sauron has forced Gollum under torture in Barad-dûr to tell what he knows of the ring. This reinforces Gandalf's growing suspicion that Bilbo's ring is the One Ring.[T 11]

Returning to the Shire, Gandalf confirms his suspicions by throwing the Ring into Frodo's hearth-fire and reading the writing that appears on the Ring's surface. He tells Frodo the history of the Ring, and urges him to take it to Rivendell, for he will be in grave danger if he stays in the Shire. Gandalf says he will attempt to return for Frodo's 50th birthday party, to accompany him on the road; and that meanwhile Frodo should arrange to leave quietly, as the servants of Sauron will be searching for him.[T 13]

Outside the Shire, Gandalf encounters Radagast the Brown, another wizard, who brings the news that the Nazgûl have ridden forth out of Mordor—and a request from Saruman that Gandalf come to Isengard. Gandalf leaves a letter to Frodo (urging his immediate departure) with Barliman Butterbur at an inn in Bree, and heads towards Isengard. There Saruman reveals his true intentions, urging Gandalf to help him obtain the Ring for his own use. Gandalf refuses, and Saruman imprisons him at the top of his tower. Eventually Gandalf is rescued by Gwaihir the Eagle.[T 11]

Gwaihir sets Gandalf down in Rohan, where Gandalf appeals to King Théoden for a horse. Théoden, under the evil influence of Gríma Wormtongue, Saruman's spy and servant, tells Gandalf to take any horse he pleases, but to leave quickly. It is then that Gandalf meets the great horse Shadowfax, one of the mearas, who will be his mount and companion for much of the Lord of the Rings. Gandalf then rides hard for the Shire, but does not reach it until Frodo has already set out. Knowing that Frodo and his companions will be heading for Rivendell, Gandalf makes his own way there. He learns at Bree that the Hobbits have fallen in with Aragorn. He faces the Nazgûl at Weathertop but escapes after an all-night battle, drawing four of them northward.[T 11] Frodo, Aragorn and company face the remaining five on Weathertop a few nights later.[T 14] Gandalf reaches Rivendell just before Frodo's arrival.[T 11]

In Rivendell, Gandalf helps Elrond drive off the Nazgûl pursuing Frodo and plays a great part in the following council as the only person who knows the full history of the Ring. He also reveals that Saruman has betrayed them and is in league with Sauron. When it is decided that the Ring has to be destroyed, Gandalf volunteers to accompany Frodo—now the Ring-bearer—in his quest. He also persuades Elrond to let Frodo's cousins Merry and Pippin join the Fellowship.[T 11]
The Balrog reached the bridge. Gandalf stood in the middle of the span, leaning on the staff in his left hand, but in his other hand Glamdring gleamed, cold and white. His enemy halted again, facing him, and the shadow about it reached out like two vast wings. It raised the whip, and the thongs whined and cracked. Fire came from its nostrils. But Gandalf stood firm. "You cannot pass," he said. The orcs stood still, and a dead silence fell. "I am a servant of the Secret Fire, wielder of the flame of Anor. You cannot pass. The dark fire will not avail you, flame of Udûn. Go back to the Shadow! You cannot pass."

J. R. R. Tolkien, The Fellowship of the Ring

Taking charge of the Fellowship (comprising nine representatives of the free peoples of Middle-earth, "set against the Nine Riders"), Gandalf and Aragorn lead the Hobbits and their companions south.[T 15] After an unsuccessful attempt to cross Mount Caradhras in winter due to harsh conditions, they cross under the mountains through the Mines of Moria, though only Gimli the Dwarf is enthusiastic about that route. In Moria, they discover that the dwarf colony established there earlier by Balin has been annihilated by orcs. The Fellowship fights with the orcs and trolls of Moria and escape them.[T 16]

At the Bridge of Khazad-dûm, they encounter "Durin's Bane", a fearsome Balrog from ancient times. Gandalf faces the Balrog to enable the others to escape. After a brief exchange of blows, Gandalf breaks the bridge beneath the Balrog with his staff. As the Balrog falls, it wraps its whip around Gandalf's legs, dragging him over the edge. Gandalf falls into the abyss, crying "Fly, you fools!".[T 17]

Gandalf and the Balrog fall into a deep subterranean lake in Moria's underworld. Gandalf pursues the Balrog through the tunnels for eight days until they climb to the peak of Zirakzigil. Here they fight for two days and nights. In the end, the Balrog is defeated and cast down onto the mountainside. Gandalf too dies shortly afterwards, and his body lies on the peak while his spirit travels "out of thought and time".'''
answer = answer_question('Who is Gandalf?', abstract)
print(answer)
