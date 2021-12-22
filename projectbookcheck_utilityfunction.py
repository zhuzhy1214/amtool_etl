#Utility Function 
import re
import numpy as np

def regulate_EFIS(EFIS):
    #check if is all numerical
    #convert to 10-digit string
    if isinstance(EFIS, str) and EFIS.strip()[0] == "'":
        EFIS = EFIS[1:]
    try: 
        return "{:10.0f}".format(float(EFIS))
    except: 
        return 0


def fiscalyear(dt):
    
    '''
    input: datetime
    
    if today is before june 30 2021, fiscalyear(today) = 21
    if today is after july 1 221, fiscalyear(today) =22
    '''

    if dt <= datetime.strptime('06-30-{}'.format(dt.year), "%m-%d-%Y"):
        return dt.year
    else:
        return dt.year + 1




#data cleaning functions
def remove_punction(string):
    string = string.strip()
    if string != '' and string[0] == "'":
        string = string[1:]
    return string


def curreny_to_float(input_string):
#     print(type(input_string))
    if isinstance(input_string,str) :
        #Question: ?($577691.00) means -$577691.00?
        input_string = re.sub(r'\((.*?)\)', r'-\1', input_string)
        input_string = re.sub(r'\$', '', input_string)
        input_string = input_string.replace(',', '')
        return float(input_string)
    else:
        return float(input_string)

def FY_cleanup(FY):
    temp = re.split('[-/]', FY)
    if int(temp[0]) < 2000: temp[0] = str(int(temp[0])+ 2000)
    return '/'.join(temp)



#data augmentation functions

def calc_unique_EA(df):
    if pd.isnull(df['District']) or pd.isnull(df['EA']) or df['District'] =='' or df['EA'] == '':
        return ''
    else:
        return str(df['District']) + '_' + df['EA'].upper()

    
# Section to Use


# If(ISNull([CCA Date Miilestone (M600)])) Then
#     (If(ISNull([PCR SHOPP Amendment Date])) Then
#         (IF(ISNULL([EFIS Programmed Projects]) and isnull([SHOPP Amendment Date])) Then
#             (If(ISNULL([Long Lead])) Then
#                 (IF(ISNULL([Resourced In PID WP]) 
#                     or isnull([Requested RTL FY]) 
#                     or isnull ([Dist Dir Appr]) 
#                     or Isnull([PID Uploaded])) Then 
#                      'TYP' 
#                  Else 
#                      'PRG' 
#                  End)
#             ElseIF(ISNULL([Resourced In PID WP]) 
#                    Or isnull([LL RTL FY PRG]) 
#                    or isnull ([Dist Dir Appr]) 
#                    or Isnull([PID Uploaded])) Then 
#                  'TYP' 
#             Else 
#                  'PRG' 
#             End)
#         Else
#              'PRG' 
#         End)
#     ELSE 
#          'PPC'
#     END)
# ELSE 
#     'CCA'
# END


#     #question: 
#     # Project could only have part of the information, such as 22764, hence be categorized as TYP. ==> use 'Section In Use'

def cal_section_in_use(df):
    if pd.notnull(df['CCA Date Miilestone (M600)']):
        return 'CCA'
    elif pd.notnull(df['PCR SHOPP Amendment Date']):
        return 'PPC'
    else:
        if pd.isnull(df['SHOPP Amendment Date']) and pd.isnull(df['EFIS_Program']): 
            if pd.isnull(df['Long Lead']):
                if(pd.isnull(df['Resourced In PID WP'])
                    or pd.isnull(df['Requested RTL FY'])
                    # or df['Requested RTL FY Number'] == 0 # the missing information for this column is already filled with zero
                    or pd.isnull(df['Dist Dir Appr'])
                    or pd.isnull(df['PID Uploaded'])):
                    return 'TYP'
                else:
                    return 'PRG'
            else: # for long lead project
                if (pd.isnull(df['Resourced In PID WP'])
                    or pd.isnull(df['Requested RTL FY'])
                    # or df['Requested RTL FY Number'] == 0 # the missing information for this column is already filled with zero
                    or pd.isnull(df['LL RTL FY PRG'])
                    or pd.isnull(df['Dist Dir Appr'])
                    or pd.isnull(df['PID Uploaded'])):
                    return 'TYP'
                else:
                    return 'PRG'
            
        else:
            return 'PRG'

