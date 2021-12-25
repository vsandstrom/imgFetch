# imgFetch.py

Web scraping program for scraping image links from discogs and inserting them into a .csv file register, corresponding to each item in store.

Program expects the user to supply a register of a certain formating, where ALBUM + ARTIST data exists in each row at column 3, and an IMAGE LINK exists in each row at column 5

It exports the register with the new image links to a new .csv file.

The input file should be located in the same directory as imgFetch.py

usage:
> $ python <input_csv_file> (opt: <output_csv_file>)

If no third argument, a name for the output file, is given, it will use the input filename but append '_export' to name. 
