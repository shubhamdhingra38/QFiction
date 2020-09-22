from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import sys

tokenizer = AutoTokenizer.from_pretrained(
    "mrm8488/bert-medium-finetuned-squadv2")
model = AutoModelForQuestionAnswering.from_pretrained(
    "mrm8488/bert-medium-finetuned-squadv2")

# tokenizer = AutoTokenizer.from_pretrained(
#     "/Users/shubham/Documents/QFiction/Q_Fiction/trained"
# )
# model = AutoModelForQuestionAnswering.from_pretrained(
#     "../trained"
# )


def answer_question(question, answer_text, DEBUG=False):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.


    Maximum length after tokenization can only be 512 so this strips off anything greater than that.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.

    ref_len = len(answer_text.split(' '))
    if DEBUG:
        print('Before tokenization, length of input text (reference) is {}'.format(ref_len))

        print(answer_text)

        print(len(answer_text))

    input_ids = tokenizer.encode(question, answer_text)

    if DEBUG:

        print('After tokenization, length is {}'.format(len(input_ids)))

    # ======== Cut off larger paragraphs limited till 512 in length ========
    max_ref_len = min(512, len(input_ids))
    input_ids = input_ids[:max_ref_len]

    # Report how long the input sequence is.
    if DEBUG:
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
    # Find the index of tokens with the highest `start` and `end` scores.
    max_start_score = torch.max(start_scores).item()
    max_end_score = torch.max(end_scores).item()




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
    
    total_score = max_end_score + max_start_score

    return (answer, total_score)



if __name__ == '__main__':
    abstract = '''
    Gandalf is a protagonist in J. R. R. Tolkien's novels The Hobbit and The Lord of the Rings. He is a wizard, one of the Istari order, and the leader and mentor of the Fellowship of the Ring. Tolkien took the name "Gandalf" from the Old Norse "Catalogue of Dwarves" (Dvergatal) in the Völuspá.

As a wizard and the bearer of a Ring of Power, Gandalf has great power, but works mostly by encouraging and persuading. He sets out as Gandalf the Grey, possessing great knowledge, and travelling continually, always focused on the mission to counter the Dark Lord Sauron. He is associated with fire, his ring being Narya, the Ring of Fire, and he both delights in fireworks to entertain the hobbits of the Shire, and in great need uses fire as a weapon. As one of the Maiar he is an immortal spirit, but being in a physical body on Middle-earth, he can be killed in battle, as he is by the Balrog from Moria. He is sent back to Middle-earth to complete his mission, now as Gandalf the White and leader of the Istari.

Tolkien once described Gandalf as an angel incarnate; later, both he and other scholars have likened Gandalf to the Norse god Odin in his "Wanderer" guise. Others have described Gandalf as a guide-figure who assists the protagonist, comparable to the Cumaean Sibyl who assisted Aeneas in Virgil's The Aeneid, or to Virgil himself in Dante's Inferno; and as a Christ-figure, a prophet. 
    '''
    question = 'Who is Gandalf?'
    print(answer_question(question, abstract))