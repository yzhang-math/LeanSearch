--@funsearch.evolve
theorem amc12a_2008_p2 (x : ℝ) (h₀ : x * (1 / 2 + 2 / 3) = 1) : x = 6 / 7 := by
  simp_all only [one_div]
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
