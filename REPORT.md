### Koç University 
### Department of Computer Engineering 
### COMP 446 Project Report 
# Natural Language Modelling 
### Atılberk Çelebi 
### acelebi@ku.edu.tr 

## Introduction  

In this project, we consider the problem of generating random text, a sequence of 
randomly chosen characters, given an input text corpus. We expect to construct a model 
which mimics the input text in a way that the output is also consist of stylised words and 
sentences by ordering the characters in a meaningful order. We adopted K­Markov Model 
and obtained the desired output utilising hashmap data structure. In this report, we are going 
to propose and explain our solution and its time and space complexity analysis in detail. 

## Solution Approach: K­Markov Model 

To achieve the given task of generating stylised random text of a certain length given 
a piece of input text, we use the methods of statistical language modelling. A statistical 
language model is a model which contains a vocabulary, set of all words, and a probability 
distribution over those words so that it can estimate the relative likelihood to different 
subsequences, words and phrases in order to be utilised in many applications of various 
research areas such as speech recognition and natural language processing. 

In natural language, we know that the probability of occurring a character does not 
only depends on its frequency of occurring in whole corpus, but also depends on the 
occurrences of the other characters. For example, if the past four characters are ​_hors_, there is high probability that the next letter is ​_e_. Markov Models addresses the problem of estimation using this simple fact. More formally, Markov Models determines the probability of an event using the probabilities of the previous events. A K­Markov Model only considers the last K states. In our project, we are going to adopt K­Markov Model to generate stylised random text.

## Design Choices, Implementation, and Complexity Analysis  

First, we convert our input text into a one long string and perform some preprocessing 
to nicely handle the white spaces and special characters and finally convert the string into a 
character array. Then, we initialise our ​_LanguageModel_ which is basically just a hashtable 
with key­value pairs. We are going to take each K­substring of the input string and threat 
them as our keys throughout our solution. As for the value, each key in the hashtable is bound 
to a ​_Markov_ object specific for the key, which is another hashtable for suffixes and keeps the record of the occurring suffixes, next tokens (in our case, the next characters), and their 
frequency of occurrence so that we can later calculate the probability distribution to generate 
a random character after that substring. We call this procedure as population of our language 
model. The corresponding method in our ​_LanguageModel_ class is ​`populate()`. The method 
takes a preprocessed input text, a preprocessor for the substrings, and K value, then iterates 
over the input string N­K times where N is the length of the input. In each iteration takes a 
K­substring, preprocess that substring in ​_O(K)_ time, and inserts into the key table if it has not been inserted before. The insertion is done by our ​`insert()` method and checks if the key 
has already exists in key table and inserts a new ​_Markov_ object with that key. Existence 
check and actual insertion are done in ​_O(1)_ time with the hashtable data structure. Lastly, `populate()` increments the frequency of the next character in that key’s suffix table by one. 
This addition is also ​_O(1)_ since the suffix table is also a hashtable. Overall, population takes _O(NK)_ time. Moreover, the size of key table can be at most ​_O(A^K)_ ​where A is the size of the alphabet, the set of all valid characters in our language. The size of each suffix table can be at most ​_O(A)_ considering a key can be followed by maximum A different characters in any input with that language.

