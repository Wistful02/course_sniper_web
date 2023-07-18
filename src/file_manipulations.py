import os


def delete_index(index):
    index_numbers=[]
    with open(os.getenv('INDEX_FILE_TXT'), mode='r') as f:
        index_numbers = f.read().splitlines()
    print(index_numbers)
    print(index)
    index_numbers.remove(index)
    with open(os.getenv('INDEX_FILE_TXT'), mode='w') as f:
        for x in index_numbers:
            f.write(x+'\n')