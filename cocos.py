import zipfile
import xxtea
import zlib
import re
import os

# setXXTEAKeyAndSign

apk = zipfile.ZipFile("pzmj.apk", "r")

probe_file = []
for filename in apk.namelist():
    if filename.endswith(".luac"):
        probe_file.append(apk.read(filename))
        print ('File:', filename)
        if len(probe_file)==2:
            break


sign = []
for i in range(len(probe_file[0])):
    if probe_file[0][i]!=probe_file[1][i]:
        sign= probe_file[0][:i]
        break
print('Sign:', sign, len(sign))


key = []
pattern = re.compile("(\w+)\0")
for filename in apk.namelist():
    if filename.endswith("libcocos2dlua.so"):
        print ('File:', filename)
        content = apk.read(filename)
        pos = content.find(sign)
        subcontent = content[pos-512:pos+512]

        sign = sign.decode()
        strlist = pattern.findall(subcontent.decode("ascii", "ignore"))
        for index, found_str in enumerate(strlist):
            if found_str==sign:
                key = strlist[index-1].encode('ascii')


print('Key:', key)

for filename in apk.namelist():
    if filename.endswith(".luac"):
        content = apk.read(filename)
        data = xxtea.decrypt(content[len(sign):], key)
        filename = os.path.splitext(filename)[0] + ".lua"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # os.makedirs(os.path.dirname(filename))
        print(filename)
        with open(filename, 'wb') as decrypted_file:
            decrypted_file.write(data)