"""
"""
import os 
import numpy as np
import pandas as pd

import utils
# import utils_fund
# import filter_items_status

# Setup the global values
LOCATION = "LOCATION"
MEDIA = "MEDIA"
ITEM = "ITEM"
MAGAZINE = "MAGAZINE"
CALLNUMBER = "CALL NUMBER"
STATUSDATE = "STATUSDATE"

Sub_callnumber = "Sub_callnumber"

Excluded_locations = ["LIBRARY OF THINGS", "Technical Equipment", 
                      "LIBRARY OPERATIONS", "HotSpot", 
                      "HOTSPOT EXPRESS", "Chromebook", 
                      "HOTSPOT FOUR WEEKS", "Google Chromebook", 
                      "Experience Pass", "CATALOGING", 
                      "INTERLIBRARY LOAN", "MISCELLANEOUS"]

Excluded_medias = ["Tablet", "MICROFORM", "VIDEO RECORDINGS", 
                   "CASSETTES", "LIBRARY OF THINGS"]

Excluded_callnumber = ["TAX", "OKTAX"]

Exceptional_keywords = ["0.*", "1.*", "2.*", "3.*", "4.*", 
                        "5.*", "6.*", "7.*", "8.*", "9.*", 
                        "Y0.*", "Y1.*", "Y2.*", "Y3.*", "Y4.*", 
                        "Y5.*", "Y6.*", "Y7.*", "Y8.*", "Y9.*",
                        "J0.*", "J1.*", "J2.*", "J3.*", "J4.*", 
                        "J5.*", "J6.*", "J7.*", "J8.*", "J9.*",
                        "OK 0.*", "OK 1.*", "OK 2.*", "OK 3.*", 
                        "OK 4.*", "OK 5.*", "OK 6.*", "OK 7.*", 
                        "OK 8.*", "OK 9.*", "R 0.*", "R 1.*", 
                        "R 2.*", "R 3.*", "R 4.*", "R 5.*", 
                        "R 6.*", "R 7.*", "R 8.*", "R 9.*"]


######################## Filter the unnecessary items #######################

def remove_unnecesary_items(data, locations=Excluded_locations, medias=Excluded_medias, 
                            callnumber=Excluded_callnumber):
    """
    This function is to remove the unnecessary items based on their locations and medias
    """
    # Remove items based on their locations
    df = utils_fund.remove_excluded_locations(data, locations)
    df = utils_fund.remove_excluded_callnumber(df, callnumber)

    # Remove items based on their medias
    return utils_fund.remove_excluded_medias(df, medias)


######################## Filter the Periodicals items #######################

def filter_periodicals_items(data: pd.DataFrame) -> pd.DataFrame:
    """
    This function is to filter only Periodicals items including 
    `Magazine` items in their Locations and `Periodicals` in their Media
    Input:
        data: dataframe contains items info
    Output:
        a dataframe contains only the periodicals items
    """
    return data[(data[MEDIA].isin(["PERIODICALS"])) | (data[LOCATION].isin(["MAGAZINE"]))]


######################## Filter the AMP items #######################

