class GenerateAst:
    def __init__(self, args=None):
        from os import path
        if args:
            self.outputDir = args
            return
        self.outputDir = path.dirname(path.realpath(__file__))

    def run(self):
        self.defineAst(
            "Expr",
           [
               "Binary   ; left:Expr, operator:Token, right:Expr",
               "Call     ; callee:Expr, paren:Token, args:List[Expr]",
               "Get      ; object:Expr, name:Token",
               "Grouping ; expression:Expr",
               "Literal  ; value:Any",
               "Logical  ; left:Expr, operator:Token, right: Expr",
               "Set      ; object:Expr, name:Token, value:Expr",
               "Super    ; keyword:Token, method:Token",
               "This     ; keyword:Token",
               "Unary    ; operator:Token, right:Expr",
               "Variable ; name:Token",
               "Assign   ; name: Token, value: Expr"
           ])

        self.defineAst(
            "Stmt",
            [
                "Block      ; statements:List[Stmt]",
                "Class      ; name:Token, superclass:Variable, methods:List",
                "Expression ; expression:Expr",
                "If         ; condition:Expr, thenBranch:Stmt, elseBranch:Stmt",
                "Function   ; name:Token, params:List[Token], body:List[Stmt]",
                "Print      ; expression:Expr",
                "Return     ; keyword:Token, value:Expr",
                "Var        ; name:Token, initializer:Expr",
                "While      ; condition:Expr, body:Stmt"
            ],
            imports=['.Expr']
        )

    def stripWhitespace(self, s: str):
        from re import sub
        return sub('[s+]','', s)

    def defineAst(self, baseName: str, types: list, imports=list()):
        path = f'{self.outputDir}/{baseName}.py'
        fileWriter = open(path, 'w')
        fileWriter.write('from typing import *\n')
        fileWriter.write('from .TokenType import Token\n')
        for i in imports:
            fileWriter.write(f'from {i} import *\n')
        fileWriter.write(f'class {baseName}:\n\tdef init(self): pass\n')
        fileWriter.write(f'\tdef accept(self,visitor): pass\n')
        self.defineVisitor(fileWriter, baseName, types)
        for type in types:
            className, fields = [
                x.strip() for x in type.split(';')]
            self.defineType(fileWriter, baseName, className, fields)
        fileWriter.write('\n')
        fileWriter.close()

    def defineType(self, fileWriter, baseName, className, fields):
        fileWriter.write(f'class {className}({baseName}):\n\t')
        fileWriter.write(f'def __init__(self,{fields}):\n');
        for field in fields.split(','):
            name = field.split(':')[0]
            fileWriter.write(f'\t\tself.{name} = {name}\n')
        fileWriter.write(f'\tdef accept(self, visitor:{baseName}Visitor):\n')
        fileWriter.write(f'\t\treturn visitor.visit{className}{baseName}(self)\n')
        fileWriter.write('\n')

    def defineVisitor(self, fileWriter, baseName, types):
        fileWriter.write(f'class {baseName}Visitor:\n')
        for type in types:
            typeName = type.split(';')[0].strip()
            fileWriter.write(f'\tdef visit{typeName}{baseName}(self,{baseName.lower()}:{baseName}): pass\n')
        fileWriter.write('\n')

GenerateAst().run()