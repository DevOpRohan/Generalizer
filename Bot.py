import asyncio
import json
import re

from openAiApi import OpenAIAPI
from prompts import generalizer_sys_prompt, generalizer_init, generalizer_prompt


class Bot:
    def __init__(self, guidelines, ex_ques, ex_sol, ex_generic_ques, ex_generic_sol, ex_var_const_map):
        self.llm = OpenAIAPI()
        self.guidelines = guidelines
        self.ex_ques = ex_ques
        self.ex_sol = ex_sol
        self.ex_generic_ques = ex_generic_ques
        self.ex_generic_sol = ex_generic_sol
        self.ex_var_const_map = ex_var_const_map

    def parse_raw_string(self, raw_string):
        # Extract the raw values of the 'GENERIC_QUESTION_STRING' and 'GENERIC_SOLUTION_STRING' keys from the last round
        question_string = re.findall(r'GENERIC_QUESTION_STRING": "(.*?)"', raw_string)[-1]
        solution_string = re.findall(r'GENERIC_SOLUTION_STRING": "(.*?)"', raw_string)[-1]

        # Extract the 'variable_constant_map'
        variable_constant_map = re.findall(r'"variable_constant_map": \{(.*?)\}', raw_string)[-1]

        # Return the values as a tuple
        return (question_string, solution_string, variable_constant_map)

    async def generalize(self, problem, solution):
        # 1. Prepare Initial Messages
        messages = [
            {
                "role": "system",
                "content": generalizer_sys_prompt,
            },
            {
                "role": "user",
                "content": generalizer_init.format(guidelines=self.guidelines, ex_ques=self.ex_ques, ex_sol=self.ex_sol,
                                                   ex_generic_ques=self.ex_generic_ques,
                                                   ex_generic_sol=self.ex_generic_sol,
                                                   ex_var_const_map=self.ex_var_const_map)
            },
            {
                "role": "user",
                "content": generalizer_prompt.format(problem=problem, solution=solution)
            }

        ]

        # 2 Return the response
        completion = await self.llm.chat_completion(
            model="gpt-4",
            messages=messages,
            temperature=0,
            max_tokens=2048,
        )
        res = completion.choices[0].message["content"]
        # print(self.load_json(res))
        print(self.parse_raw_string(res))
        print("\n=====================================\n")
        return self.parse_raw_string(res)

    """
    This function will take a list of tuple(ques,sol) and return a list of generalized question-solution pairs.
    Input: ques_sol_list: List of tuple(ques,sol) , batch_size: Number of question-solution pairs to process at a time
    Output: List of generalized question-solution pairs
    """

    async def list_generalizer(self, ques_sol_list, batch_size=25):
        # Initialize an empty list to store the results
        results = []

        # Split the ques_sol_list into batches
        batches = [ques_sol_list[i:i + batch_size] for i in range(0, len(ques_sol_list), batch_size)]

        # Iterate over each batch
        for batch in batches:
            # Use asyncio.gather to call the generalize function on each question-solution pair in the batch
            batch_results = await asyncio.gather(*[self.generalize(ques, sol) for ques, sol in batch])

            # Add the results to the results list
            results.extend(batch_results)

        # Return the results list

        return results