def filter_AMP_items(data: pd.DataFrame) -> list[pd.DataFrame]:
    """
    This function is to filter Audio Player - AMP items
    Input: 
        - data: dataframe contains items info
    Output:
        - results: dataframe contains filtered AMP items
        - data: a list of dataframes contains all the left items    
    """
    # Filter only `Audio Player` items
    amp = data[data[MEDIA] == "AUDIO PLAYER"]

    # Define the keywords for each fund

    j_media = ["JFICTION*", "JMYSTERY*", "JSCIENCE*",
               "J FICTION*", "J MYSTERY*", "J SCIENCE*",
               "JSPORTS*", "J SPORTS*"]
    a_media = ["FICTION*", "MYST*", "SCIENCE FIC*", "WESTERN*", "SHORT STORY*"]
    c_media = ["EASY *", "READER*", "TWEEN*", "BOARD*", 
                 "J0.*", "J1.*", "J2.*", "J3.*", "J4.*", 
                 "J5.*","J6.*", "J7.*", "J8.*", "J9.*"]
    y_media = ["YFICTION*", "YSCIENCE*",
                 "Y0.*", "Y1.*", "Y2.*", "Y3.*", "Y4.*", 
                 "Y5.*", "Y6.*", "Y7.*", "Y8.*", "Y9.*"]
    media_1 = ["1.*", "3.*", "6.*", "9.*",]
    media_2 = ["0.*", "2.*", "4.*", "5.*", "7.*", "8.*"]  

    # Filter items belong to `AMP-J` fund
    amp_j = amp[amp[CALLNUMBER].isin(j_media)]
    # Filter items left
    amp = amp[~amp[ITEM].isin(amp_j[ITEM])]
    data = data[~data[ITEM].isin(amp_j[ITEM])]

    # Filter items belong to `AMP-A` fund
    amp_a = amp[amp[amp[CALLNUMBER].isin(a_media)]]
    # Filter items left
    amp = amp[~amp[ITEM].isin(amp_a[ITEM])]
    data = data[~data[ITEM].isin(amp_a[ITEM])]

    # Added Sub_callnumber column
    amp[Sub_callnumber] = utils_fund.split_string_value(amp[CALLNUMBER])

    # Filter items belong to `AMP-C` fund
    amp_c = amp[amp[CALLNUMBER].isin(c_media)]

    amp_c_subset = utils_fund.filter_items_by_keywords(amp, Sub_callnumber, c_media)
    amp_c = pd.concat([amp_c, amp_c_subset], ignore_index=True).reset_index(drop=True)
    amp_c = amp_c.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)

    # Filter items left
    amp = amp[~amp[ITEM].isin(amp_c[ITEM])]
    data = data[~data[ITEM].isin(amp_c[ITEM])]

    # Filter items belong to `AMP-Y` fund
    amp_y = amp[amp[CALLNUMBER].isin(y_media)]

    amp_y_subset = utils_fund.filter_items_by_keywords(amp, Sub_callnumber, y_media)
    amp_y = pd.concat([amp_y, amp_y_subset], ignore_index=True).reset_index(drop=True)
    amp_y = amp_y.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)

    # Filter items left
    amp = amp[~amp[ITEM].isin(amp_y[ITEM])]
    data = data[~data[ITEM].isin(amp_y[ITEM])]

    # Filter items belong to `AMP-1` fund
    amp_1 = amp[amp[CALLNUMBER].isin(media_1)]
    amp_1_subset = utils_fund.filter_items_by_keywords(amp, Sub_callnumber, media_1)
    amp_1 = pd.concat([amp_1, amp_1_subset], ignore_index=True).reset_index(drop=True)
    amp_1 = amp_1.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)

    # Filter items left
    amp = amp[~amp[ITEM].isin(amp_1[ITEM])]
    data = data[~data[ITEM].isin(amp_1[ITEM])]

    # Filter items belong to `AMP-2` fund
    amp_2 = amp[amp[CALLNUMBER].isin(media_2)]
    amp_2_subset = utils_fund.filter_items_by_keywords(amp, Sub_callnumber, media_2)
    amp_2 = pd.concat([amp_2, amp_2_subset], ignore_index=True).reset_index(drop=True)
    amp_2 = amp_2.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)

    # Filter items left
    amp = amp[~amp[ITEM].isin(amp_2[ITEM])]
    data = data[~data[ITEM].isin(amp_2[ITEM])]

    return data, amp_1, amp_2, amp_a, amp_c, amp_j, amp_y


######################## Filter the AEB items #######################

