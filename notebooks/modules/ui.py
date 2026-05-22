import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_hist(df, features, figwidth=12):
    len_ft = len(features)
    fig, axes = plt.subplots(1, len_ft, figsize=(figwidth,3))
    if isinstance(axes, np.ndarray) is False:
        axes = np.array([axes])
    for idx, ft in enumerate(features):
        sns.histplot(df[ft], kde=True, ax=axes[idx])
        axes[idx].set_title(ft)
    plt.tight_layout()
    plt.show()

def show_hists(df, features, n=4):
    loop = math.ceil(len(features) / n)
    for idx in range(loop):
        if idx == 0:
            show_hist(df=df, features=features[:n], figwidth=12)
        elif idx == (loop-1):
            remainder = len(features) - (idx * n)
            remainder_width = math.ceil(12 * remainder / n)
            show_hist(df=df, features=features[n*(loop-1):], figwidth=remainder_width)
        else:
            show_hist(df=df, features=features[n*idx:n*(idx+1)], figwidth=12)

def show_skew_kurt(df, print_result=True):
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    skewness = df[numerical_columns].skew()
    kurtosis = df[numerical_columns].kurt()
    sk_df = pd.DataFrame(
        {"skewness": skewness, "kurtosis": kurtosis},
        index=numerical_columns,
    )
    if print_result:
        print(sk_df)
    return sk_df

def show_corr(df):
    corr = df.corr()
    size = corr.shape[0]
    size = min(size, 15)
    plt.figure(figsize=(size, size))
    sns.heatmap(df.corr(),annot=True,cbar=True,cmap='coolwarm')
    plt.show()

def draw_map(input_df, coor_x, coor_y, label, scale_factor=100, group_by=None, log=False):
    input_df[coor_x] = np.round(input_df[coor_x] * scale_factor)
    input_df[coor_y] = np.round(input_df[coor_y] * scale_factor)
    # if log:
    #     print("x100 round\n", input_df.head(), input_df.shape,"\n")

    if group_by == "mean":
        input_df = input_df.groupby([coor_x,coor_y])[label].mean().reset_index()
    else:
        input_df = input_df.groupby([coor_x,coor_y])[label].first().reset_index()
    input_df[coor_x] = pd.to_numeric(input_df[coor_x], downcast="integer")
    input_df[coor_y] = pd.to_numeric(input_df[coor_y], downcast="integer")
    # if log:
    #     print("GroupByXYAveragePrice\n", input_df.head(), input_df.shape, "\n")
    
    min_coor_x = min(input_df[coor_x])
    max_coor_x = max(input_df[coor_x])
    min_coor_y = min(input_df[coor_y])
    max_coor_y = max(input_df[coor_y])
    width = int(max(input_df[coor_x]) - min(input_df[coor_x]))
    height = int(max(input_df[coor_y]) - min(input_df[coor_y]))

    Z = np.full((height+1, width+1), -1)
    x = np.arange(min_coor_x, max_coor_x+1, 1) / scale_factor
    y = np.arange(min_coor_y, max_coor_y+1, 1) / scale_factor

    if log:
        print("=== input_df x y Z")
        print("input_df", input_df.shape)
        print("x", x.shape)
        print("y", y.shape)
        print("x*y", x.shape[0] * y.shape[0])
        print("Z", Z.shape)
    # for idx in range(0, width+1):
    #     for jdx in range(0, height+1):
    #         value = input_df.loc[(input_df[coor_x] == min_coor_x+idx) & (input_df[coor_y] == min_coor_y+jdx), label]
    #         if len(value) > 0:
    #             Z[jdx][idx] = value.iloc[0]

    for idx, row in input_df.iterrows():
        _x = int(row[coor_x] - min_coor_x)
        _y = int(row[coor_y] - min_coor_y)
        # if log:
        #     print(row[coor_x], row[coor_y], min_coor_x, min_coor_y, _x, _y)
        Z[_y][_x] = row[label]

    # Z[0][0] = 9000000

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title(label)
    ax.set_xlabel(coor_x)
    ax.set_ylabel(coor_y)
    # ax.set_box_aspect(1.0)
    mesh = ax.pcolormesh(x, y, Z, cmap="viridis")
    fig.colorbar(mesh, ax=ax)
    plt.show()
