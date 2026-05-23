from IPython.display import display, Markdown

def printh(h="h1", text=""):
    display(Markdown('<{}>{}</{}>'.format(h, text, h)))

def xfrange(start, stop, step):
    i = 0
    while start + i * step < stop:
        yield start + i * step
        i += 1

def scale(input_df, cols=None, scaler_class=None, scalers=None):
    _input_df = input_df.copy()
    if scalers:
        for k, v in scalers.items():
            _input_df[k] = v.transform(_input_df[[k]].copy())
    else:
        scalers = {}
        for col in cols:
            scaler = scaler_class()
            _input_df[col] = scaler.fit_transform(_input_df[[col]].copy())
            scalers[col] = scaler
    return _input_df, scalers
