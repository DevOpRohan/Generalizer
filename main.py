# Fine-tuning on custom guidelines, example
import asyncio

from Bot import Bot

# 1. You can add some custom guidelines in this string (start from 5. )
guidelines = """
1. Variable names should be kept as they are.
2. Constants should be replaced with val(a), val(b), val(c), etc., in the order they appear.
3. Any calculations or expressions that need to be evaluated should be formatted as expr(a+b-c).
4. Ensure to use val() and expr() correctly and logically. 
"""

# 2. Add a example to get more fine-tuned response.
# Like if you add example related to quadratic equation, you will get better & fine-tuned response for quadratic equations related string.
# For example, you have to add question_string, solution_string, generic_question_string, generic_solution_string, variable_constant_map

example_original_question_string = """
[string(The coefficient of latex(t^{7} )in the expansion of latex(\\\\bigg(\\\\dfrac{1 - t^{10} }{1 - t}\\\\bigg)^{3}) is)]
"""
example_original_solution_string = """
[string(Clearly, latex(\\\\bigg(\\\\dfrac{1 - t^{10}}{1 - t}\\\\bigg)^{3} = (1 - t^{10})^{3}(1 - t)^{- 3})),string(latex(\\\\therefore) coefficient of latex(t^{7} ) in latex( (1 - t^{10})^{3}(1 - t)^{- 3})),string(latex(\\\\Rightarrow) coefficient of latex(t^{7}) in latex(\\\\lparen 1 - t^{30} - 3{t^{10}} + 3t^{20} \\\\rparen (1 - t)^{- 3})),string(latex(\\\\Rightarrow) coefficient of latex(t^{7}) in latex((1 - t)^{- 3})),string(latex(\\\\Rightarrow) latex(^{3 + 7 - 1}C_{7} = ^{9}C_{7} = 36 \\\\quad \\\\lparen \\\\because) coefficient of latex(x^{r}) in latex(\\\\lparen 1-x \\\\rparen^{-n} ~=~ ^{n+r-1}C_{r} \\\\rparen)),string(Hence, the fourth option is correct.)]
"""
example_generic_question_string = """
[string(The coefficient of latex(t^{val(p)} )in the expansion of latex(\\bigg(\\dfrac{1 - t^{val(q)} }{1 - t}\\bigg)^{3}) is)]
"""

example_generic_solution_string = """
[string(Clearly, latex(\\bigg(\\dfrac{1 - t^{val(q)}}{1 - t}\\bigg)^{3} = (1 - t^{val(q)})^{3}(1 - t)^{- 3})),string(latex(\\therefore) coefficient of latex(t^{val(p)} ) in latex( (1 - t^{val(q)})^{3}(1 - t)^{- 3})),string(latex(\\Rightarrow) coefficient of latex(t^{val(p)}) in latex(\\lparen 1 - t^{expr(3*q)} - 3{t^{val(q)}} + 3t^{expr(2*q)} \\rparen (1 - t)^{- 3})),string(latex(\\Rightarrow) coefficient of latex(t^{val(p)}) in latex((1 - t)^{- 3})),string(latex(\\Rightarrow) latex(^{3 + val(p) - 1}C_{val(p)} = ^{expr(3+p-1)}C_{val(p)} = expr(binomial((3+p-1),p)) \\quad \\lparen \\because) coefficient of latex(x^{r}) in latex(\\lparen 1-x \\rparen^{-n} ~=~ ^{n+r-1}C_{r} \\rparen))]
"""
example_variable_constant_map = """
VARIABLE_CONSTANT_MAP: {p: 7, q:10}
"""