def county_to_use(df):
    if df['Section'] == 'TYP':
        return df['County TYP']
    elif df['Section']  == 'PRG':
        return df['County PRG']
    elif df['Section']  == 'PPC':
        return df['County PCR']
    elif pd.isnull(df['PCR SHOPP Amendment Date']): 
        return df['County PRG']
    else:
        return df['County PCR']

def route_to_use(df):
    if df['Section'] == 'TYP':
        return df['Route TYP']
    elif df['Section'] == 'PRG':
        return df['Route PRG']
    elif pd.isnull(df['PCR SHOPP Amendment Date']): 
        return df['Route PRG']
    else:
        return df['Route PCR']

def beginPM_to_use(df):
    if df['Section'] == 'TYP':
        return df['BackPM TYP']
    elif df['Section'] == 'PRG':
        return df['BackPM PRG']
    elif df['Section'] == 'PPC':
        return df['BackPM PCR']
    elif df['Section'] == 'CCA':
        return df['CCA BackPM']
    else:
        return df['BackPM PRG']

def endPM_to_use(df):
    if df['Section'] == 'TYP':
        return df['AheadPM TYP']
    elif df['Section'] == 'PRG':
        return df['AheadPM PRG']
    elif df['Section'] == 'PPC':
        return df['AheadPM PCR']
    elif df['Section'] == 'CCA':
        return df['CCA AheadPM']
    else:
        return df['AheadPM PRG']
        
def calc_activity_group(Activity):
    
    if Activity in [
                'Major Damage - Permanent Restoration',
                'Major Damage - Emergency Opening',   
                'Safety - SI', 
                'Safety - Monitoring',
                'Relinquishment', 
                'Reactive Safety',
                'Bridge - Deck',
                    ]:
        return 'Reservation'
    
    else:
        return Activity

def calc_SB1(Activity):
    if Activity in ['Bridge', 'Bridge - Health', 'Bridge - Deck','Pavement','Drainage', 'Mobility - TMS',]:
        return 'Yes'
    else:
        return ' '


def calc_activity_book(Activity):

    if Activity =='Advance Mitigation/Mitigation':
        return 'Advance Mitigation'
    
    elif Activity in ['Bridge', 'Bridge - Health']:
        return 'Bridge'
    elif Activity in ['Facilities', 'Facilities - Office Buildings']:
        return 'Facilities'
    elif Activity in ['Safety - SI', 'Safety - Monitoring']:
        return 'Safety Improvements'
    if Activity =='Sustainability/Climate Change':
        return 'Sustainability'
    else:
        return Activity


# AM Tool RTL (Section in Use)


# cal ='''
# IF(ISNULL([Long Lead])) THEN
#     (IF ([Section to Use]='TYP') THEN [Target RTL FY] 
#     ELSEIF([Section to Use]='PRG') THEN [Requested RTL FY]
#     ELSEIF([Section to Use]='PPC') THEN [PCR RTL]
#     ELSEIF Isnull ([PCR SHOPP Amendment Date]) then [Requested RTL FY]
#     ELSE [PCR RTL]
#     END)
# ELSEIF([Section to Use]='TYP') THEN [LL RTL FY TYP]
# ELSEIF([Section to Use]='PRG') THEN [LL RTL FY PRG]
# ELSEIF([Section to Use]='PPC') THEN [PCR RTL]
# ELSEIF Isnull ([PCR SHOPP Amendment Date]) then [LL RTL FY PRG]
#     ELSE [PCR RTL]
#     END
# '''


