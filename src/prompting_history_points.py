# config.py
# Stores example history points for prompting the fact checker chat and thought trace generator

SEARCH_HISTORY_POINTS = [
    # Example 1
    [
        {"role": "user", "message": "Question What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?"},
        {"role": "model", "message": "Thought 1 I need to search Colorado orogeny, find the area that the eastern sector of the Colorado orogeny extends into, then find the elevation range of the area."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Colorado orogeny]"},
        {"role": "model", "message": "Observation 1 The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas."},
        {"role": "model", "message": "Thought 2 It does not mention the eastern sector. So I need to look up eastern sector."},
        {"role": "model", "message": "Action 2 SearchActions.Lookup[entity=Colorado orogeny, string=eastern sector]"},
        {"role": "model", "message": "Observation 2 (Result 1 / 1) The eastern sector extends into the High Plains and is called the Central Plains orogeny."},
        {"role": "model", "message": "Thought 3 The eastern sector of Colorado orogeny extends into the High Plains. So I need to search High Plains and find its elevation range."},
        {"role": "model", "message": "Action 3 SearchActions.Search[entity=High Plains]"},
        {"role": "model", "message": "Observation 3 High Plains refers to one of two distinct land regions"},
        {"role": "model", "message": "Thought 4 I need to instead search High Plains (United States)."},
        {"role": "model", "message": "Action 4 SearchActions.Search[entity=High Plains (United States)]"},
        {"role": "model", "message": "Observation 4 The High Plains are a subregion of the Great Plains. From east to west, the High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130 m).[3]"},
        {"role": "model", "message": "Thought 5 High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft."},
        {"role": "model", "message": "Action 5 Finish[1,800 to 7,000 ft]"}
    ],
    # Example 2
    [
        {"role": "user", "message": "Question Musician and satirist Allie Goertz wrote a song about the 'The Simpsons' character Milhouse, who Matt Groening named after who?"},
        {"role": "model", "message": "Thought 1 The question simplifies to 'The Simpsons' character Milhouse is named after who. I only need to search Milhouse and find who it is named after."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Milhouse]"},
        {"role": "model", "message": "Observation 1 Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening."},
        {"role": "model", "message": "Thought 2 The paragraph does not tell who Milhouse is named after, maybe I can look up 'named after'."},
        {"role": "model", "message": "Action 2 SearchActions.Lookup[entity=Milhouse, string=named after]"},
        {"role": "model", "message": "Observation 2 (Result 1 / 1) Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous."},
        {"role": "model", "message": "Thought 3 Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon."},
        {"role": "model", "message": "Action 3 Finish[Richard Nixon]"}
    ],
    # Example 3
    [
        {"role": "user", "message": "Question Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?"},
        {"role": "model", "message": "Thought 1 I need to search Adam Clayton Powell and The Saimaa Gesture, and find which documentary is about Finnish rock groups."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Adam Clayton Powell]"},
        {"role": "model", "message": "Observation 1 Could not find [Adam Clayton Powell]. Similar: [’Adam Clayton Powell III’, ’Seventh Avenue (Manhattan)’, ’Adam Clayton Powell Jr. State Office Building’, ’Isabel Washington Powell’, ’Adam Powell’, ’Adam Clayton Powell (film)’, ’Giancarlo Esposito’]."},
        {"role": "model", "message": "Thought 2 To find the documentary, I can search Adam Clayton Powell (film)."},
        {"role": "model", "message": "Action 2 SearchActions.Search[entity=Adam Clayton Powell (film)]"},
        {"role": "model", "message": "Observation 2 Adam Clayton Powell is a 1989 American documentary film directed by Richard Kilberg. The film is about the rise and fall of influential African-American politician Adam Clayton Powell Jr.[3][4] It was later aired as part of the PBS series The American Experience."},
        {"role": "model", "message": "Thought 3 Adam Clayton Powell (film) is a documentary about an African-American politician, not Finnish rock groups. So the documentary about Finnish rock groups must instead be The Saimaa Gesture."},
        {"role": "model", "message": "Action 3 Finish[The Saimaa Gesture]"}
    ],
    # Example 4
    [
        {"role": "user", "message": "Question What profession does Nicholas Ray and Elia Kazan have in common?"},
        {"role": "model", "message": "Thought 1 I need to search Nicholas Ray and Elia Kazan, find their professions, then find the profession they have in common."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Nicholas Ray]"},
        {"role": "model", "message": "Observation 1 Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 - June 16, 1979) was an American film director, screenwriter, and actor best known for the 1955 film Rebel Without a Cause."},
        {"role": "model", "message": "Thought 2 Professions of Nicholas Ray are director, screenwriter, and actor. I need to search Elia Kazan next and find his professions."},
        {"role": "model", "message": "Action 2 SearchActions.Search[entity=Elia Kazan]"},
        {"role": "model", "message": "Observation 2 Elia Kazan was an American film and theatre director, producer, screenwriter and actor."},
        {"role": "model", "message": "Thought 3 Professions of Elia Kazan are director, producer, screenwriter, and actor. So profession Nicholas Ray and Elia Kazan have in common is director, screenwriter, and actor."},
        {"role": "model", "message": "Action 3 Finish[director, screenwriter, actor]"}
    ],
    # Example 5
    [
        {"role": "user", "message": "Question Which magazine was started first Arthur's Magazine or First for Women?"},
        {"role": "model", "message": "Thought 1 I need to search Arthur's Magazine and First for Women, and find which was started first."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Arthur's Magazine]"},
        {"role": "model", "message": "Observation 1 Arthur's Magazine (1844-1846) was an American literary periodical published in Philadelphia in the 19th century."},
        {"role": "model", "message": "Thought 2 Arthur's Magazine was started in 1844. I need to search First for Women next."},
        {"role": "model", "message": "Action 2 SearchActions.Search[entity=First for Women]"},
        {"role": "model", "message": "Observation 2 First for Women is a woman's magazine published by Bauer Media Group in the USA.[1] The magazine was started in 1989."},
        {"role": "model", "message": "Thought 3 First for Women was started in 1989. 1844 (Arthur's Magazine) < 1989 (First for Women), so Arthur's Magazine was started first."},
        {"role": "model", "message": "Action 3 Finish[Arthur's Magazine]"}
    ],
    # Example 6
    [
        {"role": "user", "message": "Question Were Pavel Urysohn and Leonid Levin known for the same type of work?"},
        {"role": "model", "message": "Thought 1 I need to search Pavel Urysohn and Leonid Levin, find their types of work, then find if they are the same."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Pavel Urysohn]"},
        {"role": "model", "message": "Observation 1 Pavel Samuilovich Urysohn (February 3, 1898 - August 17, 1924) was a Soviet mathematician who is best known for his contributions in dimension theory."},
        {"role": "model", "message": "Thought 2 Pavel Urysohn is a mathematician. I need to search Leonid Levin next and find its type of work."},
        {"role": "model", "message": "Action 2 SearchActions.Search[entity=Leonid Levin]"},
        {"role": "model", "message": "Observation 2 Leonid Anatolievich Levin is a Soviet-American mathematician and computer scientist."},
        {"role": "model", "message": "Thought 3 Leonid Levin is a mathematician and computer scientist. So Pavel Urysohn and Leonid Levin have the same type of work."},
        {"role": "model", "message": "Action 3 Finish[yes]"}
    ],
    # Example 7
    [
        {"role": "user", "message": "Determine if there is Observation that SUPPORTS or REFUTES a Claim, or if there is NOT ENOUGH INFORMATION. Claim Nikolaj Coster-Waldau worked with the Fox Broadcasting Company."},
        {"role": "model", "message": "Thought 1 I need to search Nikolaj Coster-Waldau and find if he has worked with the Fox Broadcasting Company."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Nikolaj Coster-Waldau]"},
        {"role": "model", "message": "Observation 1 Nikolaj William Coster-Waldau (born 27 July 1970) is a Danish actor and producer. He graduated from the Danish National School of Performing Arts in Copenhagen in 1993,[1], and had his breakthrough role in Denmark with the film Nightwatch (1994). He played Jaime Lannister in the HBO fantasy drama series Game of Thrones, for which he received two Primetime Emmy Award nominations for Outstanding Supporting Actor in a Drama Series.. Coster-Waldau has appeared in numerous films in his native Denmark and Scandinavia, including Headhunters (2011) and A Thousand Times Good Night (2013). In the U.S, his debut film role was in the war film Black Hawk Down (2001), playing Medal of Honor recipient Gary Gordon.[2] He then played a detective in the short-lived Fox television series New Amsterdam (2008), and appeared in the 2009 Fox television film Virtuality, originally intended as a pilot."},
        {"role": "model", "message": "Thought 2 Because he 'appeared in the 2009 Fox television film Virtuality', he should have worked with the Fox Broadcasting Company."},
        {"role": "model", "message": "Action 2 Finish[SUPPORTS]"}
    ],
    # Example 8
    [
        {"role": "user", "message": "Claim Stranger Things is set in Bloomington, Indiana."},
        {"role": "model", "message": "Thought 1 I should search for Stranger Things, and see if it is set in Bloomington, Indiana."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Stranger Things]"},
        {"role": "model", "message": "Observation 1 Stranger Things is an American science fiction horror drama television series created by the Duffer Brothers. Set in the 1980s, primarily in the fictional town of Hawkins, Indiana, the series centers on a number of mysteries and supernatural events occurring around the town and their impact on an ensemble of child and adult characters."},
        {"role": "model", "message": "Thought 2 The observation says that it is set in a 'fictional town of Hawkins, Indiana', so it is not set in Bloomington."},
        {"role": "model", "message": "Action 2 Finish[REFUTES]"}
    ],
    # Example 9 (for Billboard Hot 100)
    [
        {"role": "user", "message": "Claim Beautiful reached number two on the Billboard Hot 100 in 2003."},
        {"role": "model", "message": "Thought 1 I need to search the song Beautiful and find if it reached number two on the Billboard Hot 100 in 2003."},
        {"role": "model", "message": "Action 1 SearchActions.Search[entity=Beautiful]"},
        {"role": "model", "message": "Observation 1 Could not find [Beautiful]. Similar: [’Beautiful’, ’Beautiful, Beautiful’, ’A Beautiful Mind (film)’, ’Beautiful (Christina Aguilera song)’, ’Life Is Beautiful’]."},
        {"role": "model", "message": "Thought 2 From suggestions, I should search 'Beautiful (Christina Aguilera song)' to find the song."},
        {"role": "model", "message": "Action 2 SearchActions.Search[entity=Beautiful (Christina Aguilera song)]"},
        {"role": "model", "message": "Observation 2 'Beautiful' is a song recorded by American singer Christina Aguilera for her fourth studio album, Stripped (2002)."},
        {"role": "model", "message": "Thought 3 It does not mention Billboard, so I need to look up 'Billboard Hot 100' to find if it reached number two on it in 2003."},
        {"role": "model", "message": "Action 3 SearchActions.Lookup[entity=Beautiful (Christina Aguilera song), string=Billboard Hot 100]"},
        {"role": "model", "message": "Observation 3 (Result 1 / 3) The song peaked at number two on the Billboard Hot 100 in the United States, where it was certified Gold for 500,000 units shipped."},
        {"role": "model", "message": "Thought 4 It only says the song peaked at number two on the Billboard Hot 100, but not if it was in 2003. I am not sure if this claim is true or not."},
        {"role": "model", "message": "Action 4 Finish[NOT ENOUGH INFO]"}
    ]
]

CALCULATOR_HISTORY_POINTS = [
    [
        {"role": "user", "message": "What is the sum of 5 and 7?"},
        {"role": "model", "message": "Thought 1 I need to add 5 and 7."},
        {"role": "model", "message": "Action 1 MathActions.sum[a=5, b=7]"},
        {"role": "model", "message": "Observation 1 The sum of 5 and 7 is 12."},
        {"role": "model", "message": "Thought 2 The answer is 12."},
        {"role": "model", "message": "Action 2 Finish[12]"}
    ],
    [
        {"role": "user", "message": "What is 10 divided by 2?"},
        {"role": "model", "message": "Thought 1 I need to divide 10 by 2."},
        {"role": "model", "message": "Action 1 MathActions.divide[a=10, b=2]"},
        {"role": "model", "message": "Observation 1 10 divided by 2 is 5."},
        {"role": "model", "message": "Thought 2 The answer is 5."},
        {"role": "model", "message": "Action 2 Finish[5]"}
    ],
    [
        {"role": "user", "message": "What is 15 minus 4?"},
        {"role": "model", "message": "Thought 1 I need to subtract 4 from 15."},
        {"role": "model", "message": "Action 1 MathActions.subtract[a=15, b=4]"},
        {"role": "model", "message": "Observation 1 15 minus 4 is 11."},
        {"role": "model", "message": "Thought 2 The answer is 11."},
        {"role": "model", "message": "Action 2 Finish[11]"}
    ],
    [
        {"role": "user", "message": "What is 6 times 8?"},
        {"role": "model", "message": "Thought 1 I need to multiply 6 by 8."},
        {"role": "model", "message": "Action 1 MathActions.multiply[a=6, b=8]"},
        {"role": "model", "message": "Observation 1 6 times 8 is 48."},
        {"role": "model", "message": "Thought 2 The answer is 48."},
        {"role": "model", "message": "Action 2 Finish[48]"}
    ],
    [
        {"role": "user", "message": "What is 2 to the power of 5?"},
        {"role": "model", "message": "Thought 1 I need to raise 2 to the power of 5."},
        {"role": "model", "message": "Action 1 MathActions.power[a=2, b=5]"},
        {"role": "model", "message": "Observation 1 2 to the power of 5 is 32."},
        {"role": "model", "message": "Thought 2 The answer is 32."},
        {"role": "model", "message": "Action 2 Finish[32]"}
    ],
    [
        {"role": "user", "message": "What is 100 minus 33?"},
        {"role": "model", "message": "Thought 1 I need to subtract 33 from 100."},
        {"role": "model", "message": "Action 1 MathActions.subtract[a=100, b=33]"},
        {"role": "model", "message": "Observation 1 100 minus 33 is 67."},
        {"role": "model", "message": "Thought 2 The answer is 67."},
        {"role": "model", "message": "Action 2 Finish[67]"}
    ],
    [
        {"role": "user", "message": "What is 9 times 9?"},
        {"role": "model", "message": "Thought 1 I need to multiply 9 by 9."},
        {"role": "model", "message": "Action 1 MathActions.multiply[a=9, b=9]"},
        {"role": "model", "message": "Observation 1 9 times 9 is 81."},
        {"role": "model", "message": "Thought 2 The answer is 81."},
        {"role": "model", "message": "Action 2 Finish[81]"}
    ],
    [
        {"role": "user", "message": "What is 20 divided by 4?"},
        {"role": "model", "message": "Thought 1 I need to divide 20 by 4."},
        {"role": "model", "message": "Action 1 MathActions.divide[a=20, b=4]"},
        {"role": "model", "message": "Observation 1 20 divided by 4 is 5."},
        {"role": "model", "message": "Thought 2 The answer is 5."},
        {"role": "model", "message": "Action 2 Finish[5]"}
    ],
    [
        {"role": "user", "message": "What is the sum of 12 and 30?"},
        {"role": "model", "message": "Thought 1 I need to add 12 and 30."},
        {"role": "model", "message": "Action 1 MathActions.sum[a=12, b=30]"},
        {"role": "model", "message": "Observation 1 The sum of 12 and 30 is 42."},
        {"role": "model", "message": "Thought 2 The answer is 42."},
        {"role": "model", "message": "Action 2 Finish[42]"}
    ],
    [
        {"role": "user", "message": "What is 3 to the power of 4?"},
        {"role": "model", "message": "Thought 1 I need to raise 3 to the power of 4."},
        {"role": "model", "message": "Action 1 MathActions.power[a=3, b=4]"},
        {"role": "model", "message": "Observation 1 3 to the power of 4 is 81."},
        {"role": "model", "message": "Thought 2 The answer is 81."},
        {"role": "model", "message": "Action 2 Finish[81]"}
    ]
]

# Combine all history points
HISTORY_POINTS = SEARCH_HISTORY_POINTS + CALCULATOR_HISTORY_POINTS 