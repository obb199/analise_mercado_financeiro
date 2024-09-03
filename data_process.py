import pandas as pd

COLS_TO_DROP = ['TckrSymb', 'XprtnCd',
                    'SgmtNm', 'OpnIntrst',
                    'VartnOpnIntrst', 'DstrbtnId',
                    'BrrwrQty', 'LndrQty',
                    'CurQty', 'FwdPric']


def data_process(csv_path):
    df = pd.read_csv(csv_path, sep=';') # alterar para tornar dinâmico

    df_equity_call = df[df['SgmtNm'] == 'EQUITY CALL'].drop(columns=COLS_TO_DROP)
    df_equity_put = df[df['SgmtNm'] == 'EQUITY PUT'].drop(columns=COLS_TO_DROP)

    df_equity_call = df_equity_call.rename({'Asst': 'Ativo',
                                            'CvrdQty': 'QuantidadeCoberta',
                                            'TtlBlckdPos': 'TotalDePosiçõesBloqueadas',
                                            'UcvrdQty': 'QuantidadeDescoberta',
                                            'TtlPos': 'TotalDePosições',
                                            'RptDt': 'Data'}, axis='columns')

    df_equity_put = df_equity_call.rename({'Asst': 'Ativo',
                                           'CvrdQty': 'QuantidadeCoberta',
                                           'TtlBlckdPos': 'TotalDePosiçõesBloqueadas',
                                           'UcvrdQty': 'QuantidadeDescoberta',
                                           'TtlPos': 'TotalDePosições',
                                           'RptDt': 'Data'}, axis='columns')

    return df_equity_call.drop_duplicates(), df_equity_put.drop_duplicates()