def filter_AEB_items(data: pd.DataFrame) -> list[pd.DataFrame]:
    """
    """
    # Filter items that are `Audio Enabled Book`
    aeb = data[data[MEDIA] == "AUDIO ENABLED BOOK"]
    
    j_media = ["JFICTION*", "JMYSTERY*", "JSCIENCE*", "JSPORTS*",
               "J FICTION*", "J MYSTERY*", "J SCIENCE*", "J SPORTS*",]
    
    c_media = ["EASY *", "READER*", "TWEEN*", "BOARD*",
               "J0.*", "J1.*", "J2.*", "J3.*", "J4.*", 
               "J5.*", "J6.*", "J7.*", "J8.*", "J9.*"]
    
    # Filter items belong to `AEB-J` fund
    aeb_j = aeb[aeb[CALLNUMBER].isin(j_media)]

    # Filter only left items
    data = data[~data[ITEM].isin(aeb_j[ITEM])]

    aeb = aeb[~aeb[ITEM].isin(aeb_j[ITEM])]

    # Filter items belong to `AEB-C` fund
    aeb_c = aeb[aeb[CALLNUMBER].isin(c_media)]

    # Filter only left items
    data = data[~data[ITEM].isin(aeb_c[ITEM])]

    return data, aeb_j, aeb_c


######################## Filter the CD-Rom items #######################

def filter_CD_ROM_items(data: pd.DataFrame) -> list[pd.DataFrame]:
    """
    This function is to filter all CR-Rom items
    """
    # Filter items belong to `CDM-A` fund
    cdm_a = data[data[LOCATION].isin(["MUSIC", "JUVENILE MUSIC"])]
    data = data[~data[ITEM].isin(cdm_a[ITEM])]

    # Filter other items for CD-Rom
    cd_rom = data[data[MEDIA].isin(["CD-ROM"])]
    
    c_callnumber = ["EASY *", "READER*", "TWEEN*", "BOARD*"]

    j_callnumber = ["JFICTION*", "JMYSTERY*", "JSCIENCE*", "JSPORTS*", "JMUSIC*",
                    "J FICTION*", "J MYSTERY*", "J SCIENCE*", "J SPORTS*",]
    
    f_callnumber = ["YFICTION*", "YSCIENCE*",
                    "FICTION*", "MYST*", "SCIENCE FIC*", 
                    "WESTERN*", "SHORT STORY*"]
    
    callnumber_1 = ["0.*", "1.*", "3.*", "5.*", "6.*", "7.*", "9.*",
                    "OK 0.*", "OK 1.*", "OK 3.*", "OK 5.*", "OK 6.*", 
                    "OK 7.*", "OK 9.*",
                    "R 0.*", "R 1.*", "R 3.*", "R 5.*", "R 6.*", 
                    "R 7.*", "R 9.*",
                    "Y0.*", "Y1.*", "Y3.*", "Y5.*", "Y6.*", 
                    "Y7.*", "Y9.*"]
    
    callnumber_2 = ["2.*", "4.*", "8.*", 
                    "OK 2.*", "OK 4.*", "OK 8.*",
                    "R 2.*", "R 4.*", "R 8.*",
                    "Y2.*", "Y4.*", "Y8.*"]
    jnf_cd = ["J0.*", "J1.*", "J2.*", "J3.*", "J4.*", 
              "J5.*", "J6.*", "J7.*", "J8.*", "J9.*",]
    
    # Filter `AUD-C` items
    aud_c = cd_rom[cd_rom[CALLNUMBER].isin(c_callnumber)]
    cd_rom = cd_rom[~cd_rom[ITEM].isin(aud_c[ITEM])]
    data = data[~data[ITEM].isin(aud_c[ITEM])]

    # Filter `AUD-J` items
    aud_j = cd_rom[cd_rom[CALLNUMBER].isin(j_callnumber)]
    cd_rom = cd_rom[~cd_rom[ITEM].isin(aud_j[ITEM])]
    data = data[~data[ITEM].isin(aud_j[ITEM])]

    # Filter `AUD-F` items
    aud_f = cd_rom[cd_rom[CALLNUMBER].isin(f_callnumber)]
    cd_rom = cd_rom[~cd_rom[ITEM].isin(aud_f[ITEM])]
    data = data[~data[ITEM].isin(aud_f[ITEM])]

    # Added Sub_callnumber column
    cd_rom[Sub_callnumber] = utils_fund.split_string_value(cd_rom[CALLNUMBER])

    # Filter `AUD-1` items
    aud_1 = cd_rom[cd_rom[CALLNUMBER].isin(callnumber_1)]
    aud_1_subset = utils_fund.filter_items_by_keywords(cd_rom, Sub_callnumber, callnumber_1, 
                                                Exceptional_keywords)
    aud_1 = pd.concat([aud_1, aud_1_subset], ignore_index=True).reset_index(drop=True)
    aud_1 = aud_1.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)

    cd_rom = cd_rom[~cd_rom[ITEM].isin(aud_1[ITEM])]
    data = data[~data[ITEM].isin(aud_1[ITEM])]

    # Filter `AUD-2` items
    aud_2 = cd_rom[cd_rom[CALLNUMBER].isin(callnumber_2)]
    aud_2_subset = utils_fund.filter_items_by_keywords(cd_rom, Sub_callnumber, callnumber_2, 
                                                Exceptional_keywords)
    aud_2 = pd.concat([aud_2, aud_2_subset], ignore_index=True).reset_index(drop=True)
    aud_2 = aud_2.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)

    cd_rom = cd_rom[~cd_rom[ITEM].isin(aud_2[ITEM])]
    data = data[~data[ITEM].isin(aud_2[ITEM])]

    # Filter `JUVENILE NON-FICTION` items
    j_non_fiction = cd_rom[cd_rom[LOCATION].isin(["JUVENILE NON-FICTION"])]
    j_non_fiction_subset = cd_rom[cd_rom[CALLNUMBER].isin(jnf_cd)]
    j_non_fiction = pd.concat([j_non_fiction, j_non_fiction_subset], ignore_index=True).reset_index(drop=True)
    j_non_fiction = j_non_fiction.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)
    data = data[~data[ITEM].isin(j_non_fiction[ITEM])]

    # Merge `AUD-J` ang `Juvenile Non-fiction`
    aud_j = pd.concat([aud_j, j_non_fiction], ignore_index=True).reset_index(drop=True)
    
    return data, aud_1, aud_2, aud_c, aud_f, aud_j, cdm_a, j_non_fiction


