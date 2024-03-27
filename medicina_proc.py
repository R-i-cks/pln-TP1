import re
import json

doc_text_path ="medicina.xml"


doc_t = open(doc_text_path,'r', encoding="utf-8")

doc = doc_t.read()

doc = re.sub(r'<page number="544"[\w\W]+',"",doc) # retirar paginas sem interesse


doc = re.sub(r"<text\stop.*?>",r"<text>",doc) # limpar dados
doc = re.sub(r"<text>\s*</text>\n",r"", doc)


doc = re.sub(r"<text><b>\s*(\d.*)</b></text>",r"@tb@ \1", doc) # marcar inicio de um titulo

doc = re.sub(r"<text>\s*(\d+)\s</text>\n<text><b>(.*)</b></text>",r"@tb@ \1 \2",doc)
# Esta regex captura todos os elementos que não foram captados na anterior, por estarem em 2 linhas e coloca no mesmo formato

doc = re.sub(r"<text>\s*(es)+\s*</text>","@es@",doc)  # marcar traducoes em espanhol
doc = re.sub(r"<text>\s*(pt)+\s*</text>","@pt@",doc)  # marcar traducoes em português
doc = re.sub(r"<text>\s*(en)+\s*</text>","@en@",doc)  # marcar traducoes em inglês
doc = re.sub(r"<text>\s*(la)+\s*</text>","@la@",doc)  # marcar traducoes em galego

doc = re.sub(r"<text><i>([-\w\s\[\]\.]+)</i></text>",r"\1",doc) #extrair o conteudo de dentro das tags
doc = re.sub(r"<text>\s*;\s*</text>",r";",doc) # retirar lixo nas linhas de ;

doc = re.sub(r"<text><b>\s*</b></text>\n","",doc) # retirar tags vazias
doc = re.sub(r"([\.\[\]\w]+)\n;\n",r"\1;\n",doc) # retirar linhas em branco entre palavras e ;
doc = re.sub(r"</page>\n","",doc) # retirar fim de pagina
doc = re.sub(r"<fontspec.*\n","",doc) # retirar fontspec de fim de pagina

siglas = re.findall(r'<page number="16"[\w\W]+?<text>20</text>\n',doc)
doc = re.sub(r'<page number="16"[\w\W]+?<text>20</text>\n',"",doc)

doc = re.sub(r'<page number[\w\W]+?<text>\d+</text>\n',"",doc) # retirar inicio de pagina

doc = re.sub(r"\s+([fma])\n\s*(\w)",r' #\1#\n\2',doc) # retirar espaços e marcar genero
doc = re.sub(r'\s+([fma])\s*pl\n\s*([\w])',r' #\1 pl#\n\2',doc) # caso especial em que aparecia genero e pl (plural)
doc = re.sub(r"\s\n\s+",r" ", doc) # remoção de um erro de espaçamento
doc = re.sub(r'<text>\s*(SIN[\w\W]+?)</text>',r'#\1',doc) # marcação de sinónimos
doc = re.sub(r'<text>\s*(Vid.+)</text>',r'#\1',doc) # etiquetar VID.
doc = re.sub(r'(#Vid.-\s\w+\s)\n<text>(.+)</text>',r'\1\2',doc) # lidar com situações que ficou em 2 linhas
doc = re.sub(r'(b@.+)\n<text><i><b>(.+)</b></i></text>\n.+<b>(.+)</b>.+\n',r'\1\2\3',doc)  # correção para titulos multilinha

#doc = re.sub(r'<text><b>(.+)</b></text>',r'#SUBT \1',doc)

conceitos = re.findall(r"b@[\w\W]+?@t", doc)


# #\n.+?\n

"""
dicionario = {}
idiomas = ["@en@","@pt@","@es@","@la@"]
for elem in conceitos:
    conceito = {}
    num, des = re.findall(r'b@\s*(\d+)\s*([\w\W]+)?#',elem)
    for idioma in idiomas:
        if idioma in elem:

    dicionario[chave[0]] = elem

"""
# <text><b>[\w\W]+?</b></text>\n<text>[\w\W]+?</text>\n
#rest_conceitos = re.findall(r"<text>\s*(\d+)\s</text>\n(.*)",doc)
file_out = open("medicaProc.txt","w")
file_out.write(doc)
#file_out = open("dados.json","w")
#json.dump(dicionario,file_out)
file_out.close()

"""
lista=[]
for elem in conceitos:
    num = elem.split()
    num = num[0]
    lista.append(num)

lista_nova=[]
for i in range(1,5394):
    if i not in dicionario:
        lista_nova.append(i)

print(lista_nova)"""