def calc_SIU_RTL(df):
    
# def get_count_to_use(SectionToUse, County_TYP, COUNTY_PRG, COUNTY_PCR, COUNTY_CCA):
#     county_dict= {'TYP': County_TYP, 'PRG':COUNTY_PRG, 'PCR':COUNTY_PCR, 'CCA':COUNTY_CCA}
#     return county_dict[SectionToUse]
    
    if pd.isnull(df['Long Lead']):
        if df['Section']=='TYP':
            return df['Target RTL FY'] 
        elif df['Section']=='PRG':
            return df['Requested RTL FY']
        elif df['Section']=='PPC':
            return df['PCR RTL']
        elif pd.isnull(df['PCR SHOPP Amendment Date']):
            return df['Requested RTL FY']
        else:
            return df['PCR RTL']
    else:
        if df['Section']=='TYP':
            return df['LL RTL FY TYP']
        elif df['Section']=='PRG':
            return df['LL RTL FY PRG']    
        elif df['Section']=='PPC':
            return df['PCR RTL']  
        elif pd.isnull (df['PCR SHOPP Amendment Date']):
            return df['LL RTL FY PRG'] 
        else:
            return df['PCR RTL'] 

# PA&ED FY


# cal ='''

# IF(ISNULL([Long Lead])) THEN 0
# ELSEIF([Section to Use]='TYP') THEN Float(Right([Target RTL FY],2))
# ELSEIF([Section to Use]='PRG') THEN Float(Right([Requested RTL FY],2))
# ELSE  0
# END
# '''



def calc_PAED_FY(df):
    if pd.isnull(df['Long Lead']) : 
        return 0
    elif df['Section'] == 'TYP':
        return df['Target RTL FY Number']
    elif df['Section'] == 'PRG':
        return df['Requested RTL FY Number']
    else:
        return 0

        
def calc_drain_unique_ID(df):
    if pd.isnull(df['SYSNO']) or pd.isnull(df['INETNO']) or pd.isnull(df['OUTETNO']):
        return None
    else:
        return (df['SYSNO'] + "_"+ df['INETNO'] + "_"+ df['OUTETNO'])


#Shopp Tool Cost to use

# cal ='''
# IF(ISNULL([Long Lead])) THEN
#     (
#     IF ([Section to Use]='TYP') THEN [TYP Total Project Cost ($K)] 
#     ELSEIF([Section to Use]='PRG') THEN [Prog Total Project Cost ($K)] 
#     ELSEIF([Section to Use]='PPC') THEN [PCR Total Cost ($K)]
#     ELSEIf isNull([PCR SHOPP Amendment Date]) Then [Prog Total Project Cost ($K)]
#     Else    [PCR Total Cost ($K)] 
#     END)
# ELSEIF([Section to Use]='TYP') THEN ([TYP Total Project Cost ($K)] + [LL PAED Cost ($K)])
# ELSEIF([Section to Use]='PRG') THEN ([Total LL Prog ($K)]+ [PAED ($K)])
# ELSEIF([Section to Use]='PPC') THEN [PCR Total Cost ($K)]
# ELSEIf isNull([PCR SHOPP Amendment Date]) Then [Total LL Prog ($K)]+ [PAED ($K)]
# Else    [PCR Total Cost ($K)] 
# END
# '''

