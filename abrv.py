import re
import json

doc_text_path ="abreviaturas.xml"


doc_t = open(doc_text_path,'r', encoding="utf-8")

doc = doc_t.read()

doc = re.sub(r"<text\stop.*?>",r"<text>",doc) # limpar dados
doc = re.sub(r'.+page.+\n?',"",doc)
doc = re.sub(r'.+\n.+</b></text>\n',"",doc)

lista_abr_sig = re.findall(r'<text>(.+)</text>\n<text>(.+)</text>',doc)
dic = {elem[0].strip() : elem[1] for elem in lista_abr_sig}

file_out = open("abrev.json","w", encoding="utf-8")
json.dump(dic,file_out,  indent=4, ensure_ascii=False)
file_out.close()