structure CLang : LANG =
struct
  type t = { language : Languages.t,
             keywords : StrSet.set,
             delimiters : CharSet.set,
             tokens : StrSet.set,
             endl_comment_symbols : StrSet.set,
             pair_comment_symbols : string * string }

  val language = Languages.C
  val keywords = StrSet.fromList [ "auto",
                                   "break",
                                   "case",
                                   "char",
                                   "const",
                                   "continue",
                                   "default",
                                   "do",
                                   "double",
                                   "else",
                                   "enum",
                                   "extern",
                                   "float",
                                   "for",
                                   "goto",
                                   "if",
                                   "inline",
                                   "int",
                                   "long",
                                   "register",
                                   "restrict",
                                   "return",
                                   "short",
                                   "signed",
                                   "sizeof",
                                   "static",
                                   "struct",
                                   "switch",
                                   "typedef",
                                   "union",
                                   "unsigned",
                                   "void",
                                   "volatile",
                                   "while" ]

  val delimiters = CharSet.fromList [ #"\t",
                                      #"\n",
                                      #" " ]

  val tokens = StrSet.fromList [ "+", "-", "*", "/",
                                 "+=", "-=", "*=", "/=",
                                 "==", "?", ":", "(", ")", ";",
                                 "{", "}", "[", "]", "%", "!",
                                 "<", ">", ".", ",", "|", "&",
                                 "++", "--", "\"", "'", "=" ]
  val endl_comment_symbols = StrSet.fromList [ "//" ]
  val pair_comment_symbols = ("/*", "*/")

  fun to_lang s =
    if String.substring (s, size s - 2, 2) = ".c"
      then SOME { language = language,
                  keywords = keywords,
                  delimiters = delimiters,
                  tokens = tokens,
                  endl_comment_symbols = endl_comment_symbols,
                  pair_comment_symbols = pair_comment_symbols}
      else NONE
end