def calc_SHOPP_tool_cost(df):
    if pd.isnull(df['Long Lead']): #if it is not an active long lead
        if df['Section']=='TYP':
            return df['TYP Total Project Cost ($K)'] 
        elif df['Section']=='PRG':
            return df['Prog Total Project Cost ($K)']
        elif df['Section']=='PPC':
            return df['PCR Total Cost ($K)']
        elif pd.isnull(df['PCR SHOPP Amendment Date']):
            return df['Prog Total Project Cost ($K)']
        else:
            return df['PCR Total Cost ($K)']
    else: #for a long lead project
        if df['Section']=='TYP':
            return df['TYP Total Project Cost ($K)'] + df['LL PAED Cost ($K)']
        elif df['Section']=='PRG':
            return df['Total LL Prog ($K)'] + df['PAED ($K)']
        elif df['Section']=='PPC':
            return df['PCR Total Cost ($K)']
        elif pd.isnull(df['PCR SHOPP Amendment Date']):
            return df['Total LL Prog ($K)']+ df['PAED ($K)']
        else:
            return df['PCR Total Cost ($K)']    

    
    
    
#Total Project Cost ($K)
# cal ='''
# IF(isNULL([EFIS Programmed Projects])) Then [Shopp Tool Cost to use]
# ELSE [Total Capital & Support Cost]
# End
# '''

def calc_total_project_cost(df):
     #may consider join the Total Capital & Support Cost
#     if df_program[df_program['EFIS'] == df['EFIS']].shape[0]>0:
#         return df_program[df_program['EFIS']==df['EFIS']]['Total Capital & Support Cost'].iloc[0]
    if pd.isnull(df['EFIS_Program']):
        return df['Shopp Tool Cost to use']  #calculated value based on AMTool
    else: 
        return df['Total Capital & Support Cost'] # calculated value based on lyle's group
    
    
def calc_unique_pave_ID(df):
    
    return (df['County']
     + '_'+ df['Route']
     + '_'+ ("" if pd.isnull(df['RS']) else df['RS'])
     + '_'+ ("" if pd.isnull(df['BPP']) else df['BPP'])
     + '_'+ str(df['Beg PM'])
     + '_'+ ("" if pd.isnull(df['BPS']) else df['BPS'])
     + '_'+ ("" if pd.isnull(df['EPP']) else df['EPP'])
     + '_'+ str(df['End PM'])
     + '_'+ ("" if pd.isnull(df['EPS']) else df['EPS'])
     + '_'+ ("" if pd.isnull(df['Direction']) else df['Direction'])
     + '_'+ str(0 if pd.isnull(df['Lane']) else df['Lane'])
     + '_'+ '{:.0f}'.format(df['RoadwayClass'])
    )
    
    

def regulate_timestamp_format(dt):
    if dt is np.nan: 
        return np.nan
    else:
        return datetime.strptime(dt, "%m/%d/%y").strftime("%m-%d-%Y")
    
#deck check functions



# Does project cost exceed Minor Program limits ($1,250K)?

# cal ='''
# IF([Planning or Post-Planning]="Post-Planning") Then "OK"
# ELSEIF([Activity]= "Relinquishment") Then "OK"
# ELSEIF([Activity (group)]="Reservation") Then 
#     (IF [Project Cost ($K)]>333 Then "OK" 
#     Else 'Please review project cost, it is below Minor Program limits' 
#     End)
# ELSEIF[Project Cost ($K)]>1250 Then "OK" 
# Else 'Please review project cost, it is below Minor Program limits' 
# END
# '''

def ck_minor_program_limit(df):
    if(df['Planning or Post-Planning']=="Post-Planning"):
        return "OK"
    elif (df['Activity']== "Relinquishment"):
        return "OK"
    elif(df['Activity (group)']=="Reservation"):
        if df['Project Cost ($K)']>333:
            return "OK" 
        else:
            return 'Please review project cost, it is below Minor Program limits' 
    elif df['Project Cost ($K)']>1250:
        return "OK" 
    else:
        return 'Please review project cost, it is below Minor Program limits' 
        
        

#Does project include performance related to each location?


# cal ='''
# If([Will this project be included in the Project Book?]="Yes" and [Multiple Loc]="Y") Then
#     IF([Count Location Performance Raw Data]=[Loc Count]) Then "OK"
#     Else "Detail the performance for each location listed in the performance tab."
#     End
# Else "OK"
# END
# '''

