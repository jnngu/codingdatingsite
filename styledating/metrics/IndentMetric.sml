structure IndentMetric : METRIC =
struct
  val id = "indent_type"

  (* 0 - tabs
   * 1 - spaces *)
  fun report (C : Code.t) =
    let
      val lines : string list = #lines C
      fun count s =
        case String.sub (s, 0) of
          #"\t" => 1
        | #" " =>  ~1
        | _ => 0

      val total : int = List.foldr (op +) 0 (List.map count (#lines C))
    in
      StrDict.singleton (id, (Result.ABS (if total >= 0 then 0 else 1),
        fn (Result.ABS x, Result.ABS y) => if x = y then 0.0 else 5.0))
    end
end
