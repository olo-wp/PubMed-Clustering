from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

categories = ["title", "gdsType", "summary", "taxon", "Overall design"]

def getPMIDdict(PMIDlist):
    return {p:set() for p in PMIDlist}

def getGEO(PMIDlist):
    linkPre = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=gds&linkname=pubmed_gds&id="
    linkSuf = "&retmode=xml"

    pmids = ",".join(PMIDlist)

    link = linkPre + pmids + linkSuf
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'lxml-xml')
    soup = soup.find('LinkSetDb')
    GEOs = [g.text for g in soup.find_all('Id')]
    return GEOs

def geoToDf(geoNumbers, PMID_GEOdict):
    linkPre = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id="
    linkSuf = "&retmode=xml"
    geoN = ",".join(geoNumbers)
    link = linkPre + geoN + linkSuf
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'lxml-xml')

    df = pd.DataFrame(columns=["GEO", "PMID", "text"])

    for ds in soup.find_all('DocSum'):
        text = ""
        for c in categories:
            res = ds.find('Item', {'Name': c})
            if(res):
                text += res.text + "\n"
        possiblePMID = ds.find('Item', {'Name' :"PubMedIds"})
        possiblePMID = [p.text for p in possiblePMID.find_all('Item', {'Name': 'int'})]
        realPMID = possiblePMID[0]
        curGEO = int(ds.find("Id").text)
        for i in possiblePMID:
            if(i not in PMID_GEOdict):
                continue
            elif (curGEO in PMID_GEOdict[i]):
                continue
            else:
                PMID_GEOdict[i].add(curGEO)
                realPMID = i
                break
        df.loc[len(df.index)] = [curGEO, realPMID, text]

    return df

def geoToDf_new(geoNumbers, PMID_GEOdict):
    start = time.time()
    linkPre = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id="
    linkSuf = "&retmode=xml"
    geoN = ",".join(geoNumbers)
    link = linkPre + geoN + linkSuf
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'lxml-xml')

    df = pd.DataFrame(columns=["GEO", "PMID", "Accession", "text"])
    counter = 1

    for ds in soup.find_all('DocSum'):
        print(counter)
        possiblePMID = ds.find('Item', {'Name' :"PubMedIds"})
        possiblePMID = [p.text for p in possiblePMID.find_all('Item', {'Name': 'int'})]
        realPMID = possiblePMID[0]
        curGEO = int(ds.find("Id").text)
        accession = ds.find("Item", {'Name':'Accession'}).text
        taxon = ds.find("Item", {'Name':'taxon'}).text
        text = ''
        for c in categories:
            res = ds.find('Item', {'Name': c})
            if(res):
                text += res.text + "\n"
        for i in possiblePMID:
            if(i not in PMID_GEOdict):
                continue
            elif (curGEO in PMID_GEOdict[i]):
                continue
            else:
                PMID_GEOdict[i].add(curGEO)
                realPMID = i
                break
        link_soft = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?targ=self&acc={accession}&form=text&view=brief"
        response_soft = requests.get(link_soft)
        soft_data = response_soft.text
        for line in soft_data.splitlines():
            if line.startswith("!Series_overall_design"):
                text += line.split('=')[1].strip()
        df.loc[len(df.index)] = [curGEO, realPMID, accession, text]
        counter += 1
    end = time.time()
    print(f'time is: {end - start}')
    df = df.drop(columns=["Accession"])
    return df

