from IPython.display import display, Markdown

def printh(h="h1", text=""):
    display(Markdown('<{}>{}</{}>'.format(h, text, h)))

def xfrange(start, stop, step):
    i = 0
    while start + i * step < stop:
        yield start + i * step
        i += 1

