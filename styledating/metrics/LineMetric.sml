structure LineMetric : METRIC =
struct
  val id = "num_lines"
  fun report (C : Code.t) = StrDict.singleton (id,
    (Result.ABS (#num_lines C), fn (Result.ABS x, Result.ABS y) =>
    Compare.percent_diff_int x y 0.1 1.0))
end
