# Stores example history points for prompting the fact checker chat and thought trace generator
from llm.models.history import HistoryPoint
from actions import ACTION_SETS


available_actions = []
for action_cls in ACTION_SETS:
    available_actions.extend(action_cls.list_actions())


GENERAL_INSTRUCTIONS_HISTORY_POINTS: list[HistoryPoint] = [
    HistoryPoint(
        role="user",
        message=f"You are a helpful assistant that can answer questions and help with tasks that involve searching the web or performing calculations.",
    ),
    HistoryPoint(
        role="user",
        message=f"Here are the available actions: {available_actions}",
    ),
    HistoryPoint(
        role="user",
        message=f"Make sure to always use the actions within each thought.",
    ),
    HistoryPoint(
        role="user",
        message=f"Here are some prompt examples from previous conversations:",
    ),
    HistoryPoint(
        role="user",
        message="Only consider the answer as finished if you have answered the question asked by user in [INITIAL_PROMPT]. Set is_finished to True if [FINISH]",
    ),
]

SEARCH_HISTORY_POINTS = [
    # Example 1
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I need to search Colorado orogeny, find the area that the eastern sector of the Colorado orogeny extends into, then find the elevation range of the area.",
    ),
    HistoryPoint(
        role="model", message="Action 1 SearchActions.search[entity=Colorado orogeny]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 It does not mention the eastern sector. So I need to look up eastern sector.",
    ),
    HistoryPoint(
        role="model",
        message="Action 2 SearchActions.lookup[entity=Colorado orogeny, string=eastern sector]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 2 (Result 1 / 1) The eastern sector extends into the High Plains and is called the Central Plains orogeny.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 3 The eastern sector of Colorado orogeny extends into the High Plains. So I need to search High Plains and find its elevation range.",
    ),
    HistoryPoint(
        role="model", message="Action 3 SearchActions.search[entity=High Plains]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 3 High Plains refers to one of two distinct land regions",
    ),
    HistoryPoint(
        role="model",
        message="Thought 4 I need to instead search High Plains (United States).",
    ),
    HistoryPoint(
        role="model",
        message="Action 4 SearchActions.search[entity=High Plains (United States)]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 4 The High Plains are a subregion of the Great Plains. From east to west, the High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130 m).[3]",
    ),
    HistoryPoint(
        role="model",
        message="Thought 5 High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft.",
    ),
    HistoryPoint(role="model", message="Action 5 Finish[1,800 to 7,000 ft]"),
    # Example 2
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] Musician and satirist Allie Goertz wrote a song about the 'The Simpsons' character Milhouse, who Matt Groening named after who?",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 The question simplifies to 'The Simpsons' character Milhouse is named after who. I only need to search Milhouse and find who it is named after.",
    ),
    HistoryPoint(
        role="model", message="Action 1 SearchActions.search[entity=Milhouse]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 The paragraph does not tell who Milhouse is named after, maybe I can look up 'named after'.",
    ),
    HistoryPoint(
        role="model",
        message="Action 2 SearchActions.lookup[entity=Milhouse, string=named after]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 2 (Result 1 / 1) Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 3 Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.",
    ),
    HistoryPoint(role="model", message="Action 3 Finish[Richard Nixon]"),
    # Example 3
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I need to search Adam Clayton Powell and The Saimaa Gesture, and find which documentary is about Finnish rock groups.",
    ),
    HistoryPoint(
        role="model",
        message="Action 1 SearchActions.search[entity=Adam Clayton Powell]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Could not find [Adam Clayton Powell]. Similar: [’Adam Clayton Powell III’, ’Seventh Avenue (Manhattan)’, ’Adam Clayton Powell Jr. State Office Building’, ’Isabel Washington Powell’, ’Adam Powell’, ’Adam Clayton Powell (film)’, ’Giancarlo Esposito’].",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 To find the documentary, I can search Adam Clayton Powell (film).",
    ),
    HistoryPoint(
        role="model",
        message="Action 2 SearchActions.search[entity=Adam Clayton Powell (film)]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 2 Adam Clayton Powell is a 1989 American documentary film directed by Richard Kilberg. The film is about the rise and fall of influential African-American politician Adam Clayton Powell Jr.[3][4] It was later aired as part of the PBS series The American Experience.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 3 Adam Clayton Powell (film) is a documentary about an African-American politician, not Finnish rock groups. So the documentary about Finnish rock groups must instead be The Saimaa Gesture.",
    ),
    HistoryPoint(role="model", message="Action 3 Finish[The Saimaa Gesture]"),
    # Example 4
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] What profession does Nicholas Ray and Elia Kazan have in common?",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I need to search Nicholas Ray and Elia Kazan, find their professions, then find the profession they have in common.",
    ),
    HistoryPoint(
        role="model", message="Action 1 SearchActions.search[entity=Nicholas Ray]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 - June 16, 1979) was an American film director, screenwriter, and actor best known for the 1955 film Rebel Without a Cause.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 Professions of Nicholas Ray are director, screenwriter, and actor. I need to search Elia Kazan next and find his professions.",
    ),
    HistoryPoint(
        role="model", message="Action 2 SearchActions.search[entity=Elia Kazan]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 2 Elia Kazan was an American film and theatre director, producer, screenwriter and actor.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 3 Professions of Elia Kazan are director, producer, screenwriter, and actor. So profession Nicholas Ray and Elia Kazan have in common is director, screenwriter, and actor.",
    ),
    HistoryPoint(
        role="model", message="Action 3 Finish[director, screenwriter, actor]"
    ),
    # Example 5
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] Which magazine was started first Arthur's Magazine or First for Women?",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I need to search Arthur's Magazine and First for Women, and find which was started first.",
    ),
    HistoryPoint(
        role="model", message="Action 1 SearchActions.search[entity=Arthur's Magazine]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Arthur's Magazine (1844-1846) was an American literary periodical published in Philadelphia in the 19th century.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 Arthur's Magazine was started in 1844. I need to search First for Women next.",
    ),
    HistoryPoint(
        role="model", message="Action 2 SearchActions.search[entity=First for Women]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 2 First for Women is a woman's magazine published by Bauer Media Group in the USA.[1] The magazine was started in 1989.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 3 First for Women was started in 1989. 1844 (Arthur's Magazine) < 1989 (First for Women), so Arthur's Magazine was started first.",
    ),
    HistoryPoint(role="model", message="Action 3 Finish[Arthur's Magazine]"),
    # Example 6
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] Were Pavel Urysohn and Leonid Levin known for the same type of work?",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I need to search Pavel Urysohn and Leonid Levin, find their types of work, then find if they are the same.",
    ),
    HistoryPoint(
        role="model", message="Action 1 SearchActions.search[entity=Pavel Urysohn]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Pavel Samuilovich Urysohn (February 3, 1898 - August 17, 1924) was a Soviet mathematician who is best known for his contributions in dimension theory.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 Pavel Urysohn is a mathematician. I need to search Leonid Levin next and find its type of work.",
    ),
    HistoryPoint(
        role="model", message="Action 2 SearchActions.search[entity=Leonid Levin]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 2 Leonid Anatolievich Levin is a Soviet-American mathematician and computer scientist.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 3 Leonid Levin is a mathematician and computer scientist. So Pavel Urysohn and Leonid Levin have the same type of work.",
    ),
    HistoryPoint(role="model", message="Action 3 Finish[yes]"),
    # Example 7
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] Determine if there is Observation that SUPPORTS or REFUTES a Claim, or if there is NOT ENOUGH INFORMATION. Claim Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I need to search Nikolaj Coster-Waldau and find if he has worked with the Fox Broadcasting Company.",
    ),
    HistoryPoint(
        role="model",
        message="Action 1 SearchActions.search[entity=Nikolaj Coster-Waldau]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Nikolaj William Coster-Waldau (born 27 July 1970) is a Danish actor and producer. He graduated from the Danish National School of Performing Arts in Copenhagen in 1993,[1], and had his breakthrough role in Denmark with the film Nightwatch (1994). He played Jaime Lannister in the HBO fantasy drama series Game of Thrones, for which he received two Primetime Emmy Award nominations for Outstanding Supporting Actor in a Drama Series.. Coster-Waldau has appeared in numerous films in his native Denmark and Scandinavia, including Headhunters (2011) and A Thousand Times Good Night (2013). In the U.S, his debut film role was in the war film Black Hawk Down (2001), playing Medal of Honor recipient Gary Gordon.[2] He then played a detective in the short-lived Fox television series New Amsterdam (2008), and appeared in the 2009 Fox television film Virtuality, originally intended as a pilot.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 Because he 'appeared in the 2009 Fox television film Virtuality', he should have worked with the Fox Broadcasting Company.",
    ),
    HistoryPoint(role="model", message="Action 2 Finish[SUPPORTS]"),
    # Example 8
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] Claim Stranger Things is set in Bloomington, Indiana.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I should search for Stranger Things, and see if it is set in Bloomington, Indiana.",
    ),
    HistoryPoint(
        role="model", message="Action 1 SearchActions.search[entity=Stranger Things]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Stranger Things is an American science fiction horror drama television series created by the Duffer Brothers. Set in the 1980s, primarily in the fictional town of Hawkins, Indiana, the series centers on a number of mysteries and supernatural events occurring around the town and their impact on an ensemble of child and adult characters.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 The observation says that it is set in a 'fictional town of Hawkins, Indiana', so it is not set in Bloomington.",
    ),
    HistoryPoint(role="model", message="Action 2 Finish[REFUTES]"),
    # Example 9 (for Billboard Hot 100)
    HistoryPoint(
        role="user",
        message="[INITIAL_PROMPT] Claim Beautiful reached number two on the Billboard Hot 100 in 2003.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 1 I need to search the song Beautiful and find if it reached number two on the Billboard Hot 100 in 2003.",
    ),
    HistoryPoint(
        role="model", message="Action 1 SearchActions.search[entity=Beautiful]"
    ),
    HistoryPoint(
        role="model",
        message="Observation 1 Could not find [Beautiful]. Similar: [’Beautiful’, ’Beautiful, Beautiful’, ’A Beautiful Mind (film)’, ’Beautiful (Christina Aguilera song)’, ’Life Is Beautiful’].",
    ),
    HistoryPoint(
        role="model",
        message="Thought 2 From suggestions, I should search 'Beautiful (Christina Aguilera song)' to find the song.",
    ),
    HistoryPoint(
        role="model",
        message="Action 2 SearchActions.search[entity=Beautiful (Christina Aguilera song)]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 2 'Beautiful' is a song recorded by American singer Christina Aguilera for her fourth studio album, Stripped (2002).",
    ),
    HistoryPoint(
        role="model",
        message="Thought 3 It does not mention Billboard, so I need to look up 'Billboard Hot 100' to find if it reached number two on it in 2003.",
    ),
    HistoryPoint(
        role="model",
        message="Action 3 SearchActions.lookup[entity=Beautiful (Christina Aguilera song), string=Billboard Hot 100]",
    ),
    HistoryPoint(
        role="model",
        message="Observation 3 (Result 1 / 3) The song peaked at number two on the Billboard Hot 100 in the United States, where it was certified Gold for 500,000 units shipped.",
    ),
    HistoryPoint(
        role="model",
        message="Thought 4 It only says the song peaked at number two on the Billboard Hot 100, but not if it was in 2003. I am not sure if this claim is true or not.",
    ),
    HistoryPoint(role="model", message="Action 4 Finish[NOT ENOUGH INFO]"),
]

