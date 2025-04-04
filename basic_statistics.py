import pandas as pd
import numpy as np
import warnings
# UserWarning만 무시
warnings.filterwarnings('ignore', category=UserWarning)

def read_data(file_path):
    return pd.read_csv(file_path)

def how_many_nas(data):
    return data.isna().sum()

def data_info(data):
    return data.info()

def data_describe(data):
    return data.describe()

def date_var(data):
    for col in data.columns:
        if data[col].dtype=='O':
            try:
                # 날짜 변환 시도
                converted = pd.to_datetime(data[col], errors='raise', infer_datetime_format=True)

                # 변환 성공하면, 해당 컬럼을 날짜 타입으로 업데이트
                data[col] = converted
                print(f"✅ '{col}' 컬럼은 날짜 데이터로 변환되었습니다.")
            except (ValueError, TypeError):
                print(f"❌ '{col}' 컬럼은 날짜 데이터가 아닙니다.")
    print(data.info())

def get_categorical_columns(df, threshold=0.05):
    """
    문자열 타입(object) 컬럼 중에서 고유값 비율이 threshold 이하인 컬럼만 반환
    - threshold: 고유값 개수 / 전체 개수 기준 (기본값 5%)
    """
    categorical_cols = []

    for col in df.columns:
        if df[col].dtype == 'object':
            nunique = df[col].nunique()
            total = len(df[col])
            unique_ratio = nunique / total

            if unique_ratio < threshold:
                categorical_cols.append(col)

    return categorical_cols

def unique_var(data):
    for col in get_categorical_columns(data):
        print(f"'{col} 컬럼은 범주형 데이터입니다.")
        print(data[col],'unique values :', data[col].unique())
        print(data[col], 'unique counts :', data[col].nunique())
        data[col]=data[col].astype('category')
        print(f"✅ '{col} 컬럼은 범주형 데이터로 변환되었습니다.")
        print('\n')

def all_process(file_path):
    data=read_data(file_path)
    print("=== 결측치 현황 ===")
    print(how_many_nas(data))
    print("\n")

    print("=== 데이터 정보 ===")
    data_info(data)
    print("\n")

    print("=== 기초 통계량 (describe) ===")
    print(data_describe(data))
    print("\n")

    print("=== 날짜형 변수 변환 ===")
    date_var(data)
    print("\n")

    print("=== 범주형 변수 변환 및 고유값 확인 ===")
    unique_var(data)