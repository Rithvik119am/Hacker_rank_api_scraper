import http.client
import pandas as pd
import json
from urllib.parse import urlparse
def match_data(database,contest_board,name):
    """
    This function is used to match the data from the database and the contest board.
    It reads the database excel file, renames the columns, merges the database and contest board data,
    sorts the data by score, and writes the data to an excel file.

    Args:
        database (str): The name of the database excel file.
        contest_board (DataFrame): The contest board data.
        name (str): The name of the output excel file.
    """
    database=pd.read_excel(database+'.xlsx')
    database.rename(columns={'HackerRank Username:\nNote: Remember that the username is case sensitive': 'HackerRank'}, inplace=True)
    branch=database.columns[9]
    database["HackerRank"]=database['HackerRank'].str.lstrip('@')
    ans=pd.merge(database, contest_board, left_on='HackerRank', right_on='UserName', how='inner')
    ans=ans.loc[:,['Roll No:','Full Name:','UserName','Score',branch]]
    ans=ans.rename(columns={branch:'Branch:'})
    branch='Branch:'
    ans.sort_values(by="Score", ascending=True)
    with pd.ExcelWriter(name + '.xlsx') as writer:
        for branch_name, data in ans.groupby(branch):
            data.to_excel(writer, sheet_name=str(branch_name), index=False)
    print(ans)
    

def ans_finder(url):
    """
    This function is used to collect data from the leaderboard URL and return it as a list of JSONs.
    It sends a GET request to the server to get the data in the form of JSONs.

    Args:
        url (str): The leaderboard URL.

    Returns:
        list: A list of JSONs containing the leaderboard data.
    """
    parsed_url = urlparse(url)
    print(parsed_url.path)
    conn = http.client.HTTPSConnection("www.hackerrank.com")
    payload = ""
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        }
    to_send="/rest/"+parsed_url.path+"?offset=0&limit="+str(1)
    conn.request("GET", to_send, payload, headers)
    res = conn.getresponse()
    data = res.read()
    data=data.decode("utf-8")
    parsed_data = json.loads(data)
    start=0
    end=100
    data_list=[]
    while True:
        to_send="/rest/"+parsed_url.path+"?offset="+str(start)+"&limit="+str(end)
        conn.request("GET", to_send, payload, headers)
        res = conn.getresponse()
        data = res.read()  
        data_list.append(data.decode("utf-8"))
        if end>=parsed_data['total']:
            break
        if end+100<=parsed_data['total']:
            start,end=end,end+100
        else:
            start,end=end,parsed_data['total']
    return data_list
def data_parser(data_list):
    """
    This function is used to parse the data list and return it as a DataFrame.

    Args:
        data_list (list): A list of JSONs containing the leaderboard data.

    Returns:
        DataFrame: A DataFrame containing the parsed data.
    """
    hacker_scores_list=[]
    for data in data_list:
        parsed_data = json.loads(data)
        hacker_scores = [{"UserName": model['hacker'], "Score": model['score']} for model in parsed_data['models']]
        hacker_scores_list.extend(hacker_scores)
    df = pd.DataFrame(hacker_scores_list, columns=["UserName", "Score"])
    return df
def pre_matcher(link,leb_df):
    """
    This function is used to pre-match the link and the leaderboard data.

    Args:
        link (str): The URL.
        leb_df (DataFrame): The leaderboard data in DataFrame format.

    Returns:
        str: The name of the excel file.
    """
    link= urlparse(link).path.split('/')[2].replace('-', '_')
    if link[0]=='2':
        db="2nd Year BTech Coding Platform Details(1-678)"
    elif link[0]=='3':
        db="3rd Year B. Tech Coding Platform Details(1-648)"
    match_data(db,leb_df,link)
    return link
def linker(link):
    """
    This function is used to link the URL to the excel file.
    It finds the answer from the URL, parses the data, and pre-matches the link and the leaderboard data.

    Args:
        link (str): The URL in the given format https://www.hackerrank.com/contests/'NUMBER WITH nd or rd'-year-cdc-24-12-2023/leaderboard

    Returns:
        str: The name of the excel file.
    """
    ddd=ans_finder(link)
    leader_df=data_parser(ddd)
    return pre_matcher(link,leader_df)
