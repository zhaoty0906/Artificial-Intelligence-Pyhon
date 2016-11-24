# This reads in a file of parse rules, builds up the knowledge base and then uses them to 
# parse questions into patterns that can be used to "Ask" questions.

# We need a structure for Rules.  They need a name, a pattern and a query output. A rule can
# be defined just by its name

class Rule:

    def __init__(self, name, pattern = [], action = False, value = False):
        self.name = name
        self.pattern = pattern
        self.action = action
        self.value = value
        
    def show(self):
        if debug_print: print "\n" + self.name + ":",
        if debug_print: print self.pattern

class Disjunct: 

    def __init__(self, elements):
        self.elements = elements
            
# A few of globals, including one that allows us random access to rules by name.

global ParseRB
ParseRB = []
global indexed_ParseRB
index_ParseRB = {}

# Turning debugging messages on and off

global debug_print
debug_print = False


# Reading in a file of rule definitions, building the rule and replacing in any internal
# patterns with new rules.

# readParseRules reads in a set of rule definitions, tokenizes everything and then hands the 
# configuration elements (name, pattern, action, and arguments) to the parse rule builder

def readParserDefinitions(file):
    file_handle = open(file, "r")
    line = file_handle.readline()
    while line != "":
        definition = {}
        while ":" in line:
            label, value = line.split(":")
            if debug_print: print label
            definition[label] = value.rstrip("\n").strip(" ")
            line = file_handle.readline()
        if definition.get("Name", False):
            buildParseRule(definition["Name"], definition["Pattern"], 
                                               definition.get("Type", "Phrase"), 
                                               definition.get("Action", False), 
                                               definition.get("Value", False)) 
        line = file_handle.readline()
    file_handle.close()


# buildParseRule constructs a new parse rule and adds it to the rule base. If there is a 
# a pattern embedded in the top level pattern, it replaces the reference to the pattern with 
# the actual parse rule.  If there is a reference to a rule that has not been built yet, it
# builds an empty version of the rule so that when it is defined it will already be embedded in
# the elements that reference it.

# It also checks to see if an earlier rule built a stub of it.  If so, the pattern is added to
# the existing stub. If not, it builds the new rule from scratch.

def buildParseRule(name, pattern, type, action, value):
    if debug_print: print "\nBuilding new rule: " + name
    if debug_print: print "Pattern :",
    if debug_print: print pattern    
    pattern = map(lambda x: buildOrFindRuleFromName(x), pattern.split(" ")) 
    if index_ParseRB.get(name, False):
        if debug_print: print "Found stubbed out rule: " + index_ParseRB[name].name
        if debug_print: print index_ParseRB[name]
        if debug_print: print "Adding pattern:",
        if debug_print: print pattern
        index_ParseRB[name].pattern = pattern
        index_ParseRB[name].action = action
        index_ParseRB[name].value = value
    else:
        new_rule = Rule(name,pattern,action,value)
        if type == "Sentence":
            ParseRB.append(new_rule)
        index_ParseRB[name] = new_rule
        if debug_print: print "Adding pattern:",
        if debug_print: print pattern

 
 # buildOrFindRuleFromName tests to see if an element is a reference (i.e., it is in brackets)
 # and if it is, it checks to see if the rule referenced already exists. If it does, it returns
 # it.  If it is a reference to a rule that does not exist yet, it builds out a stub for it.
 # Otherwise, it just returns the element directly.

def buildOrFindRuleFromName(element):
    if "|" in element:
        return Disjunct(map(lambda x: buildOrFindRuleFromName(x), element.split("|")))
    if element[0] != "<":
        return element
    elif index_ParseRB.get(element[1:-1], False):
        return index_ParseRB[element[1:-1]]
    else:
        if debug_print: print "Stubbing out rule: " + element[1:-1].capitalize()
        new_rule = Rule(element[1:-1])
        index_ParseRB[element[1:-1]] = new_rule
        return new_rule


# parse takes a question and returns the representation of the statement that results with
# a set of bindings
        