######################## Filter VID items #######################

def filter_VID_items(data):
    """
    This function is to filter all VID items
    """
    j_callnumber = ["EASY", "READER", "TWEEN", "BOARD",
                    "JFICTION", "J FICTION",
                    "J0.*", "J1.*", "J2.*", "J3.*", "J4.*", 
                    "J5.*", "J6.*", "J7.*", "J8.*", "J9.*",
                    "Y0.*", "Y1.*", "Y2.*", "Y3.*", "Y4.*", 
                    "Y5.*", "Y6.*", "Y7.*", "Y8.*", "Y9.*",]
    
    callnumber_1 = ["1.*", "3.*", "5.*", "6.*", "7.*", "9.*",
                    "OK 1.*", "OK 3.*", "OK 5.*", "OK 6.*", 
                    "OK 7.*", "OK 9.*",
                    "R 1.*", "R 3.*", "R 5.*", "R 6.*", 
                    "R 7.*", "R 9.*",]
    callnumber_2 = ["0.*", "2.*", "4.*", "8.*", 
                    "OK 0.*", "OK 2.*", "OK 4.*", "OK 8.*",
                    "R 0.*", "R 2.*", "R 4.*", "R 8.*"] 
    callnumber_4 = ["MOVIE", "TV", "791.43.*", "791.45.*"]
    

    # Filter `VID-J` items - part 1
    vid_j = utils_fund.filter_items_by_keywords(data, CALLNUMBER, ["JMOVIE", "JTV*"])
    data = data[~data[ITEM].isin(vid_j[ITEM])]

    # Filter `VID-4` items - part 1
    vid_4 = data[data[LOCATION].isin(["FEATURE FILMS"])]
    data = data[~data[ITEM].isin(vid_4[ITEM])]

    dvd = data[data[MEDIA].isin(["DVD-ROM", "Restricted DVD", 
                                 "BLU-RAY", "Restricted BLU-RAY"])]

    # Filter `VID-J` items - part 2
    vid_j_subset = utils_fund.filter_items_by_keywords(dvd, CALLNUMBER, 
                                                j_callnumber, 
                                                Exceptional_keywords)
    vid_j = pd.concat([vid_j, vid_j_subset], ignore_index=True).reset_index(drop=True)
    dvd = dvd[~dvd[ITEM].isin(vid_j[ITEM])]
    data = data[~data[ITEM].isin(vid_j[ITEM])]

    # Filter `VID-4` items -  part 2
    vid_4_subset = utils_fund.filter_items_by_keywords(dvd, CALLNUMBER, callnumber_4)
    vid_4 = pd.concat([vid_4, vid_4_subset], ignore_index=True).reset_index(drop=True)
    dvd = dvd[~dvd[ITEM].isin(vid_4[ITEM])]
    data = data[~data[ITEM].isin(vid_4[ITEM])]

    # Added Sub_callnumber column
    dvd[Sub_callnumber] = utils_fund.split_string_value(dvd[CALLNUMBER])

    # Filter `VID-1` items 
    vid_1 = utils_fund.filter_items_by_keywords(dvd, CALLNUMBER, 
                                                callnumber_1, 
                                                Exceptional_keywords)
    vid_1_subset = utils_fund.filter_items_by_keywords(dvd, Sub_callnumber, 
                                                callnumber_1, 
                                                Exceptional_keywords)
    vid_1 = pd.concat([vid_1, vid_1_subset], ignore_index=True).reset_index(drop=True)
    vid_1 = vid_1.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)
    dvd = dvd[~dvd[ITEM].isin(vid_1[ITEM])]
    data = data[~data[ITEM].isin(vid_1[ITEM])]


    # Filter `VID-2` items 
    vid_2 = utils_fund.filter_items_by_keywords(dvd, CALLNUMBER, 
                                                callnumber_2, 
                                                Exceptional_keywords)
    vid_2_subset = utils_fund.filter_items_by_keywords(dvd, Sub_callnumber, 
                                                callnumber_2, 
                                                Exceptional_keywords)
    vid_2 = pd.concat([vid_2, vid_2_subset], ignore_index=True).reset_index(drop=True)
    vid_2 = vid_2.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)
    data = data[~data[ITEM].isin(vid_2[ITEM])]

    return data, vid_1, vid_2, vid_4, vid_j