def ck_multiple_location_performance(df):
    if(df['Will this project be included in the Project Book?']=="Yes" and df['Multiple Loc'] == "Y"):
        if df['perf_entry_count'] == df['Loc Count'] : 
            return "OK"
        else: 
            return "Please provide the performance details for all {} locations listed in the performance tab for {} Section.".format(df['perf_entry_count'], df['Section'])
    else: 
        return "OK"


#Is Performance tab Complete?


# cal ='''
# If [Ten-Year Plan RD]=9999 then "OK"
# ElseIf(isnull([Section])) then
# "Please Complete the Performance Tab"
# Elseif({Fixed [SHOPP ID], [Date]: Max([Include in Performance? Numeric])})=1 Then"OK"
# Else "Please Complete the Performance Tab"
# END
# '''

def ck_performance_tab_completed(df):
    if df['Ten-Year Plan RD'] == 9999 : 
        return "OK"
    elif df['perf_entry_count']>0:
        return "OK"
    else: 
        return "Please Complete the Performance Tab"
        
        
#Is at least one performance activities related to the Activity Category of planned project?

# cal ='''
# If [Planning or Post-Planning]="Post-Planning" then "OK" 
# Elseif [Section to Use]=[Section Programming Summary] then 
#      IF { FIXED [SHOPP ID], [Date], [Section Programming Summary]:SUM([Programming Summary Performance Value (No Nulls)])}=0
#                     Then "Please review activities in the performance tab, or the Activity Category of project profile. The performance measure to be reported to CTC is 0."
#                 Else "OK"
#                 END
# Else "OK"
#                 END
# '''



def ck_active_category_performance(df):
    
    '''
    if project is in post-planning, SKIP the check
    if in program summary, same project, same section, no performance value entries is found, FLAG
    else ok
    '''
    
    if df['Planning or Post-Planning'] == "Post-Planning" : 
        #question to be answered: manpaul: we should check the project performance, regardless planning or post-planning.
        return  "OK" 

    elif df['Performance Value Sum'] == 0:
        return  "Please review activities in the performance tab, or the Activity Category of project profile. The performance measure to be reported to CTC is 0."

    else: 
        return "OK"




#Is Long Lead Project Cost and RTL completed and consistent?

# cal ='''

# IF[Long Lead]="Y" and [Ten-Year Plan RD]<>9999 Then
# If [Type of Exception]="Long Lead schedule" then "OK" 
# ElseIF [Section to Use]="TYP" then 
#     If [Last Year of Fiscal Year]-FLOAT(Right([Target RTL FY],2))<4 or isnull ([Last Year of Fiscal Year])
#     or isnull([Target RTL FY]) or isnull([LL PAED Cost ($K)]) or isnull ([TYP Total Project Cost ($K)])
#     Then "Please review PA&ED cost, Long-Lead Cost or PA&ED allocation year and/or Long-Lead RTL. PA&ED allocation year must be 4 or more years before RTL" 
#     Else "OK"
#     End
# ElseIf [Section to Use]="PRG" and Isnull([SHOPP Amendment Date]) then 
#     If [Last Year of Fiscal Year]-Float(Right([Requested RTL FY],2))<4  or isnull ([Last Year of Fiscal Year]) 
#     or isnull([Requested RTL FY])or isnull([PAED ($K)]) or isnull ([Total LL Prog ($K)])
#     Then "Please review PA&ED cost, Long-Lead Cost or PA&ED allocation year and/or Long-Lead RTL. PA&ED allocation year must be 4 or more years before RTL" 
#     Else "OK"
#     End
# Else"OK"
# End
# Else"OK"
# End
# '''

