structure _Metric : METRIC =
struct
  val id = "name here"

  fun report (C : Code.t) =
      StrDict.singleton (id, Result.ABS )
end
