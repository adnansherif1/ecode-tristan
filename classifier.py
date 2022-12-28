# Importing the libraries
from bs4 import BeautifulSoup
import json
from bs4 import Comment
import re

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

import nltk
#nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')

import re
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn import datasets, linear_model
from sklearn.model_selection import ShuffleSplit

class model:
    model = model_sel = td = td_sel = unique = category = labels = None
def remove_comments_regexmethod(soup): 
    #soup argument can be string or bs4.beautifulSoup instance it will auto convert to string, please prefer to input as (string) than (soup) if you want highest speed
    if not isinstance(soup,str): 
        soup=str(soup)
    return re.sub(r'<!.*?->','', soup)

def categorizer(items,category):
    cats = {}
    for item in items:
        if item not in category:
            continue
        cat = category[item]
        if cat!="other":
            if cat not in cats:
                cats[cat] = 0
            cats[cat] +=1
    maximum = -1
    val = "other"
    for cat in cats:
        if cats[cat] > maximum:
            val = cat
            maximum = cats[cat]
    #print(val)
    return val  

def classify(dataset,vectorizer,classifier):
    dataset[0] = text_preprocess(dataset[0])    
    X = dataset.iloc[:, 0].values
    X = td.transform(X)
    y_pred = classifier.predict(X)
    return y_pred

def select_and_classify(data,u_data, labels, unique, category, td, classifier, td_sel, classifier_sel):
    new_data = []
    labels = labels
    sel_data = []
    idx = []
    idx_sel = []
    for i in range(len(data)):
        if data[i][1].lower() == 'input' and data[i][2] in ['text','email','url','date','month','tel','week']:
            idx.append(i)
            new_data.append([data[i][0],''])
        if (data[i][1].lower() == 'input' and data[i][2] in ['radio','checkbox']) or (data[i][2] == "select"):
            idx_sel.append(i)
            sel_data.append([data[i][0],data[i][3],data[i][1],data[i][2]]) 
    #print(new_data) 
    print(len(data))
    print(len(idx))
    
    # text input classification
    dataset = pd.DataFrame(new_data)
    dataset[0] = text_preprocess(dataset[0])
    X = dataset.iloc[:, 0].values
    X = td.transform(X)
    y_pred = classifier.predict(X)
    inp_cats = [labels[i] for i in y_pred]
    out = pd.DataFrame(dataset[0])
    out[1] = y_pred




#     # #select,radio,checkbox classification.
#     sel_data_preproc = []
#     for i in sel_data:
#         sel_data_preproc.extend(i[1])
#     dataset = pd.DataFrame(sel_data_preproc)
#     print("Sel_data",dataset)
#     dataset[0] = text_preprocess(dataset[0])    
#     X = dataset.iloc[:, 0].values
#     X = td_sel.transform(X)
#     y_pred_sel = classifier_sel.predict(X)

#     start = 0
#     inp_cats_sel = []
#     for i in sel_data:
#     #     print(i[1])
#         i[1] = y_pred_sel[start:start+len(i[1])]
#     #     print([unique[j] for j in i[1]])
#         i[1] = [unique[j] for j in i[1]]
#         cat = categorizer(i[1],category)
#         if cat == 'month':
#             cat = labels[classify(pd.DataFrame([i[0]]), td, classifier)[0]]
#         inp_cats_sel.append(cat)
#         start+=len(i[1])
#     # out_sel = pd.DataFrame(dataset[0])
#     # out_sel[1] = y_pred
#     #print(sel_data)


    #preparing input and category list for postprocess and value extraction
    #the inp list is filled up from the inp_cat or inp_cat_sel or "" according to idx and idx_sel respectively
    inps=[]
    tags=[]
    for i in range(len(data)):
        if i in idx:
            inps.append(inp_cats[idx.index(i)])
            tags.append(['text',""])
