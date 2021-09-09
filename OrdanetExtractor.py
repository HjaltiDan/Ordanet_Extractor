import re

'''
### DESCRIPTION ###
This program extracts all synonyms from The Icelandic Wordweb and writes them to
a text file. If WORD1 and WORD2 are synonyms, their respective entries will be 
    WORD1=WORD2(normal)
and
    WORD2=WORD1(normal)
with "(normal)" being the weight assigned to their synonymy relation.

This formatting is at the request of the Consortium of Icelandic Libraries
(Landskerfi bókasafna), for whose systems it is intended. 

Information on The Icelandic Wordweb, including the full download of its data,
may be found on the CLARIN-IS repository at http://hdl.handle.net/20.500.12537/69

Author: Hjalti Daníelsson; 2021

### END DESCRIPTION ###

### DOCUMENTATION ###

In the Wordweb, synonym are a type of "sense relation" that link up the lexical senses of two Wordweb entries.
An entry's "lexical sense" is, this context, roughly equivalent to a specific definition of that particular entry.

All entries of any kind in the Wordweb are separated by single empty lines. To extract synonyms, we thus parse all
the Wordweb's entries, picking out the synonym-related ones and extracting from each of those the IDs of the two
lexical senses it refers to. For reference, a synonym entry will look something like this (note the tab indentations):

<rdf:Description rdf:about="http://orda.net/senseRelation_(3-815)">
    <rdf:type rdf:resource="http://www.w3.org/ns/lemon/vartrans#SenseRelation"/>
    <vartrans:source rdf:resource="http://orda.net/ontolexLexicalSense_(3)"/>
    <vartrans:target rdf:resource="http://orda.net/ontolexLexicalSense_(815)"/>
    <vartrans:category rdf:resource="http://www.lexinfo.net/ontology/2.0/lexinfo#synonym"/> 
</rdf:Description>

We then parse the Wordweb's entries again, searching for all those lexical senses and extracting from each its
proper written version (marked by an rdfs:label entry). Note that each sense will be associated with several
different types of entries. We search specifically for one with "_fsh_" in its opening line, since those entries
are guaranteed to be unique and singular for each lexical sense. ("FSH" is the Icelandic abbreviation for
an entry type known as LaC, or "Lemma-as-Concept", in English. For a detailed explanation of these types, see
the Wordweb Handbook, available from http://hdl.handle.net/20.500.12537/69 )

For reference, an FSH entry will look like this:

<rdf:Description rdf:about="http://orda.net/aftækur_fsh_(815)">
    <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>
    <skos:inScheme rdf:resource="http://orda.net/conceptScheme_fsh"/>
    <rdfs:label xml:lang="is">aftækur</rdfs:label>
    <ontolex:isReferenceOf rdf:resource="http://orda.net/ontolexLexicalSense_(815)"/>
</rdf:Description>

### END DOCUMENTATION ###
'''


def read_entries(filename):
    with open(filename, 'r', encoding='utf-8') as f_in:
        all_lines = f_in.read()
        all_lines = all_lines.replace('&#160;', ' ')
        all_lines = all_lines.replace('&#60;', '<')
        all_lines = all_lines.replace('&#62;', '>')
        all_lines = all_lines.replace('&#47;', '/')
        list_allentries = all_lines.split('\n\n')
    return list_allentries


def populate_word_dict(para_list):
    word_dict = {}
    for para in para_list:
        firstline = para.partition('\n')[0]
        if "_fsh_(" in firstline:
            try:
                wordno = re.search(r'_fsh_\((.+?)\)">', firstline).group(1)
                wordstr = re.search(r'<rdfs:label xml:lang=\"is\">(.+?)</rdfs:label>', para).group(1)
            except AttributeError:
                wordno = ''
                wordstr = ''
            if (wordno is not '') & (wordstr is not ''):
                word_dict[int(wordno)] = wordstr
    return word_dict


def extract_synonyms(para_list, word_dict):
    dict_syn = {}
    for para in para_list:
        para_clean = para.rstrip()
        if ("lexinfo#synonym" in para_clean) & (para_clean.endswith('rdf:Description>')):
            try:
                sense_1 = re.search(r'senseRelation_\((.+?)-', para_clean).group(1)
                sense_2 = re.search(r'-(.+?)\)\">', para_clean).group(1)
            except AttributeError:
                sense_1 = ''
                sense_2 = ''
            if (sense_1 is not '') & (sense_2 is not ''):
                word_1 = word_dict.get(int(sense_1))
                word_2 = word_dict.get(int(sense_2))
                if (word_1 is not None) & (word_2 is not None):
                    # Note: For a much simpler implementation, have word1 be the key and word2 the value, and vice versa:
                    # dict_synonyms[word1] = word2
                    # dict_synonyms[word2] = word1
                    # We're using tuples as keys so that we can include synonym weights as values while
                    # still ensuring that we avoid duplicate word pairs.
                    dict_syn[(word_1, word_2)] = "(normal)"
                    dict_syn[(word_2, word_1)] = "(normal)"
    return dict_syn


### MAIN STARTS ###

list_entries = read_entries('wordnet.rdf')

dict_words = populate_word_dict(list_entries)

dict_synonyms = extract_synonyms(list_entries, dict_words)

with open('synonyms.txt', 'w', encoding='utf-8') as f_out:
    for key, value in dict_synonyms.items():
        syn_str = str(key[0]) + "=" + str(key[1]) + str(value) + "\n"
        f_out.write(syn_str)

### MAIN ENDS ###
