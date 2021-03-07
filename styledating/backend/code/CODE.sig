(* signature of code with some added information *)
(* structures ascribing to TEXT encode a given person's program, along with some
 * helper functions that act upon that program *)

signature CODE =
sig
  structure Lang : LANG

  type t = { linfo : Lang.t,
             source : string,
             cleaned_source : string,
             tokens : string list,
             lines : string list,
             tokenized_lines : string list list,
             idents : string list,
             num_lines : int }

  val mkCode : string -> t
end
