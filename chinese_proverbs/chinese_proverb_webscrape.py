"""
https://www.kaggle.com/bryanb/scraping-sayings-and-proverbs/notebook
"""

# Libraries
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import re

# The URL I scrap data on
url = 'https://www.fluentin3months.com/chinese-proverbs/'

# Prepare GET request
response = get(url)

# Retrieve the webpage and store it as an bs4.BeautifulSoup object
html_soup = BeautifulSoup(response.content.decode('UTF-8', 'ignore'), 'html.parser')

proverbs_container = html_soup.find_all('div', class_='col-md-7 col-sm-8 entry-content')


def starts_with_digit(text):
    """
    Return boolean, does 'text' starts with a number
    text: string
    """

    output = False
    # This pattern finds if a string is starting is a number
    pattern = re.compile(r'\d*')
    # If this pattern match with something, return True
    if pattern.search(text).group() != '':
        output = True

    return output


# All the p tags in proverbs_container
to_browse = proverbs_container[0].find_all('h3')

# List of sentence starting with a number
mask = [starts_with_digit(quote.text) for quote in to_browse]

# Filter to get all the proverbs
list_of_proverbs = [to_browse[i].text for i in range(len(mask)) if mask[i] == True]

pattern_chinese = re.compile(r'((?<=\d[\S].)(.*)(?=\())')
# pattern_chinese.search( "6. 三个和尚没水喝。 (Sān gè héshàng méi shuǐ hē. 'three monks have no water to drink') — Too many
# cooks spoil the broth.").group()

pattern_pin_yin = re.compile(r'((?<=\()(.*?)(?=\)))')
# pattern_pin_yin.search( "6. 三个和尚没水喝。 (Sān gè héshàng méi shuǐ hē. 'three monks have no water to drink' — Too many
# cooks spoil the broth.").group()

pattern_translation = re.compile(r'(?<=“)(?:\\.|[^"\\])*(?=”)')
# pattern_translation.search(
#     "1. 有缘千里来相会。 (yǒuyuán qiānlǐ lái xiāng huì) – “Fate has us meet from a thousand miles away.”").group()

chinese_proverbs = pd.DataFrame()
chinese_proverbs['all_text'] = list_of_proverbs
chinese_proverbs['in_chinese'] = chinese_proverbs['all_text'].apply(lambda x: pattern_chinese.search(x).group())
chinese_proverbs['pin_yin'] = chinese_proverbs['all_text'].apply(lambda x: pattern_pin_yin.search(x).group())
chinese_proverbs['text'] = chinese_proverbs['all_text'].apply(lambda x: pattern_translation.search(x).group())
chinese_proverbs = chinese_proverbs.drop(['all_text'], axis=1)

proverbs_container[0].find_all('h2')

chinese_proverbs.head()

# Save all the data in .csv file
chinese_proverbs.to_csv('Chinese_proverbs.csv')
