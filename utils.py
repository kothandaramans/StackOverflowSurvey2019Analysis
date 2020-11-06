import pandas as pd
import matplotlib.pyplot as plt
import pycountry_convert as pc

def average_age_of_first_line_code(Age1stCode):
    # Drop NA/NaN observations of Age1stCode
    Age_df = Age1stCode.dropna()
    responses = Age_df.count()
    # Convert Object to integer
    age_old = ('Younger than 5 years','Older than 85')
    age_new = (4, 87)
    Age_df = pd.to_numeric(Age_df.replace(age_old, age_new))
    mean = int(round(Age_df.mean()))
    Age_df.plot(kind='hist', title=f'From {responses} responses', 
                label= f'Average Age: {mean} to {mean+1}')
    plt.xlabel('Age')
    plt.legend()
    plt.show()
    
def python_developers_percent(py_dev, dev, responses):
    cols = ['python_developers_count', 'total developers_count', 
               'python_developers_percentage']
    py_percent = pd.DataFrame.from_dict(py_dev, orient='index', dtype=None, 
                                        columns=[cols[0]])
    py_percent[cols[1]] = dev.values()
    py_percent[cols[2]] = (py_percent[cols[0]] / py_percent[cols[1]]) * 100
    # top most highest python developers country
    top = py_percent.sort_values(by=cols[2], ascending=False).head(10)[cols[2]]
    ax = top.sort_values(ascending=True).plot(kind='barh', figsize=(10, 8), 
         title=f'Top 10 highest Python developers country ({responses} responses)')
    for i in ax.patches:
        ax.text(i.get_width()+.2, i.get_y()+.1, str(round(i.get_width(), 2)) + '%')
    plt.tight_layout()
    plt.show()
    
def python_developers_count(languageworked_df):
    languageworked_df = languageworked_df.dropna()
    responses = languageworked_df.count()[0]
    languageworked_df['LanguageWorkedWith'] = languageworked_df.LanguageWorkedWith + ';'
    languageworked_df = languageworked_df.groupby('Country').sum()
    countries_python = {}
    countries_developer = {}
    for country,languages in zip(languageworked_df.index, 
                                 languageworked_df['LanguageWorkedWith']):
        count = 0
        for language in languages.split(';'):
            count += 1
            if language in ['Python', 'python', 'PYTHON']:
                if country not in countries_python.keys():
                    countries_python[country] = 1
                else:
                    countries_python[country] += 1
        if country not in countries_python.keys():
            countries_python[country] = 0
        countries_developer[country] = count
    return python_developers_percent(countries_python, countries_developer, 
                                     responses)

def country_to_continent(country):
    country_from = ('Hong Kong (S.A.R.)', 'Venezuela, Bolivarian Republic of...', 
                    'The former Yugoslav Republic of Macedonia', 
                    'Libyan Arab Jamahiriya', 'Republic of Korea',
                    'Congo, Republic of the...')
    country_to = ('Hong Kong', 'Venezuela', 'Macedonia', 'Libya', 'South Korea',
                  'Congo')
    if country == 'Other Country (Not Listed Above)':
        return 'Not Mentioned'
    if country == 'Timor-Leste':
        return 'Asia'
    if country in country_from:
        country = country_to[country_from.index(country)]
    return pc.convert_continent_code_to_continent_name(pc.country_alpha2_to_continent_code
           (pc.country_name_to_country_alpha2(country)))


def salary_avg_plot(salaries_df):
    clean_salaries_df = salaries_df.dropna().reset_index()
    clean_salaries_df['Continent'] = clean_salaries_df.Country.apply(country_to_continent)
    # now lets plot salary distributions for the continents
    continents = clean_salaries_df['Continent'].value_counts().sort_values(ascending=False)[:6].index.tolist()

    for i,continent in enumerate(continents):
        plt.subplot(2,3,i+1)
        temp_salaries = clean_salaries_df.loc[clean_salaries_df['Continent'] == continent, 'ConvertedComp']
        ax = temp_salaries.plot(kind='kde', figsize=(15,7))
        ax.axvline(temp_salaries.mean(), linestyle = '-', color = 'red')
        ax.text((temp_salaries.mean() + 1500), (float(ax.get_ylim()[1])*0.55), 'mean = $ ' + str(round(temp_salaries.mean(),0)), fontsize = 12)
        ax.set_xlabel(f'Annual Salary in USD => {temp_salaries.count()} responses')
        ax.set_xlim(-temp_salaries.mean(),temp_salaries.mean()+2*temp_salaries.std())
        ax.set_title('Annual Salary Distribution in {}'.format(continent))
    plt.tight_layout()
    plt.show()

