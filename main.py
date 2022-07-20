import numpy as np
import os
import csv
from gensim.models.word2vec import Word2Vec

w2v_model = Word2Vec.load('Word2VecModel12')
data = []
fails = []
m = open('namefull19.csv', 'w', newline='')
fieldnames = ['регион', 'сайт', "строка 1", "строка 2", "rate"]
writer = csv.DictWriter(m, fieldnames=fieldnames)
writer.writeheader()


def gensim(str1, str2, folder, folders):
    global fails
    list1 = []
    list2 = []
    s = ""
    b = 0
    c = 0
    patterns = "[QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm0123456789!#$%&'()*«+,./:;<=>?@[\]_»`{|}~—\"\-]+"
    if "утвержд" in str1[:15]:
        if "город" in str1 and "город" not in str2:
            writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "город"})
        elif "республик" in str1 and "республик" not in str2:
            writer.writerow(
                {'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "республика"})
        elif "округ" in str1 and "округ" not in str2:
            writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "округ"})
        elif "администрац" in str1 and "администрац" not in str2:
            writer.writerow(
                {'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "администрация"})
        elif "район" in str1 and "район" not in str2:
            writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "район"})
    elif " мо " in str1 and (
            ("муницип" not in str2 or "образов" not in str2) and ("муницип" not in str2 or "округ" not in str2) and (
            " мо " not in str2)):
        writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "мо"})
        b = 1
    elif " рб" in str1 and (
            (("республик" not in str2 or "башкортостан" not in str2) and (
                    "республик" not in str2 or "бурятия" not in str2))):
        writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "башкортостан"})
        b = 1
    elif " мр " in str1 and ("муницип" not in str2 or "район" not in str2):
        writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "мр"})
        b = 1
    elif " бр " in str1 and ("белорецк" not in str2 or "район" not in str2):
        writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "бр"})
        b = 1
    elif " сп " in str1 and ("сельск" not in str2 and "поселен" not in str2):
        writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": "сп"})
        b = 1
    elif (" районная" in str1 and " дум" in str1) or ("городск" in str1 and "дума" in str1) or (
            "администрация" in str1 and ("район" in str1[str1.find("администрация"):] or "округ" in str1[str1.find(
        "администрация"):str1.find("администрация") + 15])):
        b = 1
    elif b == 0:
        s = ''
        for i in range(len(str1)):
            if str1[i] not in patterns:
                s += str1[i]
            elif str1[i] in patterns:
                s += " "
        list2 = s.split(" ")
        s = ''
        for i in range(len(str2)):
            if str2[i] == "\*"[0]:
                s += " "
            else:
                s += str2[i]
        list1 = s.split(" ")
        s = ''
        for i in range(len(str1)):
            if str1[i] not in patterns:
                s += str1[i]
            else:
                s += " "
        list2 = s.split(" ")
        for i in range(len(list2)):
            if list2[i][:-3] not in str2:
                b += 1
            else:
                pass
        if len(str1) < len(str2):
            if b > len(list2) // 1.3 + 1:
                b = 0
                writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": 123})
            else:
                b = 1
        else:
            if b >= len(str1):
                b = 0
                writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2, "rate": 123})
            else:
                b = 1
    else:
        for i in range(len(str1)):
            if str1[i] not in patterns:
                s += str1[i]
                c = 1
            elif str1[i] in patterns and c == 1:
                s += " "
        list1 = s.split()
        s = ''
        c = 0
        for i in range(len(str2)):
            if str2[i] not in patterns:
                s += str2[i]
                c = 1
            elif str2[i] in patterns and c == 1:
                s += " "
        list2 = s.split()
        vec_list = []
        vec_list1 = []
        for i in list1:
            try:
                vec_list.append(w2v_model.wv[i])
            except:
                pass
        for i in list2:
            try:
                vec_list1.append(w2v_model.wv[i])
            except:
                pass
        vec_matrix = np.array(vec_list, dtype="float32")
        sent_vec = np.average(vec_matrix, axis=0)
        sent_vec = sent_vec / np.linalg.norm(sent_vec)

        vec_matrix1 = np.array(vec_list1, dtype="float32")
        sent_vec1 = np.average(vec_matrix1, axis=0)
        sent_vec1 = sent_vec1 / np.linalg.norm(sent_vec1)
        if sent_vec.dot(sent_vec1) < 0.8:
            writer.writerow({'регион': folder, "сайт": folders, "строка 1": str1, "строка 2": str2,
                             "rate": sent_vec.dot(sent_vec1)})
            print(sent_vec.dot(sent_vec1))


def start(directory, folder):
    b = 0
    predlen = 0
    global data
    patterns = "[QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm0123456789!#$%&'()*«+,./:;<=>?@[\]_»`{|}~—\"\-]+"
    # stopwords_ru = stopwords.words("russian")
    folders = os.listdir(directory)
    for file in range(len(folders)):
        data = []
        # print(stopwords_ru)
        dataset = open(directory + "\\" + folders[file] + "\\all_sources.txt", mode="r")
        print(directory + "\\" + folders[file])
        for i in dataset:
            if i != "":
                data.append(i[:-1].lower())
        for i in data:
            if i == "":
                data.pop(data.index(i))
        try:
            for i in range(0, len(data), 2):
                if str(data[i]).count("[") > 0 and str(data[i + 1]).count("\*"[0]) > 0:
                    gensim(data[i], data[i + 1], folder, folders[file])
                else:
                    if data[i].count("[") == 0 or data[i].count("\*"[0]) == 0:
                        data.pop(i)
                    elif data[i + 1].count("[") == 0 or data[i + 1].count("\*"[0]) == 0:
                        data.pop(i + 1)
        except Exception as exc:
            print(exc)
            pass
        print(len(data))


directory = "D:\\SourceAll"
folders = os.listdir(directory)
for i in range(len(folders)):
    start(directory + "\\" + folders[i], folders[i])
