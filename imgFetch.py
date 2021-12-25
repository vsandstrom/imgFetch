
# TODO:
# [ X ] Get album and artist name from excel sheet document, (export it to sql before handling?)
# [ X ] Send HTTP request to website using artist and album name, fetching html document (from DISCOGS?)
# [ X ] Parse html data with BeautifulSoup to retrieve link to album cover image
# [ X ] Find html tag using id or class names
# [ X ] Add album cover link back into excel sheet document
# [ X ] Make it reusable - only add coverart if there is none
# [  ] Make money

import sys
import requests
import csv
from bs4 import BeautifulSoup



# Check if command line arguments follow program requirements
if len(sys.argv) == 3:
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
elif len(sys.argv) == 2:
    inputfile = sys.argv[1]
    outputfile = sys.argv[1].split('.')[0]
    outputfile = outputfile + '_export' + '.csv'
else:
    sys.exit("ERROR. Did you make a mistake in the spelling")


def imgFetcher(IN, OUT):
    """
    Opens a .csv file, where column 3 contains ARTIST and ALBUM data, formats a http-request to Discogs searching for
    record, parses HTML response and filters it to get an image link to the record. The link is inserted in the right
    place and the entire file is exported again as a .csv file
    """

    ITEMCOLUMN = 2
    IMGCOLUMN = 4

    preCount = 0
    postCount = 0
    totalCount = 0
    procent = 0
    
    
    # Tries to open a database file in .csv format
    try:
        with open(IN, 'r') as file:

            # if .csv file is created by 'Numbers' application, the delimiter can be a ';'
            data = csv.reader(file, delimiter=',')

            # for row in data:
            #     if len(row) > 0:
            #         print(row[0].split(';'))

            data = [e for e in data]

            totalCount = len(data)

            for row in data:
                if len(row[IMGCOLUMN]) > 0:
                    preCount += 1

        procent = 100 / totalCount

        print(f'Before image-fetching: { procent * preCount }')
    except FileNotFoundError:
        msg = f"Sorry, file {IN} not recognized"
        print(msg)
        sys.exit()

    # Makes requests to Discogs and writes the filtered link to the image of each row to file
    with open(OUT, 'w', newline='') as file:
        output = csv.writer(file, dialect='excel', delimiter=',')
        for row in data:
            if row[ITEMCOLUMN] != 'name':
                if len(row[IMGCOLUMN]) == 0:
                    print(len(row[IMGCOLUMN]))
                    request = row[ITEMCOLUMN]

                    # if length is not greater than 3, the field only contains ' - ' and is not useful
                    if len(request) > 3:
                        request = request.split(' ')
                        request = '+'.join(request)
                        request = f'https://www.discogs.com/search/?q={request}&type=all'

                        # Sending HTTP-request to url and get HTML response
                        r = requests.get(request)

                        if r.status_code == 200:
                            r = r.text
                        else:
                            pass

                        # Parsing HTML 
                        soup = BeautifulSoup(r, "html5lib")

                        span = soup.find('span', {'class': 'thumbnail_center'})
                        if span != None:

                            # check if there is an object here or if NoneType
                            img = span.find('img')
                            if img.has_attr('data-src') == True:
                                src = img.attrs['data-src']
                                row[IMGCOLUMN] = src
                                postCount += 1
                else:
                    postCount += 1
            output.writerow(row)

    print(f'After image-fetching: { procent * postCount }')

# run function
if __name__ == "__main__":
    imgFetcher(inputfile, outputfile)
