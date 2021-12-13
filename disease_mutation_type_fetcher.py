import requests
import bs4
from bs4 import BeautifulSoup


with open("disease_list.txt") as readfile:
    disease_list = readfile.read().split("\n")

disease_urls = []
base_url = "https://www.ncbi.nlm.nih.gov/clinvar/?term="
for disease in disease_list:
    disease_words = disease.split(" ")
    disease_string = ""
    for dw in disease_words:
        disease_string = disease_string + dw + "+"
    disease_string = disease_string[0:(len(disease_string)-1)]
    disease_url = base_url +disease_string
    disease_urls.append(disease_url)


disease_dicts = []
for disease_url in disease_urls[6324:]:
    disease_dict = {}
    try:
        req = requests.get(disease_url)
    except:
        print("couldn't get "+disease_url)
    soup = BeautifulSoup(req.content,"html.parser")
    variant_type = None
    for sclass in soup.find_all("ul", class_="facet"):
        if (str(sclass.get("data-filter_id")).find("VariantType")) != -1:
            variant_type = sclass

    
    if variant_type == None:
        print("no variant type heading found")
    else:
        filtergrp = None
        try:
            filtergrp = variant_type.find("li", "filter_grp")
        except:
            pass

        if filtergrp != None:
            uloflis = None
            try:
                uloflis = filtergrp.find("ul")
            except:
                pass

            if uloflis != None:
                lis = None
                try:
                    lis = uloflis.find_all("li")
                except:
                    pass
                
                if lis != None:
                    freqsum = 0
                    for li in lis:
                        mut_type = (str(li).split('href="#">')[1]).split("</a>")[0]
                        freq = (str(li).split('"fcount">(')[1]).split(")")[0]
                        freq = freq.replace(",","")
                        freqsum = freqsum+int(freq)
                        disease_dict[mut_type] = int(freq)

                    for k in disease_dict.keys():
                        if freqsum > 0:
                            disease_dict[k] = str((round((disease_dict[k]/freqsum),2)*100))+'%'
                        else: pass
                    dis = disease_url.split("term=")[1]
                    print(dis+ " "+ str(disease_dict))
                    with open("disease_data.txt","a") as writefile:
                        dis = dis.replace("+", " ")
                        writefile.write(dis + "," + str(disease_dict) + "\n")
                        writefile.close()
                    disease_dicts.append(disease_dict)
