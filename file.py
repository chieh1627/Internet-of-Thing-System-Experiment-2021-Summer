# 讀取檔案內文字。
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        return text


# 寫入文字至檔案內。
def write_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
