def tag(tag_name):
    def add_tag(content):
        return "<{0}>{1}</{0}>".format(tag_name, content)
    return add_tag
    
content = 'Hello'
a = tag('a')
b = a('aaa')
print(b)