######################## Filter BOOKS items #######################

def filter_BOOKs_items(data):
    """
    """
    books = data[data[MEDIA].isin(["BOOKS", "PAPERBACK BOOKS", "BOARD BOOKS"])]

    child_callnumber = ["EASY", "READER", "TWEEN", "BOARD"]
    jfic_callnumber = ["JFICTION", "JMYSTERY", "JSCIENCE", "JSPORTS",
                       "J FICTION", "J MYSTERY", "J SCIENCE", "J SPORTS"]
    yfic_callnumber = ["YFICTION", "YSCIENCE", "YMYSTERY"]
    afic_callnumber = ["FICTION*", "MYST*", "SCIENCE FIC*", "WESTERN*", "SHORT STORY*"]
    jnf_callnumber = ["J0.*", "J1.*", "J2.*", "J3.*", "J4.*", 
                      "J5.*", "J6.*", "J7.*", "J8.*", "J9.*",
                      "OK J0.*", "OK J1.*", "OK J2.*", "OK J3.*", "OK J4.*",
                      "OK J5.*", "OK J6.*", "OK J7.*", "OK J8.*", "OK J9.*"]
    ynf_callnumber = ["Y0.*", "Y1.*", "Y2.*", "Y3.*", "Y4.*", 
                      "Y5.*", "Y6.*", "Y7.*", "Y8.*", "Y9.*",
                      "OK Y0.*", "OK Y1.*", "OK Y2.*", "OK Y3.*", "OK Y4.*",
                      "OK Y5.*", "OK Y6.*", "OK Y7.*", "OK Y8.*", "OK Y9.*"]
    
    anf_callnumber_1 = ["0.*", "1.*", "2.*", "3.*", "4.*", 
                        "5.*", "6.*", "7.*", "8.*", "9.*"]
    anf_callnumber_2 = ["OK 0.*", "OK 1.*", "OK 2.*", "OK 3.*", "OK 4.*", 
                        "OK 5.*", "OK 6.*", "OK 7.*", "OK 8.*", "OK 9.*"]
    anf_callnumber_3 = ["R 0.*", "R 1.*", "R 2.*", "R 3.*", "R 4.*", 
                        "R 5.*", "R 6.*", "R 7.*", "R 8.*", "R 9.*"]
    anf_callnumber_4 = ["R0.*", "R1.*", "R2.*", "R3.*", "R4.*", 
                        "R5.*", "R6.*", "R7.*", "R8.*", "R9.*"]
    

    # Filter items belong to `CHILD` fund
    child = utils_fund.filter_items_by_keywords(books, CALLNUMBER, child_callnumber)
    books = books[~books[ITEM].isin(child[ITEM])]
    data = data[~data[ITEM].isin(child[ITEM])]

    # Filter items belong to `JFIC` fund
    jfic = utils_fund.filter_items_by_keywords(books, CALLNUMBER, jfic_callnumber)
    books = books[~books[ITEM].isin(jfic[ITEM])]
    data = data[~data[ITEM].isin(jfic[ITEM])]

    # Filter items belong to `YFIC` fund
    yfic = utils_fund.filter_items_by_keywords(books, CALLNUMBER, yfic_callnumber)
    books = books[~books[ITEM].isin(yfic[ITEM])]
    data = data[~data[ITEM].isin(yfic[ITEM])]

    # Filter items belong to `AFIC` fund
    afic = utils_fund.filter_items_by_keywords(books, CALLNUMBER, afic_callnumber)
    books = books[~books[ITEM].isin(afic[ITEM])]
    data = data[~data[ITEM].isin(afic[ITEM])]

    # Added Sub_callnumber column
    books[Sub_callnumber] = utils_fund.split_string_value(books[CALLNUMBER])

    # Filter items belong to `JNF` fund
    jnf = utils_fund.filter_items_by_keywords(books, CALLNUMBER, jnf_callnumber, 
                                              Exceptional_keywords)
    jnf_subset = utils_fund.filter_items_by_keywords(books, Sub_callnumber, jnf_callnumber, 
                                              Exceptional_keywords)
    jnf = pd.concat([jnf, jnf_subset], ignore_index=True).reset_index(drop=True)
    jnf = jnf.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)
    books = books[~books[ITEM].isin(jnf[ITEM])]
    data = data[~data[ITEM].isin(jnf[ITEM])]

    # Filter items belong to `YNF` fund
    ynf = utils_fund.filter_items_by_keywords(books, CALLNUMBER, ynf_callnumber, 
                                              Exceptional_keywords)
    ynf_subset = utils_fund.filter_items_by_keywords(books, Sub_callnumber, ynf_callnumber, 
                                              Exceptional_keywords)
    ynf = pd.concat([ynf, ynf_subset], ignore_index=True).reset_index(drop=True)
    ynf = ynf.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)
    books = books[~books[ITEM].isin(ynf[ITEM])]
    data = data[~data[ITEM].isin(ynf[ITEM])]

    # Filter items belong to `ANF` fund
    anf_list = list()

    for val1, val2, val3, val4 in zip(anf_callnumber_1, anf_callnumber_2, anf_callnumber_3, anf_callnumber_4):
        anf_subset = utils_fund.filter_items_by_keywords(books, CALLNUMBER, 
                                                         [val1, val2, val3, val4], Exceptional_keywords)
        anf_subset_cn = utils_fund.filter_items_by_keywords(books, Sub_callnumber, 
                                                         [val1, val2, val3, val4], Exceptional_keywords)
        anf_subset = pd.concat([anf_subset, anf_subset_cn], ignore_index=True).reset_index(drop=True)
        anf_subset = anf_subset.drop_duplicates(subset=[ITEM], keep='first').reset_index(drop=True)
        books = books[~books[ITEM].isin(anf_subset[ITEM])]
        data = data[~data[ITEM].isin(anf_subset[ITEM])]

        anf_list.append(anf_subset)
    
    return data, child, jfic, afic, yfic, jnf, ynf, anf_list


