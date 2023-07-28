from langchain import PromptTemplate

generalizer_sys_prompt = """You are super intelligent math assistant and expert of Latex.
"""
generalizer_init_prompt = """Imagine a team of two AI experts, a Generalizer and a Verifier, working together to transform a given pair of mathematical question and solution, presented as strings, into a generic format. The transformation should adhere to the following rules:

{guidelines}

Example:
====
QUESTION_STRING:{ex_ques}

SOLUTION_STRING:{ex_sol}

GENERIC_QUESTION_STRING:{ex_generic_ques}

GENERIC_SOLUTION_STRING:{ex_generic_sol}

VARIABLE_CONSTANT_MAP:{ex_var_const_map}
=====

The Generalizer will first attempt to generalize the given question and solution. The Verifier will then check the generalized question and solution to ensure they follow the guidelines. If the Verifier finds any issues, they will provide feedback and the Generalizer will attempt to generalize the question and solution again. This process will continue for a maximum of 2 rounds until the Verifier confirms that the generalized question and solution follow the guidelines.

The ultimate goal of this generalization is to create new problems and solutions by merely altering some values.
"""
generalizer_init_prompt2 = """QUESTION_STRING:
"{problem}"

SOLUTION_STRING:
"{solution}"


=====
Note: 
- The format of generic string must be same as above.
e.g. [string().....] {{string}} is a delimiter.

Always respond in this format: 
```
{{
"rounds": [
    {{
    "round_number": <round_number>,
    "generalizer": {{
        "GENERIC_QUESTION_STRING": "[sting(..), ...],...",
        "GENERIC_SOLUTION_STRING": "[sting(..), ...],..."
    }},
    "verifier": <verification_feedback>
    }},
    {{
    <ROUND_2.....>
    }},
    ..
    ..
    ..
    {{
    <ROUND_n.....>
    }}
],
"variable_constant_map": <generalized_variable(inside val or expr)_constant_map>
}}
```
"""


generalizer_init = PromptTemplate(
    input_variables=["guidelines", "ex_ques", "ex_sol", "ex_generic_ques", "ex_generic_sol", "ex_var_const_map"],
    template=generalizer_init_prompt
)

generalizer_prompt = PromptTemplate(
    input_variables=["problem", "solution"],
    template=generalizer_init_prompt2
)
