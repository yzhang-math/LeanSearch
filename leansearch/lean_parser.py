from lark import Lark, Transformer, Tree
from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Any

@dataclass
class LeanIdentifier:
    name: str
    
@dataclass
class LeanType:
    name: str
    params: List['LeanType'] = None
    
@dataclass
class LeanParam:
    name: str
    type: LeanType

@dataclass
class LeanTactic:
    name: str
    args: List[str] = None

@dataclass
class LeanTheorem:
    name: str
    params: List[LeanParam]
    type: str
    proof: List[LeanTactic]

@dataclass
class LeanDefinition:
    name: str
    params: List[LeanParam]
    return_type: Optional[LeanType]
    body: str

# Grammar for basic Lean syntax
lean_grammar = """
    ?start: statement+

    statement: theorem | definition
    
    theorem: "theorem" NAME params? ":" term (":=" proof)?
    definition: "def" NAME params? (":" type)? ":=" term
    
    params: "(" param ("," param)* ")"
    param: NAME+ ":" type
    
    type: NAME ("<" type ("," type)* ">")?
    term: simple_term (operator simple_term)*
    ?simple_term: NAME | STRING | term_with_args | "(" term ")"
    term_with_args: NAME simple_term+
    operator: "+" | "-" | "*" | "/" | "=" | "≠" | "≤" | "≥" | "<" | ">" | "∧" | "∨" | "→" | "↔" | "∈" | "∉" | "⊆" | "⊂" | "∪" | "∩"
    
    proof: "by" tactic+
    ?tactic: NAME term* | tactic_block
    tactic_block: "{" tactic+ "}"
    
    NAME: /[a-zA-Z_][a-zA-Z0-9_']*/
    STRING: /"[^"]*"/
    COMMENT: /--[^\\n]*/
    WS: /[ \\t\\f\\r\\n]/+
    
    %ignore WS
    %ignore COMMENT
"""

class LeanTransformer(Transformer):
    def NAME(self, token):
        return str(token)
        
    def STRING(self, token):
        return str(token)[1:-1]  # Remove quotes
        
    def param(self, items):
        names = items[:-1]  # All but last item are names
        type_node = items[-1]  # Last item is the type
        return [LeanParam(name=name, type=type_node) for name in names]
        
    def params(self, items):
        # Flatten the list of params since each param can produce multiple params
        return [param for params in items for param in params]
        
    def type(self, items):
        name = items[0]
        params = items[1:] if len(items) > 1 else None
        return LeanType(name=name, params=params)
        
    def term(self, items):
        # Interleave terms and operators
        result = []
        for i, item in enumerate(items):
            if i > 0:
                result.append(" ")
            result.append(str(item))
            if i < len(items) - 1:
                result.append(" ")
        return "".join(result)
        
    def term_with_args(self, items):
        return " ".join(str(i) for i in items)
        
    def operator(self, items):
        return str(items[0])
        
    def tactic(self, items):
        name = items[0]
        args = items[1:] if len(items) > 1 else None
        return LeanTactic(name=str(name), args=[str(arg) for arg in args] if args else None)
        
    def tactic_block(self, items):
        return items
        
    def proof(self, items):
        # Flatten tactic blocks
        tactics = []
        for item in items:
            if isinstance(item, list):
                tactics.extend(item)
            else:
                tactics.append(item)
        return tactics
        
    def theorem(self, items):
        name = items[0]
        
        # Find params, type and proof
        params = []
        type_term = None
        proof_tactics = []
        
        for item in items[1:]:
            if isinstance(item, list) and all(isinstance(x, LeanParam) for x in item):
                params = item
            elif isinstance(item, list) and all(isinstance(x, LeanTactic) for x in item):
                proof_tactics = item
            else:
                type_term = str(item)
                
        return LeanTheorem(
            name=name,
            params=params,
            type=type_term,
            proof=proof_tactics
        )
        
    def definition(self, items):
        name = items[0]
        params = []
        return_type = None
        body = None
        
        for item in items[1:]:
            if isinstance(item, list) and all(isinstance(x, LeanParam) for x in item):
                params = item
            elif isinstance(item, LeanType):
                return_type = item
            else:
                body = str(item)
                
        return LeanDefinition(
            name=name,
            params=params,
            return_type=return_type,
            body=body
        )

class LeanParser:
    def __init__(self):
        self.parser = Lark(lean_grammar, parser='lalr', transformer=LeanTransformer())
        
    def parse(self, code: str) -> List[Union[LeanTheorem, LeanDefinition]]:
        """Parse Lean code and return a list of parsed statements"""
        try:
            return self.parser.parse(code)
        except Exception as e:
            raise ValueError(f"Failed to parse Lean code: {str(e)}")
            
    def parse_theorem(self, code: str) -> LeanTheorem:
        """Parse a single theorem"""
        results = self.parse(code)
        if not results or not isinstance(results[0], LeanTheorem):
            raise ValueError("Code does not contain a theorem")
        return results[0]
        
    def parse_definition(self, code: str) -> LeanDefinition:
        """Parse a single definition"""
        results = self.parse(code)
        if not results or not isinstance(results[0], LeanDefinition):
            raise ValueError("Code does not contain a definition")
        return results[0]

# Example usage
if __name__ == "__main__":
    parser = LeanParser()
    
    # Example theorem
    theorem_code = """
    theorem add_zero (n : Nat) : n + 0 = n := by {
        rfl
        apply nat.zero_add
        simp
    }
    """
    
    # Example definition
    def_code = """
    def factorial (n : Nat) : Nat :=
        match n with
        | 0 => 1
        | n + 1 => (n + 1) * factorial n
    """

    test_code = """--@funsearch.evolve
    theorem pi_eq_sum_univ_v3 {ι : Type*} [Fintype ι] [DecidableEq ι] {R : Type*} [Semiring R] (x : ι → R) : x = ∑ i, (x i) • fun j => if i = j then (1 : R) else 0 := by 
    ext 
    simp"""
    
    try:
        # Parse theorem
        theorem = parser.parse_theorem(test_code)
        print("Parsed theorem:")
        print(f"Name: {theorem.name}")
        print(f"Parameters: {theorem.params}")
        print(f"Type: {theorem.type}")
        print(f"Proof tactics: {theorem.proof}")
        
        # Parse definition
        definition = parser.parse_definition(def_code)
        print("\nParsed definition:")
        print(f"Name: {definition.name}")
        print(f"Parameters: {definition.params}")
        print(f"Return type: {definition.return_type}")
        print(f"Body: {definition.body}")
        
    except ValueError as e:
        print(f"Error: {e}")