After we populated our language model and recorded all the information we require 
from the input, we are ready to start generating a random text sequence of length M. Since 
the generated token depends on the previous most recent K tokens, we cannot actually 
generate the first K tokens with our model. Therefore, we begin with printing the first K 
character, then we are able to generate the next M­K characters (from K+1th to Mth) using 
our model. Note that we require input length (N) and output length (M) to be greater than K. 
Before generating each token based on its last K predecessors, we need to check if that last K 
characters are used as a key before, because previous random character generations might have produced never­seen­before keys. In such case, we need to insert that key into our _LanguageModel_ and create a new ​_Markov_ object with empty suffix table for that key. Now, 
we can ask for a random character from the ​_Markov_ object associated with the key. ​_Markov_ object has a method called ​`random()` which returns a character from the alphabet with the 
probability distribution based on the frequency of occurrences of characters after that 
particular key. For example, in our input, we may have three occurrence of ​_thi_, with two 
occurrences in _this_, and one occurrence in ​_thin_; therefore, for our K­Markov Model with K 
equals 3, given the key is ​_thi_, the probability of generating ​_s_ as next character is 2/3 and the probability of generating ​_n_ is 1/3. If there is no history of occurrence of the key in our language model, we can safely assume that the probability is uniformly distributed over the alphabet and probability of generating any character is 1/A. _Markov_'s `random()` method takes _O(A)_ time in the worst case since how it works is the following: It generates a random float number in _​[0,F)_, where F is the total frequency of the key, and iterates over the suffix table and subtracts the frequency of each suffix one by one until it drops below zero. The method returns the suffix which causes the random number to drop below zero. If there is no entry in the suffix table, the method returns a random character from the alphabet uniformly. Note that the worst case scenario is extremely rare since it requires a very large suffix table and a very big random number. We can safely assume it takes ​_O(1)_ time on average. After we 
obtain our random character from our Markov model, notice that we need to update the suffix 
table of the key for the newly generated character, hence the probability distribution which is 
done in ​_O(1)_ time thanks to hashtable implementation. Finally, we append the generated 
token to the output sequence and continue with the next generated character in the next 
iteration. Total time for generating a text of length M with K­Markov model takes ​_O(MK)_ time and allocates ​_O(M)_ sized space for the output sequence.

Ultimately, given an input text sequence of length N, our solution reads and populates 
the K­Markov language model in ​_O(NK)_ time and generates a random sequence of length M 
in ​_O(MK)_ time. In total, the algorithm works in ​_O((N+M)K)_ times where N and M are usually 
very large numbers compared to K value. As the value of K increases, the randomness of the 
output decreases since the number of possible keys increase exponentially with K and it 
causes the frequency of occurrences of suffixes for each distinct key to be low. This results in very sparse suffix tables for each key; therefore, given a key, the variety of possible character to be generated decreases. If K is large enough, the output will be exactly same with the input for the first N characters then the remaining M­N characters will be uniformly random and therefore a total gibberish. Conversely, as K value gets smaller, the randomness of the output increases but the resemblance of the original text decreases. The number of possible keys is too small to differentiate their suffixes from each other; therefore, for each key, we obtain dense suffix tables with many entries and high frequencies. As a result, if K value gets too small, each key starts to be able to randomly produce pretty much any character with no 
distinct bias; hence, the output becomes gibberish again. Our experiments with English text 
shows that the words becomes meaningful with K equals 4, and sentences becomes proper, 
with subject­verb­object relationship, when K is around 10. As K increases more, the 
sentences becomes more sophisticated and meaningful since it approaches to input text. From 
that, we conclude that K value should be really small compared to N and M values. 
Therefore, for total asymptotic running time complexity we may only consider N and M 
values and ignore the factor of K and say that the overall complexity is ​_O(N+M)_.
 
## Conclusion 
In this project, we have implemented a language model (LM) with K­Markov model 
approach to generate stylized random text using an input corpus. We have highly exploited 
the benefits of hashtable data structure since we require a lot of search and replace operations 
to perform our task. Moreover, we have learned and applied the common approach to the 
random generation based on a distribution problem. Besides, we had a lot of chance to 
examine and understand the structure of natural languages and statistical models to process 
them. The difficulty was to understand the problem and the goal since the input is simply the 
natural language, the language that we as humans use to communicate. Thus, it is something 
we are closely familiar but do not really deal with understanding its dynamics. However, 
once understood, solving the problem was relatively easy. The hardest part was to divide the 
problem into smaller pieces and understand each of them and solve separately while keeping 
the track of the overall picture in mind. Particularly, keeping a hashtable which contains other 
hashtables was considerably hard to understand and analyse how it grows. Through the 
knowledge acquired in our course, we were able to perform analysis more systematic and 
confident. We learned that the worst­case analysis does not fully represent an algorithm’s 
characteristic so we need to use different analysis such as average and amortized as well. To conclude, the course taught us how to approach a problem, how to understand and take steps 
to solve it in traceable and provable ways. Even though the problem and the solution is 
simple, the skills that enables us to define and formalise any problem and solve responsibly is 
important and valuable. 

## References 

http://www.cs.princeton.edu/courses/archive/fall08/cos226/assignments/model.html 
https://www.ics.uci.edu/~pattis/ICS­33/lectures/complexitypython.txt 