# develop a function that will be used for plotting bar graphs (horizontal)
def plot_dimension_count(unique_dim_dict, plot_title):
    dim_count = pd.DataFrame.from_dict(unique_dim_dict, orient='index', dtype=None)
    dim_count.columns = ['Count']
    dim_count.sort_values('Count',ascending=True,inplace=True)
    ax = dim_count.plot(kind = 'barh', figsize = (12,10), fontsize = 10, title = plot_title)
    for i in ax.patches:
        ax.text(i.get_width()+.2, i.get_y()+.1, str(round((i.get_width() / 84088) * 100, 2)) + '%')
    plt.tight_layout()
    plt.show()

def desire_languages_2020(desireLanguage):
    desireLanguage_df = desireLanguage.dropna()
    responses = desireLanguage_df.count()
    desire_languages = {}
    # split the languages on ;
    for language_set in desireLanguage_df.apply(lambda row: str(row).split(';')):
        for language in language_set:
            if language not in desire_languages.keys():
                desire_languages[language] = 1
            else:
                desire_languages[language] += 1
    plot_dimension_count(desire_languages, f'Most desired programming language for the year 2020 ({responses} responses)')

def gender_rearrange(gender_df):
    # Gender Transformation
    gender_old = gender_df.Gender.unique().tolist()[2:]
    gender_df.Gender.replace(gender_old, 'Others', inplace=True)

def code_as_a_hobby(hobby_df, column):
    hobby_df = hobby_df.dropna()
    gender_rearrange(hobby_df)
    hobby_df['Continent'] = hobby_df.Country.apply(country_to_continent)

    for i, value in enumerate(hobby_df[column].unique()):
        plt.subplot(3,3,i+1)
        temp = hobby_df.loc[hobby_df[column] == value, 'Hobbyist'].value_counts()
        reponses = temp.sum()
        Yes = temp.Yes/temp.sum() * 100
        No = temp.No/temp.sum() * 100
        temp['Yes'], temp['No'] = Yes, No
        ax = temp.plot(kind='bar', figsize=(15,8), color=['g','b'])
        ax.set_title(f'Code as a hobby in Percentage ({value})')
        plt.xlabel(f'{reponses} responses')

    plt.tight_layout()
    plt.show()

def job_career_sat_plot(job_career_df ,title, column):
    clean_job_career_df = job_career_df.dropna()
    # Gender Transformation
    gender_rearrange(clean_job_career_df)
    for i, gender in enumerate(clean_job_career_df.Gender.unique()):
        plt.subplot(2,2,i+1)
        temp = clean_job_career_df.loc[clean_job_career_df['Gender'] == gender][column].value_counts()
        ax = temp.plot(kind='pie',figsize=(15,10), autopct='%1.2f%%')
        ax.axis('equal')
        ax.set_title(f'{title} ({gender}) => {temp.sum()} responses')

    plt.tight_layout()
    plt.show()

def job_career_sat_plot_based_continent(job_career_df, title, column):
    clean_job_career_df = job_career_df.dropna()
    clean_job_career_df['Continent'] = clean_job_career_df.Country.apply(country_to_continent)
    for i, continent in enumerate(clean_job_career_df.Continent.unique()[:-1]):
        plt.subplot(3,2,i+1)
        temp = clean_job_career_df.loc[clean_job_career_df['Continent'] == continent][column].value_counts()
        ax = temp.plot(kind='pie', autopct='%1.2f%%', figsize=(15,10))
        ax.axis('equal')
        ax.set_title(f'{title} ({continent}) => {temp.sum()} responses')

    plt.tight_layout()
    plt.show()