def parse(sentence):

    global augments
    global parseBindings
    
    print "Parsing: " + " ".join(sentence) 
    for rule in ParseRB:
        parseBindings = {}
        augments = []
        statements = []
        if checkPattern(sentence, [[rule], rule.pattern]):
            if len(augments) != 0:
                statements = map(lambda x: buildRepresentation(x, parseBindings), augments)
            final = [buildRepresentation(rule.value, parseBindings)] + statements
            print "Parse Suceeded:" 
            print "\tRule: " + rule.name
            print "\tAction: " + rule.action
            print "\tStatements:", 
            print final 
            return rule.action, final
    print "Parse Failed:" 
    return False


# Check pattern takes a question (or other sentence) and a pattern and checks to see if
# there is a match between the two.  It iterates through the two lists until one or the other
# is exhausted.  If both are done, there is a match.  If one one is done, there is not.

# If an elements fail to match, then there is a failure as well.

# Before testing, checkPattern calls expandPattern to expands the first element of the 
# pattern to see if it is a rule, a disjunct of possibilities or just a string. No matter 
# expandPattern will return a list of patterns that will then be iterated through.
 
def checkPattern(sentence, rp):

    global output
    global parseBindings
    
    rules = rp[0]
    pattern = rp[1]
    
    if len(sentence) == 0 or len(pattern) == 0:
        if len(sentence) == 0 and len(pattern) == 0:
            return True
        else:
            return False
            
    if debug_print: print "\nTrying: " + " ".join(sentence) 
    if debug_print: print "Against: ",
    if debug_print: print pattern 
    expands = expandPattern(pattern)

    for possible in expands:
        rules = possible[0]
        pattern = possible[1]
        if debug_print: print "\tMatching: " + sentence[0] + "/"+ pattern[0],
        if sentence[0] == pattern[0] or sentence[0] == pattern[0]+"s" or pattern[0] == "*":
            if debug_print: print "...matched"
            result = checkPattern(sentence[1:], [rules, pattern[1:]])
            if result:
                for r in rules:
                    bindParseValues(r, sentence, pattern)
            return result
        else:
            if debug_print: print "...no match"
    return False

  
# Expand pattern expands the leading edge of a pattern (the first element) and always returns
# a list of possibilities.  This means that the first element of an expanded pattern is always
# a literal that can be matched against a literal in the the question.
   
def expandPattern(pattern):
    if debug_print: print "\nExpanding:",
    if debug_print: print pattern
    if isinstance(pattern[0], Rule):
        rule = pattern[0]
        if debug_print: print "\nFirst element is a rule"
        if debug_print: print "Rule =",
        if debug_print: print rule.name
        if debug_print: print "Rule pattern=",
        if debug_print: print rule.pattern
        if len(pattern) > 1:
            new_pattern = rule.pattern + pattern[1:]
            expansions = [[[rule], new_pattern]]
        else:
             expansions = [[[rule], rule.pattern]]            
    elif isinstance(pattern[0], Disjunct):
        if debug_print: print "\nFirst element is a disjunct:",
        if debug_print: print pattern[0].elements
        if len(pattern) > 1:
            expansions = map(lambda x: [[], [x] + pattern[1:]], pattern[0].elements)
        else:
            expansions = map(lambda x: [[], [x]], pattern[0].elements)
    else:  
        if debug_print: print "\nFirst element is a literal:"
        return [[ [], pattern] ]
    final_list = []
    for pattern in expansions:
        if len(pattern[1]) != 0:
            full_list = expandPattern(pattern[1])
            for x in full_list:
                x[0] = x[0] + pattern[0]
            final_list = full_list + final_list
    return final_list
   
   
def bindParseValues(rule, sentence, pattern):
    
    global parseBindings
    global augments
    
    if rule.action == "AddBindings":
        bindings = rule.value.split(",")
        for b in bindings:
            slot, filler = b.strip().rstrip().split(" ")
            if filler == "self":
                if pattern[0] == "*":
                    parseBindings[slot.strip().rstrip()] = sentence[0]
                else:
                    parseBindings[slot.strip().rstrip()] = pattern[0]
            else:
                parseBindings[slot.strip().rstrip()] = filler.strip().rstrip()
     
    if rule.action == "Augment":
        parseBindings["<"+rule.name+">"] =  "?"+rule.name+"Variable"
        for statement in rule.value.split(","):
            augments.append(statement)
            if debug_print: print statement

       
                
                    
def buildRepresentation(pattern, bindings):
    fopc = map(lambda x: x.strip().rstrip(), pattern[1:-1].split(" "))
    return map(lambda x: bindings.get(x, x), fopc)        
