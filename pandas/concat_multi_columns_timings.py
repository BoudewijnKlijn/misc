import timeit

import pandas as pd

# Create dataframe with 17 columns and 3 million rows, all strings
df = pd.DataFrame({chr(i + 65): [chr(i + 97)] * 3_000_000 for i in range(17)})

columns = list(df.columns)
sep = "_"
new_col = "new"


def create_exec_statement(
    df_variable_name="df",
    columns_variable_name="columns",
    new_column_name="new",
    separator="_",
):
    columns_strings = [
        f"{df_variable_name}[{columns_variable_name}[{i}]]"
        for i in range(len(eval(columns_variable_name)))
    ]
    separator = f" + '{separator}' + "
    statement = (
        f'{df_variable_name}["{new_column_name}"] = {separator.join(columns_strings)}'
    )
    return statement


def f1():
    exec(
        create_exec_statement(
            df_variable_name="df",
            columns_variable_name="columns",
            new_column_name=new_col,
            separator=sep,
        )
    )


def f2():
    df[new_col] = df[columns[0]].str.cat(df[columns[1:]], sep=sep)


def f3():
    df[new_col] = df[columns].T.add(sep).sum().str[:-1]


def f4():
    df[new_col] = df[columns].add(sep).sum(axis=1).str[:-1]


def f5():
    df[new_col] = df[columns].apply(lambda x: sep.join(x), axis=1)


def f6():
    df[new_col] = df[columns].agg(sep.join, axis=1)


def f7():
    df[new_col] = df[columns].T.agg(sep.join)


if __name__ == "__main__":
    for func in [f1, f2, f3, f4, f5, f6, f7]:
        print(f"{func.__name__}: {timeit.repeat(func, number=1, repeat=3)}")

# Results
# f1: [4.366812400025083, 4.43233589999727, 4.370704000000842]
# f2: [5.970817499997793, 5.898356199992122, 5.80382699999609]
# f3: [5.981191200000467, 5.959296400018502, 5.963758500001859]
# f4: [5.967713599995477, 6.032882600004086, 6.010665400011931]
# f5: [11.023198500013677, 10.792945499997586, 10.91107919998467]
# f6: [10.698224400024628, 10.668694899999537, 10.707435600023018]
# f7: [31.499697799998103, 31.31905089999782, 31.4950811000017]
