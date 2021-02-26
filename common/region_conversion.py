def us_state_convert():
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }
    abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))
    return us_state_abbrev, abbrev_us_state


def us_state_abbreviations_list():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return states

def us_state_names_list():
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
     "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
     "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
     "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
     "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
     "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
     "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
     "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    return states


def cn_state_abbreviations_list():
    states = ['ZH', 'XI', 'HD', 'DB', 'HK','XN']
    return states

def cn_state_names_list():
    states = ['Zhongnan', 'Xibei', 'Huadong', 'Dongbei', 'Hong Kong', 'Xinan']
    return states


def cn_state_convert():
    cn_state_abbrev = {
        'Zhongnan': 'ZH',
        'Xibei': 'XI',
        'Huadong': 'HD',
        'Dongbei':  'DB',
        'Hong Kong': 'HK',
        'Xinan': 'XN'


    }
    abbrev_cn_state = dict(map(reversed, us_state_abbrev.items()))
    return cn_state_abbrev, abbrev_cn_state