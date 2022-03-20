# Ordanet_Extractor
## Description ##
This program extracts all synonyms from The Icelandic Wordweb and writes them to
a text file. If WORD1 and WORD2 are synonyms, their respective entries will be 

&nbsp;&nbsp;&nbsp;&nbsp; WORD1=WORD2(normal)

and

&nbsp;&nbsp;&nbsp;&nbsp; WORD2=WORD1(normal)

with "(normal)" being the weight assigned to their synonymy relation.
This formatting is at the request of the Consortium of Icelandic Libraries
(Landskerfi bókasafna), for whose systems it was originally created. 

Information on The Icelandic Wordweb, including the full download of its data,
may be found on the CLARIN-IS repository at http://hdl.handle.net/20.500.12537/69


## Documentation ##
In the Wordweb, synonym are a type of "sense relation" that link up the lexical senses of two Wordweb entries.

An entry's "lexical sense" is, this context, roughly equivalent to a specific definition of that particular entry.

All entries of any kind in the Wordweb are separated by single empty lines. To extract synonyms, we thus parse all
the Wordweb's entries, picking out the synonym-related ones and extracting from each of those the IDs of the two
lexical senses it refers to. For reference, a synonym entry will look something like this (note the tab indentations):

<rdf:Description rdf:about="http://orda.net/senseRelation_(3-815)">  
&nbsp;&nbsp;&nbsp;&nbsp;    <rdf:type rdf:resource="http://www.w3.org/ns/lemon/vartrans#SenseRelation"/>  
&nbsp;&nbsp;&nbsp;&nbsp;    <vartrans:source rdf:resource="http://orda.net/ontolexLexicalSense_(3)"/>  
&nbsp;&nbsp;&nbsp;&nbsp;    <vartrans:target rdf:resource="http://orda.net/ontolexLexicalSense_(815)"/>  
&nbsp;&nbsp;&nbsp;&nbsp;    <vartrans:category rdf:resource="http://www.lexinfo.net/ontology/2.0/lexinfo#synonym"/>  
</rdf:Description>

We then parse the Wordweb's entries again, searching for all those lexical senses and extracting from each its
proper written version (marked by an rdfs:label entry). Note that each sense will be associated with several
different types of entries. We search specifically for one with "_fsh_" in its opening line, since those entries
are guaranteed to be unique and singular for each lexical sense. ("FSH" is the Icelandic abbreviation for
an entry type known as LaC, or "Lemma-as-Concept", in English. For a detailed explanation of these types, see
the Wordweb Handbook, available from http://hdl.handle.net/20.500.12537/69 )

For reference, an FSH entry will look like this:

<rdf:Description rdf:about="http://orda.net/aftækur_fsh_(815)">  
&nbsp;&nbsp;&nbsp;&nbsp;    <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>  
&nbsp;&nbsp;&nbsp;&nbsp;    <skos:inScheme rdf:resource="http://orda.net/conceptScheme_fsh"/>  
&nbsp;&nbsp;&nbsp;&nbsp;    <rdfs:label xml:lang="is">aftækur</rdfs:label>  
&nbsp;&nbsp;&nbsp;&nbsp;    <ontolex:isReferenceOf rdf:resource="http://orda.net/ontolexLexicalSense_(815)"/>  
</rdf:Description>

