import re

def markdown_to_html(text):
    text = re.sub(r'^### (.*)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*)', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)


    lines = text.split('\n')
    new_text = []
    inside_list = False

    for line in lines:
        if re.match(r'^\d+\.\s', line):
            if not inside_list:
                new_text.append('<ol>')
                inside_list = True
            line = re.sub(r'^\d+\.\s+(.*)', r'<li>\1</li>', line)
            new_text.append(line)
        else:
            if inside_list:
                new_text.append('</ol>')
                inside_list = False
            new_text.append(line)
    if inside_list:
        new_text.append('</ol>')

    return '\n'.join(new_text)


example_text = ""

final_html = markdown_to_html(example_text)
print(final_html)