CALCULATOR_HISTORY_POINTS = [
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is the sum of 5 and 7?"),
    HistoryPoint(role="model", message="Thought 1 I need to add 5 and 7."),
    HistoryPoint(role="model", message="Action 1 MathActions.sum[a=5, b=7]"),
    HistoryPoint(role="model", message="Observation 1 The sum of 5 and 7 is 12."),
    HistoryPoint(role="model", message="Thought 2 The answer is 12."),
    HistoryPoint(role="model", message="Action 2 Finish[12]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 10 divided by 2?"),
    HistoryPoint(role="model", message="Thought 1 I need to divide 10 by 2."),
    HistoryPoint(role="model", message="Action 1 MathActions.divide[a=10, b=2]"),
    HistoryPoint(role="model", message="Observation 1 10 divided by 2 is 5."),
    HistoryPoint(role="model", message="Thought 2 The answer is 5."),
    HistoryPoint(role="model", message="Action 2 Finish[5]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 15 minus 4?"),
    HistoryPoint(role="model", message="Thought 1 I need to subtract 4 from 15."),
    HistoryPoint(role="model", message="Action 1 MathActions.subtract[a=15, b=4]"),
    HistoryPoint(role="model", message="Observation 1 15 minus 4 is 11."),
    HistoryPoint(role="model", message="Thought 2 The answer is 11."),
    HistoryPoint(role="model", message="Action 2 Finish[11]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 6 times 8?"),
    HistoryPoint(role="model", message="Thought 1 I need to multiply 6 by 8."),
    HistoryPoint(role="model", message="Action 1 MathActions.multiply[a=6, b=8]"),
    HistoryPoint(role="model", message="Observation 1 6 times 8 is 48."),
    HistoryPoint(role="model", message="Thought 2 The answer is 48."),
    HistoryPoint(role="model", message="Action 2 Finish[48]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 2 to the power of 5?"),
    HistoryPoint(
        role="model", message="Thought 1 I need to raise 2 to the power of 5."
    ),
    HistoryPoint(role="model", message="Action 1 MathActions.power[a=2, b=5]"),
    HistoryPoint(role="model", message="Observation 1 2 to the power of 5 is 32."),
    HistoryPoint(role="model", message="Thought 2 The answer is 32."),
    HistoryPoint(role="model", message="Action 2 Finish[32]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 100 minus 33?"),
    HistoryPoint(role="model", message="Thought 1 I need to subtract 33 from 100."),
    HistoryPoint(role="model", message="Action 1 MathActions.subtract[a=100, b=33]"),
    HistoryPoint(role="model", message="Observation 1 100 minus 33 is 67."),
    HistoryPoint(role="model", message="Thought 2 The answer is 67."),
    HistoryPoint(role="model", message="Action 2 Finish[67]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 9 times 9?"),
    HistoryPoint(role="model", message="Thought 1 I need to multiply 9 by 9."),
    HistoryPoint(role="model", message="Action 1 MathActions.multiply[a=9, b=9]"),
    HistoryPoint(role="model", message="Observation 1 9 times 9 is 81."),
    HistoryPoint(role="model", message="Thought 2 The answer is 81."),
    HistoryPoint(role="model", message="Action 2 Finish[81]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 20 divided by 4?"),
    HistoryPoint(role="model", message="Thought 1 I need to divide 20 by 4."),
    HistoryPoint(role="model", message="Action 1 MathActions.divide[a=20, b=4]"),
    HistoryPoint(role="model", message="Observation 1 20 divided by 4 is 5."),
    HistoryPoint(role="model", message="Thought 2 The answer is 5."),
    HistoryPoint(role="model", message="Action 2 Finish[5]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is the sum of 12 and 30?"),
    HistoryPoint(role="model", message="Thought 1 I need to add 12 and 30."),
    HistoryPoint(role="model", message="Action 1 MathActions.sum[a=12, b=30]"),
    HistoryPoint(role="model", message="Observation 1 The sum of 12 and 30 is 42."),
    HistoryPoint(role="model", message="Thought 2 The answer is 42."),
    HistoryPoint(role="model", message="Action 2 Finish[42]"),
    HistoryPoint(role="user", message="[INITIAL_PROMPT] What is 3 to the power of 4?"),
    HistoryPoint(
        role="model", message="Thought 1 I need to raise 3 to the power of 4."
    ),
    HistoryPoint(role="model", message="Action 1 MathActions.power[a=3, b=4]"),
    HistoryPoint(role="model", message="Observation 1 3 to the power of 4 is 81."),
    HistoryPoint(role="model", message="Thought 2 The answer is 81."),
    HistoryPoint(role="model", message="Action 2 Finish[81]"),
]

# Combine all history points
PROMPTING_EXAMPLES_HISTORY_POINTS: list[HistoryPoint] = (
    SEARCH_HISTORY_POINTS + CALCULATOR_HISTORY_POINTS
)
