# codingallstarschallenge

Helllo, 

How did you scrape the page?

Short answer : Httrack and python script.

Long : It was a long time since I perform a similar task, had tried some download helpers tool, but I hadn't done a similar task recently. Thus, I make some research and tried various softwares (like Parsehub). Due to scraped page did not contain the actual codes, it would also be difficult for him to parse the pages for process, so I look for the most effective, and free methods.  I assume you gave other people the same task, as a results too many requests are sent to the ClassCentral. The server is protecting itself from DDoS attacks. After some experimentation, the site was scrapped with the appropriate parameters by Httrack fair enoughly. You can also find a script that can do the similar task. However, because Httrack is open source and considers many problems in advance, I used it as the main source and completed the missing parts with my own code.

How did you handle the Google Translate portion?

Since the codes in the obtained files are not the actual codes of the site, but the codes that appear on the running side, I faced some challenges.2 different methods has been considered to complete the task. The first is to parse the site myself. You can find this approches code in old.code folder. The second is to use the BeautifulSoup library. The first was translating correctly. However, since there are tags outside of html, such as javascript, ajax etc. in the site, it was not able to extract them correctly. For this reason, the design of the site was broken. BeautifulSoup was also parsing the tags correctly and not breaking the design. However, sometimes it was failing to translate because it missed the text in the script tags. After some preprocessing and additions, I was able to parse the site correctly with BeautifulSoup. You may find the whole code files on Github. 

Google Cloud Translation API is employed to translate texts. Languages are parametric, so this script can be used to translate any language html files to any other language. Credentials are stored in the same folder with the code base in this example (not necessarily every time). I divided the code into functions for easy reading. 

The translation is done using the translate_html() function, which takes a string of HTML text as input and translates all the sentences in the text from the source language to the target language using the translate_sentence() function. The translate_sentence() function uses the translate_client object, which is an instance of the Google Cloud Translation API client, to translate a single sentence from the source language to the target language. The source and target languages are specified as arguments to the function. The translate_html() function uses the BeautifulSoup library to parse the input HTML text and find all the text nodes (i.e., the text inside HTML tags). It then checks if the parent of each text node is not a style or script tag and is not a comment. If these conditions are satisfied, it passes the text node to the translate_sentence() function to translate the sentence from the source language to the target language. The translated sentence is then inserted back into the HTML text.

The process_html_file() function reads an HTML file from disk, calls the translate_html() function to translate the HTML inside the <html> tag and writes the translated HTML back to the file.
