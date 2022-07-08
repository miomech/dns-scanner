# Domain Crawler
**Instructions**
1. Create a file called "domain_list" and place it in the folder where the program is
or provide a file to the program by using the "-i" flag
2. The program will generate a csv of all the data for the domains, along with specefic duneland media checks

Note:
> 1. The input file must only have domains seperated by newline characters
> 2. The program will auto detect the file as long as it is in the same folder as the "domain_crawler.py"

To run the program cd to the folder in your terminal and run:
``` bash
python3 ./domain_crawler.py
```

Alternativly to provide an input file with a name of your choice run:
``` bash
python3 ./domain_crawler.py -i myfilename.txt
```