#         elif i in idx_sel:
#     #         print(i,inp_cats_sel)
#             inps.append(inp_cats_sel[idx_sel.index(i)])
#     #         print(sel_data[idx_sel.index(i)])
#             if sel_data[idx_sel.index(i)][2] == 'select':
#                 tags.append(['select',sel_data[idx_sel.index(i)][1]])
#             elif sel_data[idx_sel.index(i)][3] in ['radio','checkbox']:
#                 tags.append(['check',sel_data[idx_sel.index(i)][1]])
        else:
            inps.append("")
            tags.append(["",""])
    #print(inps,tags)
    output = postprocess(inps,u_data,tags)
    return output

def convert(data):
    conv_dict = {'location or Address pers': ['address', 'personal'],
     'Full Name': ['full-name', 'personal'],
     'Age Group': ['age-group', 'personal'],
     'City': ['city', 'personal'],
     'Country': ['country', 'personal'],
     'company name current': ['current-company', 'personal'],
     'Job Title current': ['current-position', 'personal'],
     'Do you have any disabilities': ['disability-status', 'personal'],
     'Email address': ['email', 'personal'],
     'Ethnicity': ['ethnicity', 'personal'],
     'First Name': ['first-name', 'personal'],
     'Gender': ['gender', 'personal'],
     'Github url': ['github', 'personal'],
     'Last Name': ['last-name', 'personal'],
     'Are you legally authorized to work in the United States?': ['legal-status',
      'personal'],
     'Linkedin url': ['linkedin', 'personal'],
     'Phone number': ['phone', 'personal'],
     'Prefer Pronouns': ['pronouns', 'personal'],
     'State': ['state', 'personal'],
     'Are you a protected veteran': ['veteran-status', 'personal'],
     'Will you now or in the future require sponsorship for employment visa status (e.g. H-1B)': ['working-visa',
      'personal'],
     'Zip Code': ['zip-code', 'personal'],
     'Field of Study': ['field', 'education'],
     'starting From or start date educ': ['from', 'education'],
     'GPA': ['gpa', 'education'],
     'skills': ['related-skills', 'education'],
     'courses': ['relevant-courses', 'education'],
     'degree': ['state', 'education'],
     'graduation educ': ['to', 'education'],
     'School or University': ['university', 'education'],
     'company name': ['company', 'experience'],
     'starting From or start date exps': ['from', 'experience'],
     'Job Title': ['job-title', 'experience'],
     'location or Address exps': ['location', 'experience'],
     'job description': ['role-description', 'experience'],
     'end date exps': ['to', 'experience'],
     'starting From or start date exps month':['start-month','experience'],
     'starting From or start date exps year':['start-year','experience'],
     'end date exps month':['end-month','experience'],
     'end date exps year':['end-year','experience'],
     'starting From or start date educ month':['start-month','education'],
     'starting From or start date educ year':['start-year','education'],
     'graduation month':['end-month','education'],
     'graduation year':['end-year','education'],
      'other' : ['other', 'personal']}
    
    for key,val in conv_dict.items():
    #     convert_dict[key] = [val, 'personal', 0]
        val.append(0)
    

    exps = data['experience']
    for exp in exps:
        if exps[exp]['from']:
            exps[exp]['start-month'] = exps[exp]['from'][5:]
            exps[exp]['start-year'] = exps[exp]['from'][:4]
        if exps[exp]['to']:
            exps[exp]['end-month'] = exps[exp]['to'][5:]
            exps[exp]['end-year'] = exps[exp]['to'][:4]
    educ  = data['education']
    if educ['from']:
        educ['start-month'] = educ['from'][5:]
        educ['start-year'] = educ['from'][:4]
    if educ['to']:
        educ['end-month'] = educ['to'][5:]
        educ['end-year'] = educ['to'][:4]
    data['personal']['full-name'] = data['personal']['first-name'] + ' ' + data['personal']['last-name']
    return conv_dict, data

