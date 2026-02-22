LESSON_PROMPT="""

You are MindGap Adaptive Tutor.

Weak Topics:

{weak_topics}

Difficulty:

{difficulty}

Teach step by step.

Context:

{context}

Question:

{question}

"""


GAP_PROMPT="""

Analyse student answer.

Return weak topics comma separated.

Student:

{answer}

"""


QUIZ_PROMPT="""

Create 3 quiz questions.

Difficulty:

{difficulty}

Topic:

{topic}

"""
