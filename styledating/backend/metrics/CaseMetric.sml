structure CaseMetric : METRIC =
struct
  val id = "case_metric"

  fun report (C : Code.t) =
    let
      val idents = #idents C
      datatype kinds = CAMEL | SNAKE | PASCAL | UNKNOWN
      val sorted = List.map (fn s =>
        case Char.isUpper (String.sub (s, 0)) of
          true => PASCAL
        | false =>
          if String.isSubstring "_" s then
            SNAKE
          else
            if List.exists (fn x => Char.isUpper x) (String.explode s) then
              CAMEL
            else
              UNKNOWN) idents
      fun f x = List.filter (fn y => y = x) sorted
      val (L as [camelSum, snakeSum, pascalSum, unknownSum]) =
        [(0, List.length (f CAMEL)),
         (1, List.length (f SNAKE)),
         (2, List.length (f PASCAL)),
         (3, List.length (f UNKNOWN))]

      val (v, max) = List.foldr (fn ((a, v1), (b, v2)) =>
        if v1 > v2 then (a, v1) else (b, v2)) camelSum L
    in
      StrDict.singleton (id, (Result.ABS v, fn (Result.ABS n, Result.ABS m) =>
      if n = m then 0.0 else 15.0))
    end
end
