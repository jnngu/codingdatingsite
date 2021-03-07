functor MkEitherLang (structure L1 : LANG
                      structure L2 : LANG) : LANG =
struct
  type t = { language : Languages.t,
             keywords : StrSet.set,
             delimiters : CharSet.set,
             tokens : StrSet.set,
             endl_comment_symbols : StrSet.set,
             pair_comment_symbols : string * string }

  fun to_lang s =
    case L1.to_lang s of
      NONE => L2.to_lang s
    | SOME res => SOME res
end
