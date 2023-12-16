from datetime import datetime, timedelta
import pandas as pd

def transform_date(date, full=True):
    if len(date.split("-")) == 1:
        date = parse_relative_date(date)
    elif len(date.split("-")) == 2:
        date = datetime.strptime(date, '%m-%d')
        date = date.replace(year=datetime.now().year)
    else:
        date = datetime.strptime(date, '%Y-%m-%d')
    
    if full: return date
    return date.strftime("%Y-%m-%d")


def is_date_between(date, start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date = transform_date(date)
    return start_date <= date <= end_date


def parse_relative_date(date):
    delta_mapping = {'s': 'seconds', 'm': 'minutes', 'h': 'hours', 'd': 'days', 'w': 'weeks'}
    quantity, unit = date.split()[0][:-1], date.split()[0][-1]
    delta = timedelta(**{delta_mapping[unit[0].lower()]: int(quantity)})
    return datetime.now() - delta


def save_results(RESULTS):
    results = pd.DataFrame(RESULTS)
    results = results.drop_duplicates(subset=['media link'])
    FILTRED_DESCRIPTIONS = [[description for description in results['description'].iloc[idx] if description not in ['', ' ']] for idx in range(len(results))]
    results['description'] = FILTRED_DESCRIPTIONS
    results.to_csv("RESULTS.csv", index=False)