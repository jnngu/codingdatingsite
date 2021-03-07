(* CODE signature determines the important information needed to know for a
 * specific programming language *)

signature LANG =
sig
  type t = { language : Languages.t,
             keywords : StrSet.set,
             delimiters : CharSet.set,
             tokens : StrSet.set,
             endl_comment_symbols : StrSet.set,
             pair_comment_symbols : string * string }

  val to_lang : string -> t option
end