def ck_longlead(df):
    AMT_ID= df['AMT_ID']
    if df['Long Lead'] == "Y" and df['Ten-Year Plan RD']!=9999 :  
        if df['Type of Exception'] == "Long Lead schedule": 
            return "OK" 
        elif df['Section'] == "TYP" :
            if (df['Last Year of Fiscal Year']-df['Target RTL FY']<4 
                    or pd.isnull(df['Last Year of Fiscal Year'])
                    or pd.isnull(df['Target RTL FY']) 
                    or pd.isnull(df['LL PAED Cost ($K)']) 
                    or pd.isnull(df['TYP Total Project Cost ($K)'])): 
                return "Please review PA&ED cost, Long-Lead Cost or PA&ED allocation year and/or Long-Lead RTL. PA&ED allocation year must be 4 or more years before RTL" 
            else: 
                return "OK"

        elif df['Section'] == "PRG" and pd.isnull(df['SHOPP Amendment Date']) : 
            if (df['Last Year of Fiscal Year']-df['Requested RTL FY']<4 
                or pd.isnull (df['Last Year of Fiscal Year']) 
                or pd.isnull(df['Requested RTL FY'])
                or pd.isnull(df['PAED ($K)']) 
                or pd.isnull (df['Total LL Prog ($K)'])): 
                return "Please review PA&ED cost, Long-Lead Cost or PA&ED allocation year and/or Long-Lead RTL. PA&ED allocation year must be 4 or more years before RTL" 
            else: 
                return "OK"
        else:
            return "OK"
    else:
        return "OK"


#Is Drainage Worksheet Complete (2024/25 RTL and after)? 

#Question: what does this mean ['Include in Worksheet']

# cal ='''
# If [Include in Worksheet]="Yes" then
# If(isnull([Drainage ID])and [Last Year of Fiscal Year]>24 
# and [Include in Performance?]="Yes" 
# and Left([Performance Objective],15)="Drainage System")
# Then 'Please complete drainage worksheet'
# Else'OK'
# END
# Else'OK'
# END
# '''

    

def ck_drainage_ws_complete(df):
   
    #check if "Last Year of Fiscal Year" is more than 3 years from now, "OK" if no, check further if yes.
    #check if Performance raw dataset as has an entry with the same ID and STU, 
    #        and performance objective that starts with "Drainage system"
    #if no, "OK"
    #if yes, check if drainage worksheet dataset has an entry with the same ID and STU, FLAG if no, "OK" if yes.
    
    #Questions: can we use dynamic FY instead of fixed number 24
    #mara: keep this a static value of 24
    
    if df['Last Year of Fiscal Year'] <= 24:
        return 'OK'
    else:
        AMT_ID = df['AMT_ID']
        section_to_use = df['Section']  
            #potentially slow down the process, conduct join with additional column: performance has drainage?
            #question to be answered: of the entire dataset of df_perf_raw_data, there is no instance of "Drainage system ..."
        drainage_in_performance = df_perf_raw_data[(df_perf_raw_data['AMT_ID'] == AMT_ID) 
                                                   & (df_perf_raw_data['Section']==section_to_use )
                                                   & (df_perf_raw_data['Performance Objective'].str[:15] == 'Drainage system')].shape[0] > 0
        if not drainage_in_performance:
            return 'OK'
        else: 

            if df['No of Drainage Entries'] > 0:
                return 'OK'
            else:
                return 'Please complete drainage worksheet'
            
 #Are all conditions selected for bridge replacements?


# cal ='''
# IF [Ten-Year Plan RD]<> 9999 and [Last Year of Fiscal Year]>24 then
#     IF [Section Bridge worksheet]=[Section to Use] Then
#     IF isnull([Bridge №]) then "OK"
#         ElseIF [Work Type]="Replacement" Then 
#             If Isnull ([Conditions Bridge / Tunnel Health Pre]) Or Isnull([Conditions Bridge Gds Mvmt Pre]) or isnull([Conditions Bridge Scour Pre]) or Isnull ([Conditions Bridge Seismic Pre]) 
# or (ifnull([Bridge Rail Good (lf)],0)+IFNULL([Bridge Rail Fair (lf)],0)+ifnull([Bridge Rail Poor (lf)],0))=0 
#             Then "Please review Bridge Worksheet. Bridge Replacement should select the condition for Health, Scour, Seismic, Goods and Rail"
#             Else "OK"
#             END
# Else "OK"
#    END
# Else "OK"
# END
# Else "OK"
# END
# '''