def get_inp(conv_dict,data, inp):
    cat, typ, num = conv_dict[inp][0], conv_dict[inp][1], conv_dict[inp][2]
    conv_dict[inp][2] += 1
    if typ == 'personal' or typ =='education':
        if cat not in data[typ]:
            return ""
        return data[typ][cat]
    elif typ == 'experience':
        if num not in data[typ] or cat not in data[typ][num]:
            return ""
        return data[typ][num][cat]
    
def postprocess(inps, u_data, tags):
    conv_dict, u_data = convert(u_data)
    for i in range(len(inps)):
        prev_exps = ['Job Title','company name']
        prev_ed = ['']
        if inps[i] in ['starting From or start date']:
            if inps[i-1] in prev_exps or inps[i-2] in prev_exps or inps[i-3] in prev_exps:
                inps[i] = inps[i] + ' ' + 'exps'
            elif inps[i-1] in prev_ed or inps[i-2] in prev_ed or inps[i-3] in prev_ed:
                inps[i] = inps[i] + ' ' + 'educ'
        elif inps[i] in ['end date']:
            if inps[i-2] in prev_exps or inps[i-3] in prev_exps or inps[i-4] in prev_exps:
                inps[i] = inps[i] + ' ' + 'exps' 
            elif inps[i-2] in prev_exps or inps[i-3] in prev_exps or inps[i-4] in prev_exps:
                # end date is changed to graduation
                #inps[i] = 'graduation' + ' ' + 'educ'
                inps[i] = 'graduation'
        elif inps[i] in ['location or Address']:
            if inps[i-2] in prev_exps or inps[i-3] in prev_exps or inps[i-4] in prev_exps:
                inps[i] = inp[i] + ' ' + 'exps'
            else:
                inps[i] = inp[i] + ' ' + 'pers'
        elif inps[i] in ['year']:
            if inps[i-1] in ['starting From or start date exps']:
                inps[i-1] = inps[i-1] + ' ' + 'month'
                inps[i] = 'starting From or start date exps' + ' '+ 'year'
            elif inps[i-1] in ['end date exps']:
                inps[i-1] = inps[i-1] + ' ' + 'month'
                inps[i] = 'end date exps'+ ' '+ 'year'
            elif inps[i-1] in ['starting From or start date educ']:
                inps[i-1] = inps[i-1] + ' ' + 'month'
                inps[i] = 'starting From or start date educ' + ' '+ 'year'
            elif inps[i-1] in ['graduation']:
                inps[i-1] = inps[i-1] + ' ' + 'month'
                inps[i] = 'graduation' + ' '+ 'year'
                
            
    num_title = inps.count('Job Title')
    num_name = inps.count('company name')
    num_start = inps.count('starting From or start date exps')
    num_loc = inps.count('end date exps')
    num_exps = num_start if num_start > 0 else num_loc
    
    #changes the first job title or name. If current company asked later then screwed.
    if num_title > num_exps:
        inps[inps.index('Job Title')] = 'Job Title current'
    if num_name > num_exps:
        inps[inps.index('company name')] = 'company name current'
    
#     print(inps)
    result = {}
    for i in range(len(inps)):
        result[i] = ''
        if inps[i] == '' or inps[i] == 'None of the above':
            continue
        user_inp = get_inp(conv_dict, u_data, inps[i])
        print(user_inp)
        if tags[i][0] == 'select':
            if user_inp in tags[i][1]:
                result[i] = tags[i][1].index(user_inp)
        elif tags[i][0] == 'check':
            if user_inp in tags[i][1]:
                result[i] = "true"
        elif tags[i][0] == 'text':
            result[i] = user_inp
    return result

def getall(b_soup):
    data =[]
    val = ""
    for tag in b_soup.find('body').find_all():
        #soup = BeautifulSoup(tag.get_attribute('outerHTML'))
        soup = BeautifulSoup(remove_comments_regexmethod(tag))
        try:       
            text  = soup.find('body').find_all()[0].find(text=True, recursive= False)
            if text and text.strip():
                val = val + " " + text.strip()
        except:
