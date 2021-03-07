structure CharKey : ORD_KEY =
struct
  type ord_key = char

  val compare = Char.compare
end
