--@funsearch.evolve
theorem algebra_3rootspoly_amdtamctambeqnasqmbpctapcbtdpasqmbpctapcbta (b c d a : ℂ) :
    (a - d) * (a - c) * (a - b) =
      -((a ^ 2 - (b + c) * a + c * b) * d) + (a ^ 2 - (b + c) * a + c * b) * a := by
  -- TODO: `aesop` stucks here but `suggest_tactics` works
  ring

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
