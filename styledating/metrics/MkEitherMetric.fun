functor MkEitherMetric (structure M1 : METRIC
                        structure M2 : METRIC) : METRIC =
struct
  val id = M1.id ^ ", " ^ M2.id

  fun report C =
    StrDict.mergeWith (fn (x, y) =>
      case (x, y) of
        (SOME v, _) => SOME v
      | (_, SOME v) => SOME v
      | _ => NONE)
    (M1.report C, M2.report C)
end