#             print("UNDETECTED")
#             print(soup)
            continue
        soup = soup.find('body').find_all()[0]
        if data and soup.name == 'option':
            data[-1][1].append(val)
            val = ""
        
        
        props = {}
        for i in ['vis','disp','type','value','sel','placeholder']:
            try:
                props[i] = soup[i]
            except:
                props[i] = ''
        vis = props['vis']
        disp = props['disp']
        i_type = props['type']
        value = props['value']
        sel = props['sel']
        placeholder = props['placeholder']
        

        
        if (soup.name in ['input','select','textarea']) and disp != 'none' and vis != 'hidden' and i_type != 'hidden': 
            
            #for input or select boxes that don't get selected due to invicibility fill in the same value as the
            #box above it 
            if placeholder:
                val = val+" " + placeholder
            if val:
#                 print(tag.value_of_css_property('display'),tag.value_of_css_property('visibility'),tag.size,val)
#                 print(tag.tag_name,val)

                if data and data[-1][5] in ['radio','checkbox']:
                    data[-1][1].append(val)
                
                if soup.name == 'textarea':
                    data.append([val,[],value,"", soup.name, i_type, sel])
                    val = ""
                    continue
                if soup.name == 'select':
                    data.append([val,[],value,"",soup.name, i_type, sel])
                    val=""
                    continue
                try:
                    if i_type != 'hidden':
                        data.append([val,[],value,"",soup.name, i_type, sel])
                except:
                    continue
                
                val = ""
            else:
                if i_type != 'hidden'and soup.name == 'select':
                    data.append([data[-1][0],data[-1][1],value,"",soup.name, i_type, sel])
                elif i_type != 'hidden' and soup.name == 'input' and data[-1][-3] == 'input':
                    #print(data[-1],soup.name,i_type)
                    data.append([data[-1][0],data[-1][1],value,"",soup.name, i_type, sel])
                else:
                    data.append(["",[],"","","","",""])
#             print(tag.tag_name)

#         print(soup.find('body'))
#         i+=1
#         if i ==10:
#             break
        
    return data

def text_preprocess(ds: pd.Series) -> pd.Series:
    """
    Apply NLP Preprocessing Techniques to the reviews.
    """
    for m in range(len(ds)):
        main_words = ds[m]
        #main_words = re.sub('[^a-zA-Z]', ' ', ds[m])                                      # Retain only alphabets
        main_words = (main_words.lower()).split()
        main_words = [w for w in main_words if not w in set(stopwords.words('english'))]  # Remove stopwords
        
        lem = WordNetLemmatizer()
        main_words = [lem.lemmatize(w) for w in main_words if len(w) > 1]                 # Group different forms of the same word
        
        main_words= main_words[:10]
        
        main_words = ' '.join(main_words)
        ds[m] = main_words
    return ds

