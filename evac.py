import csv,os, json
evacdir = os.path.realpath('./evacdata')
paths = os.listdir(evacdir)
results = []
output = os.path.realpath('./result/evacdata.json')
for path in paths:

    with open(os.path.join(evacdir, path), encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for name, code, todofuken, ku, jyuusyo, lat, lon in reader:
            if ku != '渋谷区':
                continue
            result = dict(name=name, lat=lat, lon=lon)
            results.append(result)
with open(output, mode='w', encoding='utf-8') as fp:
    json.dump(results, fp, ensure_ascii=False)

    

