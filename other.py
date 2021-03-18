# https://www.zipcomic.com/img/s3/philip-k-dick-a-comics-biography/tpb/02.jpg
import os
import time
import webbrowser
import requests

FOLDER = 'D:\\BGC_ARCHIVE_TMP\\wtf'

for i in range(1, 250):
    url = f'https://i.i9i9.to/image/1608603/{i}.jpg'
    webbrowser.open_new_tab(url)

    if i % 10 == 0:
        input()

    # r = requests.get(url)
    #
    # mark = url.find('?')
    # if mark != -1:
    #     url = url[:mark]
    #
    # filename = url.rsplit('/', 1)[1]
    # content = r.content
    # path = os.path.join(FOLDER, filename)
    # with open(path, mode='wb') as file:
    #     file.write(content)
    #
    # print(filename)
    # time.sleep(1.0)
