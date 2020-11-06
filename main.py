import pandas as pd
import matplotlib.pyplot as plt
import warnings
from pprint import pprint
from data_loading import load
from utils import average_age_of_first_line_code, python_developers_count 
from utils import salary_avg_plot, desire_languages_2020, code_as_a_hobby
from utils import job_career_sat_plot, job_career_sat_plot_based_continent

warnings.filterwarnings('ignore')
plt.style.use('ggplot')

filename = 'survey_results_public.csv'
df = load(filename)
qns = [
    '1. Average age of developers when they wrote their first line of code.',
    '2. Percentage of developers who know python in each country.',
    '3. Average salary of developer based on continent.',
    '4. Most desired programming language for the year 2020.',
    '5. People who code as a hobby based on gender and continent.',
    '6. Job and Career satisfaction of developer based on their gender and continent.',
]

if __name__ == '__main__':
    while True:
        pprint(qns)
        question = input('Select Option (q for quit): ')
        if question == '1':
            print('Computing...')
            average_age_of_first_line_code(df.Age1stCode)
        elif question == '2':
            print('Computing...')
            selected_columns = ['LanguageWorkedWith','Country']
            python_developers_count(df[selected_columns])
        elif question == '3':
            print('Computing...')
            selected_columns = ['Country','ConvertedComp']
            salary_avg_plot(df[selected_columns])
        elif question == '4':
            print('Computing...')
            desire_languages_2020(df.LanguageDesireNextYear)
        elif question == '5':
            print('Computing...')
            selected_columns = ['Hobbyist', 'Gender', 'Country']
            code_as_a_hobby(df[selected_columns], column='Gender')
            code_as_a_hobby(df[selected_columns], column='Continent')
        elif question == '6':
            print('Computing...')
            selected_columns = ['CareerSat', 'JobSat', 'Gender', 'Country']
            title_job = 'Job Satisfaction'
            job_career_sat_plot(df[selected_columns], title=title_job, 
                                column='JobSat')
            title_career = 'Career Satisfaction'
            job_career_sat_plot(df[selected_columns] ,title=title_career, 
                                column='CareerSat')
            job_career_sat_plot_based_continent(df[selected_columns], 
                                                title=title_job, column='JobSat')
            job_career_sat_plot_based_continent(df[selected_columns], 
                                                title=title_career, column='JobSat')
        elif question == 'q':
            print('exit')
            break
        else:
            print('Invalid Option, Try again...')
