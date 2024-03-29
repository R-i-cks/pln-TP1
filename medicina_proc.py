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

doc = re.sub(r"\s+([fmas]|sg|sb)\n\s*(\w)",r' #\1#\n\2',doc) # retirar espaços e marcar genero + s(ingular) + sg + sb
doc = re.sub(r'\s+([fma])\s*pl\n\s*([\w])',r' #\1 pl#\n\2',doc) # caso especial em que aparecia genero e pl (plural)
doc = re.sub(r"\s\n\s+",r" ", doc) # remoção de um erro de espaçamento
doc = re.sub(r'<text>\s*(SIN[\w\W]+?)</text>\n',r'#\1\n',doc) # marcação de sinónimos
doc = re.sub(r'<text>\s*(Vid.+)</text>',r'#\1',doc) # etiquetar VID.
doc = re.sub(r'(#Vid.-\s\w+\s)\n<text>(.+)</text>',r'\1\2',doc) # lidar com situações que ficou em 2 linhas
doc = re.sub(r'(b@.+)\n<text><i><b>(.+)</b></i></text>\n.+<b>\s*(.+)</b>.+\n',r'\1\2 #\3#\n',doc)  # correção para titulos multilinha
doc = re.sub(r'<text><i><b>(.+)</b></i></text>\n#',r'#REL \1\n',doc) # marcação de termos que aparecem a negrito
doc = re.sub(r'<text><i>(.+)</i></text>\n;',r'\1;',doc) # retirar linhas de ; pós itálico
doc = re.sub(r'<text><i>(.+)</i></text>',r'\1',doc) # retirar itálico
doc = re.sub(r'(b@.+)\n.+<b>(.+)</b>.+\n.+<b>.*\s([mfa]).*</b>.+',r'\1\2#\3#',doc) # títulos de 3 linhas e colocar tag no genero
doc = re.sub(r'(b@.+)\n<text><b>(.+)\s([mfa])(\spl)</b></text>',r'\1\2 #\3\4#',doc) # caso especifico de 2 linhas titulo com gen e pl não marcado
doc = re.sub(r'(b@.+)\n<text><b>(.+)\s+([mfa])\s*</b></text>\n',r'\1\2#\3#\n',doc)  # tratar titulos com 2 linhas e colocar tag no genero
doc = re.sub(r'(b@.+)\n<text><b>(.+)\s+([mfa]?)\s*</b></text>\n',r'\1\2#\3#\n',doc) # escrever esta e a linha anterior não estava a funcionar como esperado

# Ao analisar elementos com bold reparou-se que havia um subtítulo com 4 linhas, e vários com 2 ou 1.
""""""
doc = re.sub(r'<text><b>(.+)</b></text>\n?<text><b>(.+)</b></text>\n?<text><b>(.+)</b></text>\n?<text><b>(.+)</b></text>\n?',r'#SUBT \1\2 \3\4\n',doc)  # não se usou {4} para conseguir aceder aos grupos de captura
doc = re.sub(r'<text><b>(.+)</b></text>\n?<text><b>(.+)</b></text>\n',r'#SUBT \1\2\n',doc)
doc = re.sub(r'<text><b>(.+)</b></text>\n',r'#SUBT \1\n',doc)

doc = re.sub(r'.+(VAR.+)</text>',r'#\1',doc) # marcação VAR

doc= re.sub(r'.+(Nota.+)</text>\n',r'#\1\n',doc) # marcação início Notas

doc = re.sub(r'<text>(.+)</text>',r'\1',doc) # retirar tags de texts que faltam



doc = re.sub(r"(#SUBT   CO)\n@tb@\s(2)",r"\1\2",doc) # caso específico em que CO2 quebra a regra de marcação @tb@
doc = re.sub(r'(@tb@.+)\n@tb@\s(.+)',r'\1\2',doc)  # erro de tag, duas seguidas referentes ao msm
doc = re.sub(r'(b@.+)##\n#SUBT\s([mf])\s+\n',r'\1 #\2#\n',doc) # correção de um erro introduzido
doc = re.sub(r'(b@.+#)#',r'\1Nap#',doc) # marcar os que n tem genero

doc += '@t' # introduzido para fechar o último termo

conceitos = re.findall(r"b@[\w\W]+?@t", doc)

sub_ini = "#SUBT A\n#Vid.- adenina"  # este subtermo está fora de todos os outros. 

file_out = open("medicaProc.txt","w")
file_out.write(doc)
file_out.close()

dicionario = {}

for elem in conceitos:
    tipos = re.search(r'b@.+#\n(.+)',elem).groups()
    linha = re.search(r'b@\s(\d+)\s(.+)\s#(.+)#',elem) # lista de 1 tuplo
    num, tit, gen = linha.groups()
    tit = tit.strip()
    tit = re.sub(r'\s+',' ', tit)
    if gen=="Nap":
        gen = ""
    dicionario[num] = {"Termo":tit, "Género": gen, "Classes": [tipo for tipo in re.split(r'\s{2,}',tipos[0])]}
    extras = ["#SIN","#Nota","REL"]
    for extra in extras:
        if extra in elem:
            cont = re.search(r'{}([\w\W]+?)[@#]'.format(extra),elem).groups()
            extra = extra.strip("#")
            cont = cont[0].strip("\n")
            cont = cont.strip(".-")
            cont = cont.strip()
            cont = re.sub(r'\s+',' ',cont)
            dicionario[num][extra] = cont
    subtemas = ["#SUBT","#Vid"]
    if "#SUBT" in elem:
        subt = [sub for sub in re.findall(r'#SUBT(.+\n(.+\n)*?)#',elem)]
        vid = [sub for sub in re.findall(r'#Vid(.+\n(.+\n)*?)[@#]',elem)]  # um subt tem sempre um vid
        subt = subt[0]
        vid = vid[0]
        rel = {}
        for i in range(len(subt)):
            if subt[i]!="" and vid[i]!="":
                subt_c = subt[i].strip("\n")
                subt_c = subt_c.strip(".-")
                subt_c = subt_c.strip(" ")

                vid_c = vid[i].strip("\n")
                vid_c = vid_c.strip(".-")
                vid_c = vid_c.strip(" ")
                rel[subt_c] = vid_c
                dicionario[num]["Termos relacionados"] = rel

    trad= re.findall(r"(pt|en|es|la)@([\w\W]+?[@#])",elem)
    for idioma in trad:
        cod_pais = idioma[0]
        tradu = idioma[1].replace("\n"," ")
        tradu = tradu.replace("@","")
        tradu= tradu.strip("#")
        tradu= tradu.strip("@")
        tradu= tradu.strip()
        tradu = re.sub(r'\s+',' ', tradu)
        dicionario[num][cod_pais] = tradu




file_out = open("dados.json","w", encoding="utf-8")
json.dump(dicionario,file_out,  indent=4, ensure_ascii=False)
file_out.close()
