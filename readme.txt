Hello

This program is intended to simulate both a back end environment and a front end environment.
Backend: Console Window with debug info
Frontend: Web UI

Instructions:
    Start (This should open your browser automatically)
    If browser does not open, open your browser and navigate to http://127.0.0.1:5000/
    From here, enter your queries into the chat box and see the responses from GPT.

Further Development:
    For further development features I would have liked to add, please look at the Notes.txt file,
    it goes into detail my thinking process and is a typical file I have in all my projects so future
    devs can see my thinking process. It might be a bit scattered, however I find it adds context to some decisions
    I made while programming.

    Features I would like to implement:
        Chat memory
            Currently the program has no context to previous messages, there will have to be some sort of server 
            database of responses based off user ids. This will add a more immersive experience for users.
        Local model
            Currently I am making 2 calls to GPT, once for a check to see if the user input matches
            the theme of number facts, and the second to provide an elaborated response based off of the
            numbers API response. A way to optimize this is to have a light weight model running server side
            which can provide basic answers and prompt the user to ask number questions, then upon confirmation
            of the function call, the program will make 1 call to GPT to create an elaborated response.

            To extend on this, another optimization that can me made is to cache popular results. So for example
            if 100 users ask about the number 10, and the most common response from numbersAPI is that 10 is the 
            number of years in a decade, the GPT elaborated response can be cached server side and presented to the user.
            Although this method might have an issue of making the chat seem robotic and static, there can be
            measures taken to ensure that a certain cached response is not served to the user more than once.
        Adjustable parameters
            Some parameters could have been implemented on the back end to extract certain details such as
            if the user wanted a date fact, a math fact, year fact, or trivia about a random or particular number.
        Preventative measures against gpt hallucination
            Some measures can be added to prevent gpt hallucination with either a fast function for info verification
            or fact verification, this can be done via a script that can crawl the DB mentioned above and verify facts
            creating a DB of stored facts we can serve instantly, and if needed, generate new ones. Script can just verify
            facts by doing a wikipedia query.