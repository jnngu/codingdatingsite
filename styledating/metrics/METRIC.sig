(* each separate metric will ascribe to ANALYSIS *)

signature METRIC =
sig
  val id : string
  val report : Code.t -> (Result.t * (Result.t * Result.t -> real)) StrDict.map
end
