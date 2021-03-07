functor MkCode (structure Lang : LANG) : CODE =
struct
  structure Lang = Lang
  type t = { linfo : Lang.t,
             source : string,
             cleaned_source : string,
             tokens : string list,
             lines : string list,
             idents : string list,
             tokenized_lines : string list list,
             num_lines : int }

  fun pred p s =
    List.foldr (fn (a, b) => p a andalso b) true (String.explode s)

  fun set_exists p S =
    StrSet.foldl (fn (i, b) =>
      case b of
        SOME v => SOME v
      | _ => if p i then SOME i else NONE) NONE S

  fun str_cons s = (String.substring (s, 0, 1), String.substring (s, 1, size s - 1))

  fun mkCode s =
    let
      val _ = print ("for " ^ s ^ "\n")
      val lang : Lang.t = Option.valOf (Lang.to_lang s)
      val source = TextIO.inputAll (TextIO.openIn s)

        (* clean will take out all of the comment starters *)
      fun clean S =
        let
          fun clean' "" = ""
            | clean' s =
            let
              val (hd, tl) = str_cons s
              val res = clean' tl
            in
              if StrSet.exists (fn x =>
                String.isPrefix x (hd ^ res)) (#endl_comment_symbols
                lang) then ""
              else
                hd ^ res
            end
        in
          List.foldr (fn (x, y) => x ^ "\n" ^ y) "" (List.map clean' S)
        end

    fun drop s n =
      String.substring (s, n, size s - n)

    local
      val (start, stop) = #pair_comment_symbols lang
    in
      fun clean2 "" flag = ""
        | clean2 s flag =
        if not flag then
          let
            val (hd, tl) = str_cons s
          in
            if String.isPrefix start s then
              clean2 (drop s (size start)) true
            else
              hd ^ clean2 tl false
          end
        else
          if String.isPrefix stop s then
            clean2 (drop s (size stop)) false
          else
            let
              val (_, tl) = str_cons s
            in
              clean2 tl true
            end
    end

      val cleaned_source : string =
        let
          val clean_once = clean2 source false
          val clean_twice = clean (String.tokens (fn x => x = #"\n") clean_once)
        in
          clean_twice
        end

      fun expand "" = ""
        | expand s =
        case (set_exists (fn x => String.isPrefix x s) (#tokens lang),
        CharSet.exists (fn y => String.sub (s, 0) = y) (#delimiters lang)) of
          (SOME token, _) => " " ^ token ^ " " ^ expand (drop s (size token))
        | (_, true) => " " ^ String.substring (s, 0, 1) ^ " " ^ expand (drop s 1)
        | _ =>
          let
            val (hd, tl) = str_cons s
          in
            hd ^ expand tl
          end
      fun mkTokens s = String.tokens (fn x => CharSet.member
      (#delimiters lang, x)) (expand s)
      val tokens : string list = mkTokens cleaned_source

      val lines = String.tokens (fn x => x = #"\n") cleaned_source
      val num_lines = List.length lines
    in
      { linfo = lang,
        source = source,
        cleaned_source = cleaned_source,
        tokens = tokens,
        lines = lines,
        tokenized_lines = List.map mkTokens lines,
        idents = List.filter
          (fn x => not (StrSet.member (#keywords lang, x)
               orelse StrSet.member (#tokens lang, x)
               orelse pred Char.isDigit x)) tokens,
        num_lines = num_lines }
    end

end