def ck_bridge_data_completeness(df):
    
    if df['Ten-Year Plan RD'] != 9999 and df['Last Year of Fiscal Year'] > 24 :  
        AMT_ID = df['AMT_ID']
        STU = df['Section']

        temp = df_brg_raw_data[(df_brg_raw_data['AMT_ID'] == AMT_ID) 
                        & (df_brg_raw_data['Section'] == STU)
                        & (df_brg_raw_data['WorkType'] == 'Replacement')][[
                        'Health Pre',
                        'Scour_Pre',
                        'Seismic_Pre', 
                        'GdsMvmt_Pre',
                        'Rail_Total(lf)']]
        if temp.shape[0] == 0:
            return 'OK'
    
        elif ((temp[['Health Pre',
                        'Scour_Pre',
                        'Seismic_Pre', 
                        'GdsMvmt_Pre',]].isnull().sum().sum() > 0) 
                or (temp['Rail_Total(lf)'].min() == 0)):
                return  "Please review Bridge Worksheet. Bridge Replacement should select the condition for Health, Scour, Seismic, Goods and Rail"
        else:
            return 'OK'
    else: return "OK"
     
#Does the Plan Year in the Pavement Worksheet match the Project RTL?


# cal ='''
# If [Include in Worksheet]="Yes" and [Last Year of Fiscal Year]<30 then
# If(isnull([Plan Year])) then "OK"
# ElseIf [Last Year of Fiscal Year]+2000<2016 and [Plan Year]=2016 then "OK"
# ElseIf([Plan Year]=[Last Year of Fiscal Year]+2000 and [Pavement Section]=[Section to Use])
# Then "OK"
# Else "Please review Pavement Worksheet Plan Year. It does not match the project RTL."
# END
# ElSe "OK"
# End
# '''

def ck_pavement_ws_plan_year_RTL(df):

    if df['Last Year of Fiscal Year']<30 :    
        if(pd.isnull(df['Pavement Plan Years'])) : 
            return  "OK"
        elif df['Last Year of Fiscal Year']+2000<2016 and 2016 in df['Pavement Plan Years'] : 
            #question to be answered: should be this logic or all pavement plan years be within 2015 and 2016?
            return  "OK"
        elif(df['Last Year of Fiscal Year']+2000 in df['Pavement Plan Years']): 
            return  "OK"
        else: 
            return "Please review Pavement Worksheet Plan Year. It does not match the project RTL."
    else: 
        return "OK"

#Is Pavement Worksheet Complete (2024/25 RTL and after)?


# cal ='''
# If [Include in Worksheet]="Yes" then
# If(isnull([Plan Year])and [Last Year of Fiscal Year]>24 and [Last Year of Fiscal Year]<31 
#and [Include in Performance?]="Yes" and Left([Performance Objective],8)="Pavement")
# Then 'Please complete pavement worksheet'
# Else'OK'
# END
# Else'OK'
# END
# '''


def ck_pav_ws_complete(df):
    
    #updated logic
    # if ['Performance Objective has Pavement'] == 'Yes', 
    #if last fiscal year is exclusively between 24 and 31, 
    # and pavement worksheet has a plan year matching last fiscal year, 
    # and performance worksheet has an entry of same project ID and section, and Performance Objective starting with 'Pavement'
    # Question: can we make the logic more specific and reading friendly 
    # df_perf_raw_data['Performance Objective'] in ['Pavement Class I','Pavement Class II','Pavement Class III']
    
    if(pd.isnull(df['Pavement Plan Years'])) : #if found plan year, means there is an entry in pavement worksheet
        if df['Performance Objective has Pavement'] == 'Yes':
            return  'Please complete pavement worksheet'
        else:
            return  "OK"
    else:
        #There is no missing data issue for PavementWorksheet_Plan Year:  df_pav_raw_data['Plan Year'].unique()
        if(df['Last Year of Fiscal Year']>24 and df['Last Year of Fiscal Year']<31 
           and not (df['Last Year of Fiscal Year'] + 2000 in df['Pavement Plan Years']) #question to be answered: check this logic
           and df['Performance Objective has Pavement'] == 'Yes'): 
            return  'Please complete pavement worksheet'
        else: return 'OK'