######################## Filter all items #######################

def filter_all_items(data, save_path, fiscalyr):
    """
    """    
    # Filter `Periodical` items
    periodical = filter_periodicals_items(data)
    # Keep only the items left
    data = data[~data[ITEM].isin(periodical[ITEM])]

    # Filter `Large Print` items first
    bkslp = utils_fund.filter_items_by_keywords(data, CALLNUMBER, [".* LARGE PRINT.*", ".* LP"])
    # Filter items left
    data = data[~data[ITEM].isin(bkslp[ITEM])]

    # Filter VID items
    data, vid_1, vid_2, vid_4, vid_j = filter_VID_items(data)

    # Filter CD-Rom items
    data, aud_1, aud_2, aud_c, aud_f, aud_j, cdm_a, j_non_fiction = filter_CD_ROM_items(data)

    # Filter AEB items
    data, aeb_j, aeb_c = filter_AEB_items(data)

    # Filter AMP items
    data, amp_1, amp_2, amp_a, amp_c, amp_j, amp_y = filter_AMP_items(data)

    # Filter BOOKs items
    data, child, jfic, afic, yfic, jnf, ynf, anf_list = filter_BOOKs_items(data)

    # Save files to save_data
    bkslp.to_excel(f"{save_path}/Fund_FY{fiscalyr}_BKSLP.xlsx", index=False)
    vid_1.to_excel(f"{save_path}/Fund_FY{fiscalyr}_VID_1.xlsx", index=False)
    vid_2.to_excel(f"{save_path}/Fund_FY{fiscalyr}_VID_2.xlsx", index=False)
    vid_4.to_excel(f"{save_path}/Fund_FY{fiscalyr}_VID_4.xlsx", index=False)
    vid_j.to_excel(f"{save_path}/Fund_FY{fiscalyr}_VID_J.xlsx", index=False)

    aud_1.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AUD_1.xlsx", index=False)
    aud_2.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AUD_2.xlsx", index=False)
    aud_c.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AUD_C.xlsx", index=False)
    aud_f.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AUD_F.xlsx", index=False)
    aud_j.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AUD_J.xlsx", index=False)
    cdm_a.to_excel(f"{save_path}/Fund_FY{fiscalyr}_CDM_A.xlsx", index=False)
    # j_non_fiction.to_excel(f"{save_path}/Fund_FY{fiscalyr}_J_NON-FIC.xlsx", index=False)

    aeb_j.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AEB_J.xlsx", index=False)
    aeb_c.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AEB_C.xlsx", index=False)

    amp_1.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AMP_1.xlsx", index=False)
    amp_2.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AMP_2.xlsx", index=False)
    amp_a.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AMP_A.xlsx", index=False)
    amp_c.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AMP_C.xlsx", index=False)
    amp_j.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AMP_J.xlsx", index=False)
    amp_y.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AMP_Y.xlsx", index=False)

    child.to_excel(f"{save_path}/Fund_FY{fiscalyr}_CHILD.xlsx", index=False)
    jfic.to_excel(f"{save_path}/Fund_FY{fiscalyr}_JFIC.xlsx", index=False)
    afic.to_excel(f"{save_path}/Fund_FY{fiscalyr}_AFIC.xlsx", index=False)
    yfic.to_excel(f"{save_path}/Fund_FY{fiscalyr}_YFIC.xlsx", index=False)
    jnf.to_excel(f"{save_path}/Fund_FY{fiscalyr}_JNF.xlsx", index=False)
    ynf.to_excel(f"{save_path}/Fund_FY{fiscalyr}_YNF.xlsx", index=False)

    periodical.to_excel(f"{save_path}/Fund_FY{fiscalyr}_Periodicals.xlsx", index=False)

    data.to_excel(f"{save_path}/Fund_FY{fiscalyr}_data_left.xlsx", index=False)

    for val in np.arange(0, 10, 1):
        anf_list[val].to_excel(f"{save_path}/Fund_FY{fiscalyr}_ANF-{val}.xlsx", index=False)

    fund_list = {"vid-1": vid_1, "vid-2": vid_2, "vid-4": vid_4, "vid-j": vid_j,
                 "aud-1": aud_1, "aud-2": aud_2, "aud-c": aud_c, "aud-f": aud_f, 
                 "aud-j": aud_j, "cdm-a": cdm_a, # "j_non_fiction": j_non_fiction,
                 "aeb-j": aeb_j, "aeb-c": aeb_c, "amp-1": amp_1, "amp-2": amp_2, 
                 "amp-a": amp_a, "amp-c": amp_c, "amp-j": amp_j, "amp-y": amp_y, 
                 "bkslp": bkslp, "child": child, "jfic": jfic, "afic": afic, 
                 "yfic": yfic, "jnf": jnf, "ynf": ynf, "periodical": periodical}

    return anf_list, fund_list



