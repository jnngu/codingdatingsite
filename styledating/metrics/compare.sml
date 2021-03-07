structure Compare =
struct

  fun order_int x y = if x < y then (x, y) else (y, x)
  fun order_real (x : real) (y : real) = if x < y then (x, y) else (y, x)
  fun percent_diff_int n m d w =
    let
      val (lo, hi) = order_int n m
    in
      ((((real hi) / (real lo)) - 1.0) / d) * w
    end
  fun percent_diff_real n m d w =
    let
      val (lo, hi) = order_real n m
    in
      (((hi / lo) - 1.0) / d) * w
    end
end