#data publish functions

import urllib.request
from datetime import datetime
from pathlib import Path

# key configuration to publish the data source (do not share this config.py)
# from python_scripts import config
import config

import pandas as pd
# Rest API to publish hyper to tableau server
import tableauserverclient as TSC

# third party module to create tableau hyper file from pandas dataframe
from pandleau import *


def publish_datasource(df, hyper_name):
    #IMPORTANT: tableau limit the number of columns in one extract to be 128. 
    
    #remove the local hyper file
    # try :
        # print('deleting existing hyper file...')
        # os.remove(hyper_name)
    # except:
        # pass
    
    df_tab = pandleau(df)
    df_tab.to_tableau(hyper_name, 'Extract',
                      add_index=False)  # must name the table to be "EXTRACT" to publish the hyper file to server

    tableau_auth = TSC.PersonalAccessTokenAuth(token_name=config.token_name, personal_access_token=config.token_value,
                                               site_id=config.site_name)
    server = TSC.Server(config.server_address, use_server_version=True)

    path_to_database = Path(hyper_name)

    
    print(f"Signing into {config.site_name} at {config.server_address}")
    with server.auth.sign_in(tableau_auth):
        # Define publish mode - Overwrite, Append, or CreateNew
        publish_mode = TSC.Server.PublishMode.Overwrite

        # Get project_id from project_name
        all_projects, pagination_item = server.projects.get()
        for project in TSC.Pager(server.projects):
            if project.name == config.project_name:
                project_id = project.id

        # Create the datasource object with the project_id
        datasource = TSC.DatasourceItem(project_id)

        print(f"Publishing {hyper_name} to {config.project_name}...")
        # Publish datasource
        datasource = server.datasources.publish(datasource, path_to_database, publish_mode)
        
        
        # print("Datasource published. Datasource ID: {0}".format(datasource.id))
        # print("Datasource published. Datasource Name: {0}".format(datasource.name))

        return "Datasource published. Datasource Name: {0}".format(datasource.name)



def export_data(df_out, filename, PROJECTBOOKCHECK_HTTPSEVER_FOLDER, LOG_FILE):
    file_export_log = open(LOG_FILE, "a")  # append mode
    file_export_log.write("#####{} \n".format(datetime.now().strftime("%m-%d-%Y, %H:%M")))
    
    try: 
        df_out.to_csv('.\output\{}.csv'.format(filename), index= False)
        shutil.copy('.\output\{}.csv'.format(filename), '{}\{}.csv'.format(PROJECTBOOKCHECK_HTTPSEVER_FOLDER, filename))
        file_export_log.write("Succeeded: {} \n".format('{}\{}.csv'.format(PROJECTBOOKCHECK_HTTPSEVER_FOLDER, filename)))
    except:
        file_export_log.write("Failed: {} \n".format('{}\{}.csv'.format(PROJECTBOOKCHECK_HTTPSEVER_FOLDER, filename)))


    hyper_name = r'{}.hyper'.format(filename)

    try: 
        publish_datasource(df_out, hyper_name)
        file_export_log.write("Succeeded: {} \n".format('{}'.format(hyper_name)))
    except:
    #     print('error')
        file_export_log.write("Failed: {} \n".format('{}'.format(hyper_name)))
        
    file_export_log.close()    
    