categories = [['Age Group',['18-29',
 '30-49',
 '50 or older'
]],
 ['Ethnicity',[
 'white',
 'hispanic',
 'black',
 'asian',
 'hawaiian',
 'native american',
 'middle eastern',
 'some other race, ethnicity, or origin',
 'two or more'
]],
 ['Gender',['woman',
 'man',
 'lgbt'
]],
['other',[
 'yes',
 'no',
 '',
 'i prefer not to say'
]],
 ['degree',[
 'bachelors',
 'masters',
 'phd'
 ]],
 
 ['Current',[
 'currently work here'
 ]],
 
 ['Gender',[
 'male',
 'female'
]],
 ['Country',[
 'afghanistan',
 'aland',
 'albania',
 'algeria',
 'american samoa',
 'argentina',
 'armenia',
 'australia',
 'austria',
 'belarus',
 'belgium',
 'belize',
 'brazil',
 'british indian ocean territory',
 'canada',
 'china',
 'cuba',
 'egypt',
 'finland',
 'france',
 'germany',
 'ghana',
 'greece',
 'greenland',
 'haiti',
 'hong kong',
 'hungary',
 'iceland',
 'independent state of samoa',
 'india',
 'indonesia',
 'iran (islamic republic of)',
 'iraq',
 'ireland',
 'israel',
 'italy',
 'jamaica',
 'japan',
 'jersey',
 'jordan',
 'kuwait',
 'mexico',
 'myanmar',
 'new zealand',
 'norway',
 'oman',
 'pakistan',
 'palau',
 'saudi arabia',
 'scotland',
 'senegal',
 'serbia - inactive use srb',
 'seychelles',
 'sierra leone',
 'singapore',
 'slovakia',
 'slovenia',
 'solomon islands',
 'somalia',
 'south africa',
 'south sudan',
 'spain',
 'sri lanka',
 'sudan',
 'switzerland',
 'thailand',
 'turkey',
 'ukraine',
 'united arab emirates',
 'united kingdom',
 'united republic of tanzania',
 'united states',
 'united states minor outlying',
 'uruguay',
 'uzbekistan',
 'yemen',
 'yugoslavia',
 'zambia',
 'zimbabwe',
 'georgia',
 "korea, democratic people's rep",
 'korea, republic of',
 'other',
 'russian federation',
 'samoa',
 'united states minor outlying islands',
 'viet nam',
 'iran',
 'korea',
 'laos',
 'u.s. outlying islands',
 'u.s. virgin islands',
 'vatican city',
 'aland islands']],
 ['month',[
 'january',
 'february',
 'march',
 'april',
 'may',
 'june',
 'july',
 'august',
 'september',
 'october',
 'november',
 'december',
]],
 ['year',[
 '2021',
 '2020',
 '2019',
 '2018',
 '2017',
 '2016',
 '2015',
 '2014',
 '2013',
 '2012',
 '2011',
 '2010',
 '2009',
 '2008',
 '2007',
 '2006',
 '2005',
 '2004',
 '2003',
 '2002',
 '2001',
 '2000',
 '1999',
 '1998',
 '1997',
 '1996',
 '1995',
 '1994',
 '1993',
 '1992',
 '1991',
 '1990',
 '2022',
 '2023',
 '2024',
 '2025',
 '2026',
 '2027',
 '2028',
 '2029',
 '2030',
 '2031']],
 ['educ status',[
 'graduated',
 'now attending',
 'incomplete']],
 
 ['State',[
 'alabama',
 'alaska',
 'arizona',
 'arkansas',
 'armed forces america',
 'armed forces europe',
 'armed forces pacific',
 'california',
 'colorado',
 'connecticut',
 'delaware',
 'florida',
 'hawaii',
 'idaho',
 'illinois',
 'indiana',
 'iowa',
 'kansas',
 'kentucky',
 'louisiana',
 'maine',
 'maryland',
 'massachusetts',
 'michigan',
 'minnesota',
 'mississippi',
 'missouri',
 'montana',
 'nebraska',
 'nevada',
 'new hampshire',
 'new jersey',
 'new mexico',
 'new york',
 'north carolina',
 'north dakota',
 'ohio',
 'oklahoma',
 'oregon',
 'pennsylvania',
 'rhode island',
 'south carolina',
 'district of columbia',
 'south dakota',
 'tennessee',
 'texas',
 'utah',
 'vermont',
 'virginia',
 'washington',
 'washington, dc',
 'west virginia',
 'wisconsin',
 'wyoming']],
 ['School or University',[
 'university of california berkeley']],
 ['Do you have any disabilities',[
 'yes disability',
 'no disability']],
 ['Are you a protected veteran',[
 'yes veteran',
 'no veteran']],
 ['phone loc', [
 'home',
 'work'
 ]]]