def iterate_filter_by_fund(fund, sub_fund, active_only, fy_inactive):
    """
    """
    # Filter only active items for fund processing
    if sub_fund.shape[0] > 0:
        active_items, inactive_items = filter_items_status.filter_items_by_status(sub_fund)
    else:
        active_items, inactive_items = pd.DataFrame(), pd.DataFrame()

    if (fy_inactive != "None") and fy_inactive.isdigit():
        start_date = f"{int(fy_inactive)-1}-07-01"
        end_date = f"{fy_inactive}-07-01"
        inactive_items = inactive_items[(inactive_items[STATUSDATE] >= start_date) & 
                                        (inactive_items[STATUSDATE] < end_date)]
    
    # Extract the total fund info
    if active_only and (active_items.shape[0] > 0):
        sub_fund_info = utils_fund.calculate_single_fund_info(fund, active_items, inactive_items)
    else:
        sub_fund_info = utils_fund.calculate_single_fund_info(fund, sub_fund, inactive_items)

    return sub_fund_info


def extract_fund_info(data, data_fields, save_path, fiscalyr="2025", 
                      active_only=False, fy_inactive="None"):
    """
    """
    # Remove all items that are excluded based on their medias and locations
    data = remove_unnecesary_items(data, locations=Excluded_locations, medias=Excluded_medias)

    # Convert `STATUSDATE` column from string to datetime
    data[STATUSDATE] = utils.convert_str_to_datetime(data[STATUSDATE])

    # Filter items by their funds
    anf_list, fund_dict = filter_all_items(data, save_path, fiscalyr)

    total_fund_df = pd.DataFrame(columns=data_fields)

    for idx, sub_fund in enumerate(anf_list):
        fund = f"ANF-{idx}"

        print(fund)

        sub_fund_info = iterate_filter_by_fund(fund, sub_fund, active_only, fy_inactive)

        # Add sub_fund_info to the total_fund_df       
        total_fund_df.loc[len(total_fund_df)] = sub_fund_info
    

    for key, sub_fund in fund_dict.items():
        fund = key.upper()

        print(fund)

        sub_fund_info = iterate_filter_by_fund(fund, sub_fund, active_only, fy_inactive)

        # Add sub_fund_info to the total_fund_df       
        total_fund_df.loc[len(total_fund_df)] = sub_fund_info

    
    # Calculate total fund info
    _, fy_info = utils_fund.calculate_multiple_fund_info(total_fund_df)

    # Add fy_info into the total_fund_df
    total_fund_df = pd.concat([total_fund_df, fy_info], axis=1)

    
    return total_fund_df




if __name__ == "__main__":
    print('Hello!')

    data = pd.read_csv('data/Monthly_items_info/Items_2026-06-30_1125pm.csv', 
                       encoding='latin-1', low_memory=False)
    data_fields = ['Fund', 'Volumes', 'FY Circs', 'Lifetime Circs', 
                   'Total Price', 'FY WLMT']
    save_path = './data_save/Fund2026/Monthly reports/Jun2026'
    fiscalyr = "2026"
    active_only = False
    fy_inactive = "None"

    extract_fund_info(data, data_fields, save_path, fiscalyr, active_only, fy_inactive)