# List  of tuples of Ques-Sol
original_list = [
    (
        """
        [,string(Robert's electronics shop buys headphones at a wholesale price of latex(\\$ 113).),string(If the markup rate at Robert's electronics shop is latex(45 \\%), what is the markup for the headphones?),]
        """,
        """
        [string(The amount of markup can be found with the following equation.),string(Markup rate latex(\\times) wholesale price latex(=) amount of markup),string(Since markup rate is a percentage, we have to convert it into a decimal first.),string(So, latex(45 \\%=\\dfrac{45}{100}=0.45)),string(Now, using the formula and substituting the values, we get latex(0.45 \\times \\$ 113=\\$ 50.85)),string(Therefore, the amount of markup on the headphones is latex(\\$ 50.85).)]
        """
    ),
    (
        """
        [string(The bookstore is having a latex(20\\%) off sale on all of its books.),string(If the book you want to purchase costs latex(\\$18), what is the markdown for the book?)]
        """,

        """
        [string(The amount of markdown can be found with the following equation.),string(Markdown rate latex(\\times) original price latex(=) amount of markdown),string(Since the markdown rate is a percentage, we have to convert it into a decimal first.),string(So, latex(20 \\%=\\dfrac{20}{100}=0.20)),string(Now, using the formula and substituting the values, we get latex(0.20 \\times \\$ 18=\\$ 3.60)),string(Therefore, the amount of markdown for the book is latex(\\$ 3.60).)]
        """
    ),
    (
        """
        [string(Sophia works at a reputable art gallery. She earns a commission of latex(6\\%) on every artwork she sells. If she sells a painting for latex(\\$764), how much money does Sophia make in commission?)]
        """,

        """
        [string(To find the amount of commission made, use the following formula Commission rate latex(\\times) retail price latex(=) amount of commission made Since the commission rate is a percentage, we have to convert it into a decimal first. So, latex(6 \\%=\\dfrac{6}{100}=0.06)),string(Now, using the formula and substituting the values, we get latex(0.06 \\times \\$ 764=\\$ 45.84)),string(Therefore, the amount of commission Sophia makes by selling a computer is latex(\\$ 45.84).)]
        """
    ),
    (
        """
        [string(In San Francisco, California, stores charge a latex(3.65\\%) city sales tax and a latex(4.6\\%) state sales tax. Emma is purchasing a smartwatch at latex(\\$220) before tax.),string(How much sales tax does Emma pay for her smartwatch purchase?)]
        """,
        """
        [,string(We have to convert the percentage of tax into a decimal first.),string(latex(4.6 \\%=\\dfrac{4.6}{100}=0.046)),string(latex(3.65 \\%=\\dfrac{3.65}{100}=0.0365)),string(Since both sales tax rates apply to latex(\\$ 220), we can add the two rates.),string(latex(0.046+0.0365=0.0825)),string(latex(0.0825 \\times \\$ 220=\\$ 18.15)),string(Emma pays latex(\\$ 18.15) in sales tax for her smartwatch purchase.),]
        """
    ),
    (
        """
        [string(Anna has dinner at a fancy restaurant and the cost of her meal is latex(\\$36.00). Due to the exceptional service, she decides to leave a latex(15\\%) tip.),string(What is her total bill including tip?)]
        """,
        """
       [,string(The tip is a percentage, we have to convert it into a decimal first.),string(So, latex(15 \\%=\\dfrac{15}{100}=0.15)),evaluation_expression(lhs([string(The tip amount)]),rhs([string(latex(0.15 \\times \\$ 36)),string(latex(\\$ 5.4))])),string(Now calculate the total bill, we get),evaluation_expression(lhs([string(Total bill)]),rhs([string(latex(\\$ 36+\\$ 5.4)),string(latex(\\$ 41.4))])),string(Therefore, the total bill is latex(\\$ 41.4).),] 
        """
    )
]

bot = Bot(guidelines, example_original_question_string, example_original_solution_string,
          example_generic_question_string, example_generic_solution_string, example_variable_constant_map)

generic_list = asyncio.run(bot.list_generalizer(original_list))
#
# # Print each generalized question-solution pair
# for i in range(len(generic_list)):
#     print("======================================\nQUES_SOL_PAIR: ", i + 1)
#     print("Question_String: ", """\n""" + original_list[i][0])
#     print("Solution_String: ", """\n""" +  original_list[i][1])
#     print("Generic_Question_String: ", """\n""" + generic_list[i])
#     print("\n")

#Print in the text file
with open("generic_questions.txt", "w") as f:
    for i in range(len(generic_list)):
        f.write("======================================\nQUES_SOL_PAIR: " + str(i + 1))
        f.write("\nQuestion_String: \n" + original_list[i][0])
        f.write("\nSolution_String: \n" + original_list[i][1])
        f.write("\nGeneric_Question_String: \n" + generic_list[i])
        f.write("\n\n")