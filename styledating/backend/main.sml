
structure Main =
struct
  open Result
  fun doTheThing name =
    let
      val C = Code.mkCode name
      val res = Metrics.report C
      val outs = TextIO.openOut (name ^ ".analysis")
      fun publish D =
      StrDict.foldli (fn (name, (res, _), ()) =>
      case res of
        ABS n =>
          (TextIO.output (outs, name ^ ", ");
          TextIO.output (outs, Int.toString n ^ "\n"))
      | NORM f =>
          (TextIO.output (outs, name ^ ", ");
          TextIO.output (outs, Real.toString f ^ "\n"))) () D
    in
      publish res
    end

  fun check file1 file2 =
    let
      val (code1, code2) = (Code.mkCode file1, Code.mkCode file2)
      val (report1, report2) = (Metrics.report code1, Metrics.report
      code2)
      val (lang1, lang2) = (#language (#linfo code1), #language (#linfo code2))
      val both = StrDict.mergeWith (fn (x, y) =>
        case (x, y) of
          (SOME (v1, f), SOME (v2, _)) => SOME (f (v1, v2))
        | _ => NONE) (report1, report2)
    in
      StrDict.foldli (fn (name, x, y) => (x + y)) 0.0 both
    end

end

val SOME s = TextIO.inputLine TextIO.stdIn
val (L as [name1, name2]) = String.tokens (fn x => x = #" ") s
val [name1, name2] = map String.implode (map (List.filter (fn x => not (Char.isSpace
x))) (map String.explode L))
val score = Main.check name1 name2

val outs = TextIO.openOut "output"
val _ = TextIO.output (outs, Real.toString score)
