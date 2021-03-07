structure AverageLineLengthMetric : METRIC =
struct
  val id = "average_line_length"

  fun report (C : Code.t) =
    let
      val lines = #lines C
      val lengths = map (fn l => size l) lines
    in
      StrDict.singleton (id,
        (if #num_lines C = 0 then
          Result.NORM (0.0)
        else
          Result.NORM ((real (foldr (op+) 0 lengths)) / (real (#num_lines
          C))), fn (Result.NORM x, Result.NORM y) => Compare.percent_diff_real x y 0.1
          1.0))
    end
end
