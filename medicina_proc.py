import re


doc_text_path ="medicina.xml"

doc_t = open(doc_text_path,'r', encoding="utf-8")

doc = doc_t.read()



doc = re.sub(r"<text\stop.*?>",r"<text>",doc) # limpar dados
doc = re.sub(r"<text>\s*</text>\n",r"", doc)


doc = re.sub(r"<text><b>\s*(\d.*)</b></text>",r"@tb@ \1 @e", doc) # marcar inicio e fim de um titulo

doc = re.sub(r"<text>\s*(\d+)\s</text>\n<text><b>(.*)</b></text>",r"@tb@ \1 \2 @e",doc)
# Esta regex captura todos os elementos que não foram captados na anterior, por estarem em 2 linhas e coloca no mesmo formato

doc = re.sub(r"<text>\s*(es)+\s*</text>","@es@",doc)  # marcar traducoes em espanhol
doc = re.sub(r"<text>\s*(pt)+\s*</text>","@pt@",doc)  # marcar traducoes em português
doc = re.sub(r"<text>\s*(en)+\s*</text>","@en@",doc)  # marcar traducoes em inglês
doc = re.sub(r"<text>\s*(la)+\s*</text>","@la@",doc)  # marcar traducoes em galego

doc = re.sub(r"<text><i>([-\w\s\[\]\.]+)</i></text>",r"\1",doc) #extrair o conteudo de dentro das tags
doc = re.sub(r"<text>\s*;\s*</text>",r";",doc) # retirar lixo nas linhas de ;

doc = re.sub(r"<text><b>\s*</b></text>\n","",doc) # retirar tags vazias
conceitos = re.findall(r"b@[\w\W]+?@t", doc)

#rest_conceitos = re.findall(r"<text>\s*(\d+)\s</text>\n(.*)",doc)
#print(conceitos)
file_out = open("medicaProc.txt","w")
file_out.write(doc)
file_out.close()

"""
lista=[]
for elem in conceitos:
    num = elem.split()
    num = num[0]
    lista.append(num)

lista_nova=[]
for i in range(1,5394):
    if str(i) not in lista:
        lista_nova.append(i)
"""
#print(lista_nova)