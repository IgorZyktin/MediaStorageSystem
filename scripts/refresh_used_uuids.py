import os

FOLDER = 'D:\\BGC_ARCHIVE\\bubblegum_crisis'


def main():
    path = os.path.join(FOLDER, 'metainfo')
    meta = [x[:-5] for x in os.listdir(path)]
    meta.sort()

    meta_path = os.path.join(FOLDER, 'used_uuids.csv')
    with open(meta_path, mode='w', encoding='utf-8') as file:
        for line in meta:
            file.write(line + '\n')


if __name__ == '__main__':
    main()
