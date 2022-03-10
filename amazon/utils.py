import csv

def parse_rating(value):
    return value.split(' ')[0]

def parse_price(value):
    return value[1:]

def parse_title(value):
    return value.strip()


def parse_review_text(value):
    return value.replace("\n", '').strip()

def parse_date(value):
    return value.split("on")[1].strip()

def parse_loc(value):
    loc = value.split("on")[0]
    return loc.split("in")[1].strip()

def parse_helpful(value):
    return value.split(" ")[0].strip()

def get_asin_list(file) -> list:
    asin_list = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i==0:
                continue #header
            if row[0]:
                asin_list.append(row[0])
        return asin_list