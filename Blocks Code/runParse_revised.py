import Parse_Revised

Parse_Revised.readParserDefinitions("sampleRules.dat")

global sentences
sentences = []

Parse_Revised.debug_print = False

def gather(sentence_string):
    global sentences
    sentences.append(sentence_string.rstrip().split(" "))
    
handle = open("sentences.txt", 'r')
for sentence in handle:
    gather(sentence)
handle.close()

for sentence in sentences:
    print
    Parse_Revised.parse(sentence)