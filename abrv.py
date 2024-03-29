import re
import json

doc_text_path ="abreviaturas.xml"


doc_t = open(doc_text_path,'r', encoding="utf-8")

doc = doc_t.read()

doc = re.sub(r"<text\stop.*?>",r"<text>",doc) # limpar dados
doc = re.sub(r'.+page.+\n?',"",doc)
doc = re.sub(r'.+\n.+</b></text>\n',"",doc)

file_out = open("abrev.txt","w")
file_out.write(doc)
file_out.close()