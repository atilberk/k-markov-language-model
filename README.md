# K-Markov Language Model
A K-Markov Language Model and Random Text Generator

This is a project I have implemented and done the complexity analysis for Algorithm Design and Anaylsis course taught by Dr. Alptekin Kupcu at Koç University Computer Engineering Department.

The original project description can be found at [Princeton's COS226 Assignment in Fall'08](http://www.cs.princeton.edu/courses/archive/fall08/cos226/assignments/model.html).

Full report and complexity analysis on the project can be read on [REPORT.md](/REPORT.md)

### How to run?
```
$ python TextGenerator.py -K <Kvalue> -M <Mvalue> <source_file> <destination_file> [optional args]
```

### Arguments

**-K :** K value for Markov model  
**-M :** Number of characters to be generated  

**-v , --verbose :** Makes the output verbose  
**-q , --quiet :** Makes the output quite  
**-l , --log :** Writes the log into `log.txt`  
**-i , --ignore-new-line :** Ignores the newline character in input  
