structure MaxLineLengthMetric : METRIC =
struct
  val id = "max_line_length"

  fun report (C : Code.t) =
    let
      val lines = #lines C
      val lengths = map (fn l => size l) lines
    in
      StrDict.singleton (id,
        (if length lengths = 0 then
          Result.ABS 0
        else
          Result.ABS (List.foldr (fn (x, y) => if x >= y then x else y) (List.nth (lengths,
          0)) (lengths)), fn (Result.ABS x, Result.ABS y) =>
            let
              val (lo, hi) = Compare.order_int x y
            in
              (real (hi - lo)) / 30.0
            end))
    end
end
