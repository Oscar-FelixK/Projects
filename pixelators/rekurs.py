numb = 5

def self(num):
    if num > 0:
        num -= 1
        print(num)
        self(num)

self(numb)