structure PythonLang : LANG =
struct
  type t = { language : Languages.t,
             keywords : StrSet.set,
             delimiters : CharSet.set,
             tokens : StrSet.set,
             endl_comment_symbols : StrSet.set,
             pair_comment_symbols : string * string}

  val language = Languages.PYTHON

  val keywords = StrSet.fromList [ "and",
                                   "as",
                                   "assert",
                                   "break",
                                   "class",
                                   "continue",
                                   "def",
                                   "del",
                                   "elif",
                                   "else",
                                   "except",
                                   "False",
                                   "finally",
                                   "for",
                                   "from",
                                   "global",
                                   "if",
                                   "import",
                                   "in",
                                   "is",
                                   "lambda",
                                   "None",
                                   "nonlocal",
                                   "not",
                                   "or",
                                   "pass",
                                   "raise",
                                   "return",
                                   "True",
                                   "try",
                                   "while",
                                   "with",
                                   "yield" ]
  val delimiters = CharSet.fromList [ #" " ]

  val tokens = StrSet.fromList [ "+", "-", "*", "/",
                                 "//", ":", ")", "(",
                                 "{", "}", "[", "]", ",",
                                 ".", "?", "&", "|", "==",
                                 "=" ]

  val endl_comment_symbols = StrSet.fromList [ "#" ]
  val pair_comment_symbols = ("\"\"\"", "\"\"\"")

  fun to_lang s =
    if String.substring (s, size s - 3, 3) = ".py"
      then SOME { language = language,
             keywords = keywords,
             delimiters = delimiters,
             tokens = tokens,
             endl_comment_symbols = endl_comment_symbols,
             pair_comment_symbols = pair_comment_symbols }
      else NONE
end
