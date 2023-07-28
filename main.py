import asyncio
import json

from Bot import Bot

# Fine-tuning on custom guidelines, example
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
        [string(latex(12) でわると latex(6) あまる整数の中で latex(199) に最も近い数を求めなさい。)]
        """,
        """
        [string(求める数は latex(12) の倍数よりも latex(6) 大きい数なので,),string(latex(12 \\\\times \\\\square + 6) と表すことができます。),string(latex((199-6)\\\\div 12 = 16 ) あまり latex(1 ) より,),string(latex(12\\\\times 16+6= \\\\underline{198}) です。latex(\\\\quad \\\\blacktriangleleft 199-1=198) でも可)]
        """
    ),
    (
        """
        [string(latex(8) でわっても, latex(12) でわっても latex(7) あまる latex(3) けたの整数の中で最も小さい数を求めなさい。)]
        """,

        """
        [string(求める数は,latex(\\\\lparen 8) の倍数latex(\\\\rparen +7,~\\\\lparen 12) の倍数latex(\\\\rparen + 7) であることから, latex(\\\\quad \\\\blacktriangleleft) あまりが等しい場合求める数は, latex(\\\\lparen)わる数の公倍数latex(\\\\rparen)latex(+)latex(\\\\lparen)あまりの数 latex(\\\\rparen) ),string(latex(8) と latex(12) の公倍数latex(\\\\lparen\\\\rightarrow 24 ) の倍数latex(\\\\rparen) に, latex(7) を加えた数です。),string(よって, latex(24 \\\\times \\\\square + 7) と表すことができ, latex(3) けたで最も小さい数は,),string(latex(24 \\\\times 4+ 7= \\\\underline{103}) です。)]
        """
    ),
    (
        """
        [string(Có bao nhiêu cặp số tự nhiên latex((x; y)) thỏa mãn latex(4\\\\left(4^{5y}+5y \\\\right)+2003\\\\leq -x^2+2000x+\\\\log_{4}\\\\left[(x-1999)^{4} (1-x)^{4} \\\\right] )?)]
        """,

        """
        [string(Để bất đẳng thức đã cho luôn đúng thì),string(ĐKlatex(\\\\colon ( x -1999)^{4}(1- x )^{4}>0) ),string(latex((x-1999)(1-x)>0) ),string(latex(1< x <1999) ),string(latex(x \\\\in N \\\\implies 2 \\\\leq x \\\\leq 1998).),string(Coi như,),string(latex(4\\\\left(4^{5 y}+5 y\\\\right)+2003 \\\\leq-x^{2}+2000 x+\\\\log _{4}\\\\left[(x-1999)^{4}(1-x)^{4}\\\\right]) ),string(latex(4\\\\cdot 4^{5 y}+20 y+2003 \\\\leq-x^{2}+2000 x+4 \\\\log _{4}(x-1999)(1-x)) ),string(latex(4^{5 y+1}+4(5 y+1) \\\\leq-x^{2}+2000 x-1999+4 \\\\log _{4}\\\\left(-x^{2}+2000 x-1999\\\\right) \\\\qquad \\\\ldots\\\\ldots (i) ) ),string(Đặt latex(u =\\\\log _{4}\\\\left(- x ^{2}+2000 x -1999\\\\right) \\\\Leftrightarrow 4^{u}=\\\\left(- x ^{2}+2000 x -1999\\\\right)) ),string(latex((i)) Trở thành latex(4^{5 y+1}+4(5 y+1) \\\\leq 4^{u}+4 u \\\\qquad \\\\qquad \\\\ldots\\\\ldots (ii) )),string(Xét hàm số),string(latex(f(t)=4^{t}+4 t)),string(latex( f^{\\\\prime}(t)=4^{t} \\\\cdot \\\\ln 4+4>0~ \\\\forall t \\\\Rightarrow f(t)) là hàm số đồng biến trên latex(R)),string(latex(f(5 y+1) \\\\leq f(u))),string(latex(5 y+1 \\\\leq u \\\\qquad \\\\ldots \\\\ldots (iii))),string(latex(5 y+1 \\\\leq \\\\log _{4}\\\\left(-x^{2}+2000 x-1999\\\\right))),string(Xét hàm số latex(g(x)=-x ^{2}+2000x -1999),  với latex(2 \\\\leq x \\\\leq 1998).),string(latex(g^{\\\\prime}(x)=-2 x+2000)),string(latex( g^{\\\\prime}=0 \\\\Leftrightarrow x=1000)),string(latex(g(2)=g(1998)=1997 )),string(latex( g(1000)= 998001 \\\\Rightarrow g(x) \\\\leq 998001 )),string(Do đó latex(5 y+1 \\\\leq \\\\log _{4}(998001) )),string(latex(5y+1\\\\leq 9.96 )),string(latex(5y\\\\leq 9.96-1 )),string(latex(y\\\\leq \\\\dfrac{8.96}{5} )),string(latex(y\\\\leq 1.79 )),string(latex(y\\\\in N \\\\implies y\\\\in \\\\{0;1\\\\} )),string(Thay latex(y=0) vào latex((iii))),string(latex(u\\\\geq  1)),string(latex(4^{u}\\\\geq 4 )),string(latex(-x^2+2000x-1999\\\\geq 4)),string(latex(-x^2+2000x-2003\\\\geq 0)),string(latex( 1.002 \\\\leq x \\\\leq 1998.99799 )),string(latex(x\\\\in \\\\{2, 3,\\\\ldots \\\\ldots, 1998 \\\\}) có latex(1997 ) số tự nhiên),string(Với latex(y = 1) ),string(latex(u\\\\geq 6)),string(latex(4^{u}\\\\geq 4^{6})),string(latex(-x^2+2000x-1999\\\\geq 4096 )),string(latex(-x^2+2000x-6095\\\\geq 0 )),string(latex(3.05215 \\\\leq x\\\\leq 1996.94784 )),string(latex(x\\\\in \\\\{ 4, 5,\\\\ldots \\\\ldots, 1996 \\\\}) có latex(1993 ) số tự nhiên.),string(Kết luận có latex(3990 ) cặp số tự nhiên latex((x; y)) thỏa đề bài.),string(Hence, the fourth option is correct.)]
        """
    ),
    (
        """
        [string(Cho hàm số latex(f(x)) liên tục trên latex(\\\\R). Biết latex(f(x)) có đạo hàm là latex(f^{\\\\prime}(x)=x^{8}+2) và latex(f(1)=2). Khi đó latex(\\displaystyle\\int_{0}^{2} f\\\\left(\\\\dfrac{x}{2}\\\\right) d x) bằng)]
        """,
        """
        [string(Xét latex(\\displaystyle\\int_{0}^{2} f \\\\left(\\\\dfrac{x}{2} \\\\right) d x),  đặt latex(t=\\\\dfrac{x}{2} \\\\Rightarrow d t=\\\\dfrac{d x}{2})),string(Đổi cậnlatex(\\\\colon x=0),  latex(t=0)), string(latex(\\\\qquad\\\\quad x=2),  latex(t=1)), string(Suy ra, latex(\\displaystyle\\int_{0}^{2} f \\\\left(\\\\dfrac{x}{2}\\\\right) d x=\\displaystyle\\int_{0}^{1} 2 f(t) d t)),string(Xét latex(\\displaystyle\\int_{0}^{1} f(t) d t),  đặt latex(u = f(t)),  latex(du= f'(t)dt) và latex(dv= 2dt),  latex(v = 2t)),custom_evaluation_expression(lhs([string(latex(\\displaystyle\\int_{0}^{1} 2f(t) d t))]),  rhs([string(latex(\\\\left. 2 t \\\\cdot f(t)\\\\right|_{0} ^{1}-\\displaystyle\\int_{0}^{1} 2t \\\\cdot f^{\\\\prime}(t) d t)), string(latex(2(1)(2)-\\displaystyle\\int_{0}^{1} 2t\\\\left(t^{8}+2 \\\\right) d t)), string(latex(4-\\displaystyle\\int_{0}^{1} \\\\left(2t^{9}+4t \\\\right) d t)), string(latex(4- \\\\left.\\\\left(\\\\dfrac{t^{10}}{5}+2t^{2} \\\\right)\\\\right|_{0}^{1})), string(latex(4-\\\\dfrac{1}{5}-2 )), string(latex(2-\\\\dfrac{1}{5})), string(latex(\\\\dfrac{9}{5}))]),equating(latex(=))),string(Hence, the fourth option is correct.)]
        """
    ),
    (
        """
        [string(Suppose the average weight of adults is latex(123) pounds and the average weight of minors is latex(79) pounds.)]
        SUBPARTS:
        A. [string(Choose the function that relates the total weight latex(T(a)) with the number of adults latex((a)).)]
        B. [string(Choose the function that relates the total weight latex(M(b)) with the number of minors latex((b)).)]
        """,
        """
        A. [string(Average weight of adults latex(=) latex(\\\\\\\\dfrac{\\\\\\\\text{Total~weight~of~adults}}{\\\\\\\\text{Number~of ~adults}})),string(According to the question,),string(latex(123=\\\\\\\\dfrac{T(a)}{a})),string(latex(T(a)=123a)),string(Hence, the second option is correct.)]
        B. [string(Average weight of minors latex(=) latex(\\\\\\\\dfrac{\\\\\\\\text{Total ~weight ~of ~minors}}{\\\\\\\\text{Number ~of ~minors}})),string(According to the question,),string(latex(79=\\\\\\\\dfrac{M(b)}{b})),string(latex(M(b)=79b)),string(Hence, the first option is correct.)]
        """
    )
]

bot = Bot(guidelines, example_original_question_string, example_original_solution_string,
          example_generic_question_string, example_generic_solution_string, example_variable_constant_map)

generic_list = asyncio.run(bot.list_generalizer(original_list))
